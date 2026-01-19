from flask import Flask
from werkzeug.routing import BaseConverter
import logging

from .config import Config
from .extensions import db, migrate, login_manager
from .blueprints.main import main_bp
from .blueprints.auth import auth_bp
from .blueprints.api import api_bp


class RegexConverter(BaseConverter):
    """Permits regular expressions in routes."""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

def create_app(config_class=Config):
    """Create and configure an instance of the Flask application."""
    app = Flask(
        __name__,
        static_folder='../static',
        static_url_path='/static',
        template_folder='../templates'
    )

    # --- Configuration ---
    app.config.from_object(config_class)

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
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # --- Register Routes and Converters ---
    app.url_map.converters['regex'] = RegexConverter
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app