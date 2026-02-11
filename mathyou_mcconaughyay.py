"""Main application file for the math learning web application."""

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

from app import create_app, db
from app.models import Subject, Concept, Question, UserResponse

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Subject': Subject,
        'Concept': Concept,
        'Question': Question,
        'UserResponse': UserResponse
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)