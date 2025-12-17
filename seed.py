import os
from app import create_app, db
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

from app.models import Subject, Concept, Question
from data.disciplines import DISCIPLINES

def slugify(text):
    """A simple function to create a URL-friendly slug."""
    return text.lower().replace(' ', '-')

def seed_data():
    """Seeds the database with subjects, concepts, and questions."""
    app = create_app()
    with app.app_context():
        # Clear existing data to prevent duplicates on re-run
        db.session.query(Question).delete()
        db.session.query(Concept).delete()
        db.session.query(Subject).delete()
        db.session.commit()
        print("Cleared existing data.")

        for subject_slug, subject_data in DISCIPLINES.items():
            # 1. Create the Subject
            subject = Subject(name=subject_data['name'], slug=subject_slug)
            db.session.add(subject)
            print(f"Seeding Subject: {subject.name}")

            # 2. Create Concepts for the Subject
            for concept_name, concept_details in subject_data['concepts'].items():
                concept = Concept(
                    name=concept_name,
                    slug=slugify(concept_name),
                    subject=subject, # Automatically links subject_id
                    formula=concept_details.get('formula'),
                    explanation=concept_details.get('explanation'),
                    core_idea=concept_details.get('core_idea'),
                    real_world_application=concept_details.get('real_world_application'),
                    mathematical_demonstration=concept_details.get('mathematical_demonstration'),
                    study_plan=concept_details.get('study_plan')
                )
                db.session.add(concept)

                # 3. Create Questions for the Concept
                problems_data = subject_data.get('problems') or {}
                problem_set = problems_data.get(concept_name, [])
                for problem in problem_set:
                    question = Question(
                        legacy_id=problem['id'],
                        concept=concept, # Automatically links concept_id
                        problem_text=problem['problem'],
                        difficulty=problem.get('difficulty'),
                        explanation=problem.get('explanation'),
                        # Store the rest of the data in the JSONB field
                        data={k: v for k, v in problem.items() if k not in ['id', 'problem', 'difficulty', 'explanation']}
                    )
                    db.session.add(question)

        # Commit all the changes to the database
        db.session.commit()
        print("Database seeding complete!")

if __name__ == '__main__':
    seed_data()
