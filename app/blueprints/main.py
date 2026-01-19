from flask import Blueprint, render_template
from flask_login import current_user
from app.models import Subject, UserResponse

main_bp = Blueprint('main', __name__)

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main_bp.route('/')
def index():
    return render_template('index.html', active_page='home')

@main_bp.route('/<string:subject_slug>')
def discipline_page(subject_slug):
    # Query the database for the subject by its slug.
    subject = Subject.query.filter_by(slug=subject_slug).first_or_404()

    # Reconstruct the practice problems dictionary from the database
    problems_by_concept = {}
    
    # Difficulty mapping
    difficulty_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}
    reverse_difficulty_map = {1: 'Easy', 2: 'Medium', 3: 'Hard'}

    for concept in subject.concepts:
        questions = concept.questions
        if not questions:
            continue

        target_difficulty = 'Easy' # Default

        if current_user.is_authenticated:
            # Get all question IDs for this concept
            q_ids = [q.id for q in questions]
            
            # Find which ones the user has answered correctly
            responses = UserResponse.query.filter(
                UserResponse.user_id == current_user.id,
                UserResponse.question_id.in_(q_ids),
                UserResponse.is_correct == True
            ).all()
            
            if responses:
                # Find the max difficulty solved
                solved_q_ids = {r.question_id for r in responses}
                solved_questions = [q for q in questions if q.id in solved_q_ids]
                
                max_diff_val = 0
                for q in solved_questions:
                    val = difficulty_map.get(q.difficulty, 0)
                    if val > max_diff_val:
                        max_diff_val = val
                
                # Target is one step up
                target_val = max_diff_val + 1
                if target_val > 3:
                    # User has mastered all levels -> Trigger Gemini
                    problems_by_concept[concept.slug] = [f"gemini_trigger_{concept.slug}"]
                    continue
                
                target_difficulty = reverse_difficulty_map.get(target_val, 'Easy')

        # Find a question with the target difficulty
        # We pick the first one matching the difficulty
        candidate = next((q for q in questions if q.difficulty == target_difficulty), None)
        
        if candidate:
            problems_by_concept[concept.slug] = [candidate.legacy_id]
        elif not current_user.is_authenticated:
                # Fallback for unauth users if 'Easy' is missing, just take first available
                problems_by_concept[concept.slug] = [questions[0].legacy_id]

    return render_template('discipline.html',
                            discipline_name=subject.name,
                            concepts=subject.concepts,
                            active_page=subject.slug,
                            problems=problems_by_concept)