import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- Database Configuration ---
    # Check for DATABASE_URL first (common in production/PaaS)
    _db_url = os.getenv('DATABASE_URL')
    
    if _db_url:
        SQLALCHEMY_DATABASE_URI = _db_url
    elif os.environ.get('DB_USER') and os.environ.get('DB_NAME'):
        # Construct from individual parts if provided
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@"
            f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
        )
    else:
        # Fallback to SQLite for local development if no env vars are set
        SQLALCHEMY_DATABASE_URI = 'sqlite:///mathyou.db'

class TestingConfig(Config):
    """Configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False