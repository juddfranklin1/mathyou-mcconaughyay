"""Routes for the math learning application."""

from flask import render_template, jsonify, request, abort, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import logging
import uuid
import os
import google.generativeai as genai
from .models import Subject, Concept, Question, User, UserResponse, db

# --- Gemini Configuration & System Prompt ---

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# You can customize the system prompt here to change the AI's behavior
TEACHER_PERSONA_PROMPT = """
You are a patient, friendly, and relatable math teacher who enjoys irreverent humor and punk rock culture, but you like to make sure your teaching stays relevant to practical use cases in real-world jobs and situations.
Your task is to provide helpful feedback to students who are answering practice questions. Your goal is to get students to understand math in a practical way, so you often use real-world examples.

Problem: {problem_text}
Correct Answer: {correct_answer}
Student's Answer: {user_answer}
Is the answer correct?: {is_correct}

Instructions:
1. If the answer is INCORRECT:
   - Interpret why the student might have chosen that answer.
   - Explain the concept clearly to guide them back to the right path.
   - Do not simply state the answer if possible, help them derive it.
   - Use a gentle tone.

2. If the answer is CORRECT:
   - Congratulate them coolly, in a punk rock way.
   - Provide a brief follow-up that describes a practical, real-world use case for the concept they are working on. Building on that example, provide a mathematical representation of the real world problem that would function as a practical use of the concept. Encourage them to try to answer it independently.

3. Tone and Style:
   - Don't be afraid to be brusque, and sarcastic. You can even be a bit harsh, but only in a playful, punk rock way.
   - Keep the response concise (under 150 words).
   - Format all mathematical expressions using LaTeX syntax. Enclose inline math in single dollar signs ($) and display math in double dollar signs ($$).
"""

def get_ai_feedback(question, user_answer, is_correct):
    """Generates custom feedback using Gemini based on the user's answer."""
    if not GEMINI_API_KEY:
        return None

    try:
        # Format the prompt inputs
        problem_text = question.problem_text
        correct_val = question.data.get('answer')
        user_val = user_answer

        # If multiple choice, provide context about the choices
        if question.data.get('type') == 'multiple_choice':
            choices = question.data.get('choices', [])
            problem_text += "\nChoices: " + ", ".join([f"({i}) {c}" for i, c in enumerate(choices)])
            
            # Try to map indices to text for better AI context
            try:
                u_idx = int(user_answer)
                user_val = f"{u_idx} ({choices[u_idx]})" if 0 <= u_idx < len(choices) else str(user_answer)
            except (ValueError, TypeError):
                pass
                
            try:
                c_idx = int(correct_val)
                correct_val = f"{c_idx} ({choices[c_idx]})" if 0 <= c_idx < len(choices) else str(correct_val)
            except (ValueError, TypeError):
                pass

        prompt = TEACHER_PERSONA_PROMPT.format(
            problem_text=problem_text,
            correct_answer=correct_val,
            user_answer=user_val,
            is_correct="Yes" if is_correct else "No"
        )

        # Try multiple model variants to find one that works for the user's API key
        candidate_models = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.0-pro', 'gemini-pro']
        
        for model_name in candidate_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                logging.warning(f"Model {model_name} failed: {e}")
                continue
        
        return None
    except Exception as e:
        logging.error(f"Error generating AI feedback: {e}")
        return None

