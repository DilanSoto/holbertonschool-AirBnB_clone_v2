#!/usr/bin/python3
"""
Module for console
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City
from datetime import datetime


def split_curly_braces(e_arg):
    """
    Splits the curly braces for the update method
    """
    try:
        curly_braces = re.search(r"\{(.*?)\}", e_arg)
        if curly_braces:
            id_with_comma = shlex.split(e_arg[:curly_braces.span()[0]])
            id = [i.strip(",") for i in id_with_comma][0]

            str_data = curly_braces.group(1)
            arg_dict = ast.literal_eval("{" + str_data + "}")
            return id, arg_dict
        else:
            commands = e_arg.split(",")
            if commands:
                id = commands[0]
                attr_name = commands[1] if len(commands) > 1 else ""
                attr_value = commands[2] if len(commands) > 2 else ""
                return f"{id}", f"{attr_name} {attr_value}"
    except Exception as e:
        print(f"Error: {e}")
    return "", ""


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Amenity",
                     "Place", "Review", "State", "City"]

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_EOF(self, arg):
        """
        EOF (Ctrl+D) signal to exit the program.
        """
        return True

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_create(self, arg):
        """
        Create a new instance of BaseModel and save it to the JSON file.
        Usage: create <class_name> [attribute_1=value_1] [attribute_2=value_2] ...
        """
        try:
            class_name = arg.split(" ")[0]
            if not class_name:
                print("** class name missing **")
                return
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
                return

            kwargs = {}
            commands = shlex.split(arg)
            for command in commands[1:]:
                key, value = command.split("=")
                if value.startswith('"'):
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = ast.literal_eval(value)
                    except (SyntaxError, ValueError):
                        pass
                kwargs[key] = value

            new_instance = globals()[class_name](**kwargs)
            storage.new(new_instance)
            storage.save()
            print(new_instance.id)
        except Exception as e:
            print(f"Error: {e}")

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        try:
            commands = shlex.split(arg)
            if len(commands) == 0:
                print("** class name missing **")
                return
            if commands[0] not in self.valid_classes:
                print("** class doesn't exist **")
                return
            if len(commands) < 2:
                print("** instance id missing **")
                return
            key = "{}.{}".format(commands[0], commands[1])
            objects = storage.all()
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")
        except Exception as e:
            print(f"Error: {e}")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        try:
            commands = shlex.split(arg)
            if len(commands) == 0:
                print("** class name missing **")
                return
            if commands[0] not in self.valid_classes:
                print("** class doesn't exist **")
                return
            if len(commands) < 2:
                print("** instance id missing **")
                return
            key = "{}.{}".format(commands[0], commands[1])
            objects = storage.all()
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")
        except Exception as e:
            print(f"Error: {e}")

    def do_all(self, arg):
        """
        Print the string representation of all instances or a specific class.
        Usage: all [class_name]
        """
        try:
            objects = storage.all()
            commands = shlex.split(arg)
            if len(commands) == 0:
                for key, value in objects.items():
                    print(value)
            elif commands[0] not in self.valid_classes:
                print("** class doesn't exist **")
            else:
                for key, value in objects.items():
                    if key.split('.')[0] == commands[0]:
                        print(value)
        except Exception as e:
            print(f"Error: {e}")

    def do_count(self, arg):
        """
        Counts and retrieves the number of instances of a class.
        Usage: <class name>.count()
        """
        try:
            objects = storage.all()
            commands = shlex.split(arg)
            if len(commands) == 0:
                print("** class name missing **")
                return
            class_name = commands[0]
            count = sum(1 for obj in objects.values() if obj.__class__.__name__ == class_name)
            print(count)
        except Exception as e:
            print(f"Error: {e}")

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        try:
            commands = shlex.split(arg)
            if len(commands) < 4:
                print("** Usage: update <class_name> <id> <attribute_name> '<attribute_value>' **")
                return
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key not in objects:
                print("** no instance found **")
                return
            obj = objects[key]
            attr_name = commands[2]
            attr_value = " ".join(commands[3:])
            if attr_value.startswith('"') and attr_value.endswith('"'):
                attr_value = attr_value[1:-1]
            try:
                attr_value = ast.literal_eval(attr_value)
            except (ValueError, SyntaxError):
                pass
            setattr(obj, attr_name, attr_value)
            obj.save()
        except Exception as e:
            print(f"Error: {e}")

    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
        """
        try:
            arg_list = arg.split('.')
            class_name = arg_list[0]
            command = arg_list[1].split('(')
            method_name = command[0]
            extra_args = command[1].split(')')[0]

            method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
            }

            if method_name in method_dict:
                method = method_dict[method_name]
                if method_name != "update":
                    return method("{} {}".format(class_name, extra_args))
                else:
                    obj_id, attr_dict = split_curly_braces(extra_args)
                    return method("{} {} {}".format(class_name, obj_id, attr_dict))
            else:
                print("*** Unknown syntax: {}".format(arg))
                return False
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
