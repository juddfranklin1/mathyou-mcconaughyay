"""Main application file for the math learning web application."""

from flask import Flask
from routes import init_routes

app = Flask(__name__)

# Initialize all routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)