def init_routes(app):
    # Custom 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return render_template('index.html', active_page='home')

    @app.route('/<string:subject_slug>')
    def discipline_page(subject_slug):
        # Query the database for the subject by its slug.
        # .first_or_404() is a handy shortcut that returns the first result
        # or automatically triggers a 404 error if no result is found.
        subject = Subject.query.filter_by(slug=subject_slug).first_or_404()

        # Reconstruct the practice problems dictionary from the database
        # to pass to the math-content web component.
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

        # app.logger.info(f"Passing problems_by_concept to template for '{subject.name}': {problems_by_concept}")

        # The template name is now derived from the subject slug.
        template_name = f"{subject.slug.replace('-', '_')}.html"

        return render_template(template_name,
                             discipline_name=subject.name,
                             concepts=subject.concepts, # Pass the list of Concept objects
                             active_page=subject.slug,
                             problems=problems_by_concept)

    @app.route('/api/concept')
    def api_concept():
        subject_slug = request.args.get('discipline')
        concept_slug = request.args.get('concept')

        # Find the concept by joining Subject and filtering by both slugs.
        concept = Concept.query.join(Subject).filter(
            Subject.slug == subject_slug,
            Concept.slug == concept_slug
        ).first()

        if not concept:
            return jsonify({'error': 'Concept not found'}), 404

        # Return the concept data as a dictionary.
        return jsonify({
            'name': concept.name,
            'formula': concept.formula,
            'explanation': concept.explanation,
            'core_idea': concept.core_idea,
            'real_world_application': concept.real_world_application,
            'mathematical_demonstration': concept.mathematical_demonstration,
            'study_plan': concept.study_plan,
            'questions': [q.legacy_id for q in concept.questions] # Optionally include question IDs
        })

    @app.route('/api/question/<string:legacy_id>')
    def api_question(legacy_id):
        """API endpoint to fetch a single question by its legacy ID."""
        
        # Handle special Gemini Trigger ID
        if legacy_id.startswith('gemini_trigger_'):
            concept_slug = legacy_id.replace('gemini_trigger_', '')
            concept = Concept.query.filter_by(slug=concept_slug).first()
            concept_name = concept.name if concept else concept_slug.replace('-', ' ')
            
            prompt = f"Provide a real-world example of a math problem that demonstrates the concept of {concept_name}. The output should be a practical scenario followed by a question, but do not provide the answer immediately. Format it as a practice problem."
            
            ai_content = "This concept is mastered! Here is a real-world application..."
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                ai_content = response.text
            except Exception as e:
                logging.error(f"Gemini trigger failed: {e}")
                ai_content = f"Great job! You've mastered {concept_name}. Try applying this to real-world physics or engineering problems."

            return jsonify({
                'id': legacy_id,
                'problem': ai_content,
                'difficulty': 'Real World Application',
                'explanation': 'This is an advanced application of the concept you have mastered.',
                'type': 'numerical', # Dummy type to satisfy frontend
                'answer': '0' # Dummy answer
            })

        app.logger.info(f"API request received for question with legacy_id: '{legacy_id}'")
        question = Question.query.filter_by(legacy_id=legacy_id).first_or_404()

        # The 'data' field in the DB holds 'type', 'choices', 'answer' etc.
        # We merge it with the other question fields to create a full response.
        response_data = {
            'id': question.legacy_id,
            'problem': question.problem_text,
            'difficulty': question.difficulty,
            'explanation': question.explanation,
        }
        response_data.update(question.data)

        return jsonify(response_data)

    @app.route('/api/question/create', methods=['POST'])
    @login_required
    def create_question():
        """API endpoint to add a new practice problem."""
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        subject_slug = data.get('subject_slug')
        concept_slug = data.get('concept_slug')

        # Find the concept
        concept = Concept.query.join(Subject).filter(
            Subject.slug == subject_slug,
            Concept.slug == concept_slug
        ).first()

        if not concept:
            return jsonify({'error': 'Concept not found'}), 404

        legacy_id = data.get('legacy_id') or f"{concept.slug}_{uuid.uuid4().hex[:8]}"
        if Question.query.filter_by(legacy_id=legacy_id).first():
            return jsonify({'error': 'Question ID already exists'}), 400

        question = Question(
            legacy_id=legacy_id,
            concept_id=concept.id,
            problem_text=data.get('problem_text'),
            difficulty=data.get('difficulty', 'Medium'),
            explanation=data.get('explanation'),
            data=data.get('data', {})
        )
        db.session.add(question)
        db.session.commit()

        return jsonify({'message': 'Question created', 'id': legacy_id}), 201

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            if User.query.filter_by(email=email).first():
                flash('Email already registered')
                return redirect(url_for('register'))
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user is None or not user.check_password(password):
                flash('Invalid email or password')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/change_password', methods=['POST'])
    @login_required
    def change_password():
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        if not current_user.check_password(current_password):
            flash('Invalid current password')
            return redirect(url_for('profile'))

        current_user.set_password(new_password)
        db.session.commit()
        flash('Your password has been updated.')
        return redirect(url_for('profile'))

    @app.route('/reset_password_request', methods=['GET', 'POST'])
    def reset_password_request():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                token = user.get_reset_token()
                # In a real application, you would send an email here.
                # For demonstration, we log the link to the console.
                reset_url = url_for('reset_password', token=token, _external=True)
                app.logger.info(f"Password reset link for {email}: {reset_url}")
            
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('login'))
        return render_template('reset_password_request.html')

    @app.route('/reset_password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        user = User.verify_reset_token(token)
        if not user:
            flash('Invalid or expired token')
            return redirect(url_for('index'))
        if request.method == 'POST':
            password = request.form.get('password')
            user.set_password(password)
            db.session.commit()
            flash('Your password has been reset.')
            return redirect(url_for('login'))
        return render_template('reset_password.html')

    @app.route('/profile')
    @login_required
    def profile():
        responses = UserResponse.query.filter_by(user_id=current_user.id).order_by(UserResponse.timestamp.desc()).all()
        return render_template('profile.html', responses=responses)

    @app.route('/api/question/submit_answer', methods=['POST'])
    @login_required
    def submit_answer():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        legacy_id = data.get('question_id')
        user_answer = data.get('answer')

        if not legacy_id or user_answer is None:
            return jsonify({'error': 'Missing question_id or answer'}), 400

        question = Question.query.filter_by(legacy_id=legacy_id).first_or_404()

        # Check correctness (converting to string handles both integer indices and string answers)
        correct_answer = question.data.get('answer')
        is_correct = str(user_answer).strip() == str(correct_answer).strip()

        # Record the response
        response = UserResponse(
            user_id=current_user.id,
            question_id=question.id,
            response_data={'answer': user_answer},
            is_correct=is_correct
        )
        db.session.add(response)
        db.session.commit()

        # Generate AI feedback
        ai_explanation = get_ai_feedback(question, user_answer, is_correct)
        
        # Fallback to static explanation if AI fails or is not configured
        final_explanation = ai_explanation if ai_explanation else question.explanation

        return jsonify({
            'correct': is_correct,
            'explanation': final_explanation
        })