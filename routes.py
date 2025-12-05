"""Routes for the math learning application."""

from flask import render_template, jsonify, request, abort
from data.disciplines import DISCIPLINES

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html', active_page='home')

    # Use the 'regex' converter to safely handle hyphens in route names.
    # This creates a pattern like '(linear-algebra|calculus|...)'
    valid_disciplines_regex = '|'.join(DISCIPLINES.keys())
    @app.route(f'/<regex("({valid_disciplines_regex})"):discipline_id>')
    def discipline_page(discipline_id):
        discipline = DISCIPLINES.get(discipline_id)
        if not discipline:
            abort(404)
        
        # Create the concepts list using the dictionary key for the name and a slug for the id.
        concepts_list = [{'id': k.lower().replace(' ', '-'), 'name': k}
                         for k, v in discipline['concepts'].items() if isinstance(v, dict)]
        return render_template(discipline['template'],
                             discipline_name=discipline['name'],
                             concepts=concepts_list,
                             active_page=discipline_id,
                             practice_problems=discipline.get('problems'))

    @app.route('/api/concept')
    def api_concept():
        discipline_id = request.args.get('discipline')
        concept_id = request.args.get('concept')
        discipline = DISCIPLINES.get(discipline_id)
        if not discipline or not concept_id:
            return jsonify({'error': 'Missing discipline or concept ID'}), 400
        
        # Find the concept by matching the slug-like ID against the keys.
        for key, value in discipline['concepts'].items():
            if concept_id == key.lower().replace(' ', '-'):
                # Add the name to the returned data, as the component expects it.
                response_data = value.copy()
                response_data['name'] = key
                return jsonify(response_data)

        return jsonify({'error': 'Concept not found'}), 404