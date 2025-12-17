from flask import Flask
import os
from flask_migrate import Migrate
from werkzeug.routing import BaseConverter
import logging

from .models import db
from .routes import init_routes


class RegexConverter(BaseConverter):
    """Permits regular expressions in routes."""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(
        __name__,
        static_folder='../static',
        static_url_path='/static',
        template_folder='../templates'
    )

    # --- Database Configuration ---
    # Allow overriding the DB via DATABASE_URL env var for local dev (e.g., sqlite)
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        DB_USER = os.environ['DB_USER']
        DB_PASSWORD = os.environ['DB_PASSWORD']
        DB_HOST = os.environ['DB_HOST']
        DB_PORT = os.environ['DB_PORT']
        DB_NAME = os.environ['DB_NAME']

        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Logging Configuration ---
    # Only configure logging when not in testing mode
    if not app.testing:
        # Set the logging level to INFO
        app.logger.setLevel(logging.INFO)
        # Create a handler to output to the console (stderr)
        stream_handler = logging.StreamHandler()
        app.logger.addHandler(stream_handler)

    # --- Initialize Extensions ---
    db.init_app(app)
    Migrate(app, db)

    # --- Register Routes and Converters ---
    app.url_map.converters['regex'] = RegexConverter
    init_routes(app)

    return app