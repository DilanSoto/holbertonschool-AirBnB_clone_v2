#!/usr/bin/python3
""" DBStorage engine """
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class DBStorage:
    """ database storage engine """

    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """ add obj to session """
        self.__session.add(obj)

    def save(self):
        """ commit all changes to session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete obj from session """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database  and initializes a session """
        Base.metadata.create_all(self.__engine)
        session_creat = sessionmaker(bind=self.__engine,
                                     expire_on_commit=False)
        Session = scoped_session(session_creat)
        self.__session = Session()
