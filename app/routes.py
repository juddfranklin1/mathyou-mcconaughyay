"""Routes for the math learning application."""

from flask import render_template, jsonify, request, abort
import logging
from .models import Subject, Concept, Question

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