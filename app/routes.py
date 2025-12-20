"""Routes for the math learning application."""

from flask import render_template, jsonify, request, abort, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import logging
from .models import Subject, Concept, Question, User, UserResponse, db

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
        for concept in subject.concepts:
            if concept.questions:
                # Use the concept's slug as the key for consistency with the frontend.
                problems_by_concept[concept.slug] = [q.legacy_id for q in concept.questions]
        app.logger.info(f"Passing problems_by_concept to template for '{subject.name}': {problems_by_concept}")

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

        return jsonify({
            'correct': is_correct,
            'explanation': question.explanation
        })