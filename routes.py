"""Routes for the math learning application."""

from flask import render_template, jsonify, request
from data import (
    LINEAR_ALGEBRA_CONCEPTS,
    DIFFERENTIAL_CALCULUS_CONCEPTS,
    INTEGRATION_CONCEPTS,
    TRIGONOMETRY_CONCEPTS
)
from data.practice_problems import LINEAR_ALGEBRA_PROBLEMS

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html', active_page='home')

    @app.route('/linear-algebra')
    def linear_algebra():
        return render_template('linear_algebra.html', 
                             concepts=list(LINEAR_ALGEBRA_CONCEPTS.keys()),
                             active_page='linear-algebra',
                             practice_problems=LINEAR_ALGEBRA_PROBLEMS)

    @app.route('/calculus')
    def calculus():
        return render_template('calculus.html', 
                             concepts=list(DIFFERENTIAL_CALCULUS_CONCEPTS.keys()),
                             active_page='calculus')

    @app.route('/integration')
    def integration():
        return render_template('integration.html', 
                             concepts=list(INTEGRATION_CONCEPTS.keys()),
                             active_page='integration')

    @app.route('/concept')
    def concept():
        name = request.args.get('name')
        data = LINEAR_ALGEBRA_CONCEPTS.get(name, {})
        return jsonify(data)

    @app.route('/calculus_concept')
    def calculus_concept():
        name = request.args.get('name')
        data = DIFFERENTIAL_CALCULUS_CONCEPTS.get(name, {})
        return jsonify(data)

    @app.route('/integration_concept')
    def integration_concept():
        name = request.args.get('name')
        data = INTEGRATION_CONCEPTS.get(name, {})
        return jsonify(data)
        
    @app.route('/trigonometry')
    def trigonometry():
        return render_template('trigonometry.html', 
                             concepts=list(TRIGONOMETRY_CONCEPTS.keys()),
                             active_page='trigonometry')

    @app.route('/trigonometry_concept')
    def trigonometry_concept():
        name = request.args.get('name')
        data = TRIGONOMETRY_CONCEPTS.get(name, {})
        return jsonify(data)