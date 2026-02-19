import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, make_transient
from app import create_app, db
from app.models import User, Subject, Concept, Question, UserResponse

# 1. Configuration
# Ensure DATABASE_URL is set to your Postgres connection string in your .env file
PG_URI = 'postgresql://mathyou_admin:28hiSdjuKU@localhost:5432/mathyou'
# Load environment variables from .env file to ensure DATABASE_URL is available
from dotenv import load_dotenv
load_dotenv()

PG_URI = os.environ.get('DATABASE_URL')
SQLITE_URI = 'sqlite:///mathyou.db'

def migrate():
    if not PG_URI:
        print("Error: DATABASE_URL environment variable is not set.")
        print("Please ensure your .env file contains the Postgres connection string.")
        return

    print(f"Source (Postgres): {PG_URI}")
    print(f"Destination (SQLite): {SQLITE_URI}")

    # 2. Connect to Source (Postgres)
    pg_engine = create_engine(PG_URI)
    PG_Session = sessionmaker(bind=pg_engine)
    pg_session = PG_Session()

    # 3. Connect to Destination (SQLite)
    sqlite_engine = create_engine(SQLITE_URI)
    SQLite_Session = sessionmaker(bind=sqlite_engine)
    sqlite_session = SQLite_Session()

    # 4. Create Tables in SQLite
    # We use the app context to ensure SQLAlchemy metadata is loaded correctly
    app = create_app()
    with app.app_context():
        print("Creating tables in SQLite...")
        db.metadata.create_all(bind=sqlite_engine)

    # 5. Transfer Data
    # Order matters to satisfy Foreign Key constraints
    models_to_migrate = [User, Subject, Concept, Question, UserResponse]

    try:
        for model in models_to_migrate:
            table_name = model.__tablename__
            print(f"Migrating table: {table_name}...")
            
            # Fetch all records from Postgres
            records = pg_session.query(model).all()
            print(f"  Found {len(records)} records.")

            for record in records:
                # Detach from Postgres session and make transient (like a new object)
                pg_session.expunge(record)
                make_transient(record)
                
                # Add to SQLite session
                sqlite_session.add(record)
            
            sqlite_session.commit()
            print(f"  Committed {table_name}.")
            
        print("\nMigration successful! Data is now in 'mathyou.db'.")
        
    except Exception as e:
        print(f"\nError during migration: {e}")
        sqlite_session.rollback()
    finally:
        pg_session.close()
        sqlite_session.close()

if __name__ == "__main__":
    migrate()