#!/usr/bin/python3

# Import the Flask class from the flask package
from flask import Flask

# Create an instance of the Flask class and assign it to the variable 'app'
app = Flask(__name__)

# Define a route for the root URL '/', with the strict_slashes=False option to accept the URL with or without a trailing slash
@app.route('/', strict_slashes=False)
def hello():
    return 'Hello HBNB!'

# Define a route for the '/hbnb' URL, with the strict_slashes=False option to accept the URL with or without a trailing slash
@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'

# Define a dynamic route for the '/c/<text>' URL, where '<text>' is a variable part of the URL, with the strict_slashes=False option to accept the URL with or without a trailing slash
@app.route('/c/<text>', strict_slashes=False)
def replace_text(text):
    replaced_text = text.replace("_", " ")
    return 'C ' + replaced_text

# Define a dynamic route for the '/python/<text>' URL, where '<text>' is a variable part of the URL and has a default value "is cool", with the strict_slashes=False option to accept the URL with or without a trailing slash
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    formatted_text = "Python " + text.replace("_", " ")
    return formatted_text

@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    return f'{n} is a number'

@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('number_template.html', number=n)

# Run the Flask application on host '0.0.0.0' and port 5000 if this script is executed as the main script
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
