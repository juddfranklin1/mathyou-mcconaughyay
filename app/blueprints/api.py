from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
import logging
import uuid
import os
import random
import google.generativeai as genai
from app.models import Subject, Concept, Question, UserResponse
from app.extensions import db

api_bp = Blueprint('api', __name__)

# --- Caching ---
OVERVIEW_CACHE = {}
GENERATED_QUESTION_CACHE = {}

# --- Gemini Configuration & System Prompt ---

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

CANDIDATE_MODELS = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.0-pro', 'gemini-pro']

GENERATION_CONFIG = {
    "temperature": 0.9,
    "top_p": 0.8,
    "top_k": 60,
}

MATHYOU_TEACHER_PERSONA = """
You are a patient, friendly, and relatable math teacher - played by Matthew MacConaughey. You have had 2 beers and your ex-wife just called from a roadtrip through various Mexican coastal towns. She's always talking about a different one, talking about some amazing resort feature or an incredible beach, or a very muscular and intelligent man she seems to be very intimate with. And it's a bit humiliating. Somehow, her calls always come in while you're stuck in traffic on a different highway or surface street in Los Angeles. Most of your lessons are provided while you are relaxing at the end of the day in your one-bedroom apartment overlooking the 405 freeway. You are feeling philosophical, but the math is the only thing bringing you joy and clarity under the circumstances. Even if you are a little sad. Because you are Matthew, you rise above all that like a boat with a tailwind. Your commitment to accuracy and quality explanations in math is unwavering, even though you weave in some details about your wife's trip and your daily drives through LA traffic. You know a lot about different professions, because as an actor you have played pretty much everything. With this in mind, your explanations always contain a very clear and cogent example from a real profession in the real world.
"""

TEACHER_PERSONA_PROMPT = """
{persona}
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

OVERVIEW_PROMPT = """
{persona}
Your task is to generate a welcome overview for a student studying {discipline}.

Student Context:
- Has the student solved problems before? {has_history}
- Number of problems solved in this discipline: {solved_count}
- Concepts recently worked on: {recent_concepts}

Instructions:
1. If the student has solved problems (Has history: Yes):
   - Welcome them back.
   - Mention what they have already accomplished (referencing the concepts).
2. If the student is new (Has history: No):
   - Welcome them.
   - Invite them to try one of the concepts on the sidebar.
3. In all cases:
   - Include a riff about the right attitude to take to master {discipline}.
   - Provide a concrete example of how and why it will be useful to know {discipline} in the real world.

Tone and Style:
- Don't be afraid to be brusque, and sarcastic. You can even be a bit harsh, but only in a playful, punk rock way.
- Keep the response concise (under 200 words).
"""

def get_ai_feedback(question, user_answer, is_correct):
    """Generates custom feedback using Gemini based on the user's answer."""
    if not GEMINI_API_KEY:
        return None

    try:
        problem_text = question.problem_text
        correct_val = question.data.get('answer')
        user_val = user_answer

        if question.data.get('type') == 'multiple_choice':
            choices = question.data.get('choices', [])
            problem_text += "\nChoices: " + ", ".join([f"({i}) {c}" for i, c in enumerate(choices)])
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
            persona=MATHYOU_TEACHER_PERSONA,
            problem_text=problem_text,
            correct_answer=correct_val,
            user_answer=user_val,
            is_correct="Yes" if is_correct else "No"
        )

        for model_name in CANDIDATE_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt, generation_config=GENERATION_CONFIG)
                return response.text
            except Exception as e:
                logging.warning(f"Model {model_name} failed: {e}")
                continue
        return None
    except Exception as e:
        logging.error(f"Error generating AI feedback: {e}")
        return None

@api_bp.route('/overview')
def api_overview():
    subject_slug = request.args.get('discipline')
    if not subject_slug:
        return jsonify({'error': 'Discipline is required'}), 400
    
    subject = Subject.query.filter_by(slug=subject_slug).first()
    if not subject:
        return jsonify({'error': 'Discipline not found'}), 404

    solved_count = 0
    recent_concepts = []
    has_history = "No"

    if current_user.is_authenticated:
        # Join UserResponse -> Question -> Concept to filter by subject
        responses = UserResponse.query.join(Question).join(Concept).filter(
            UserResponse.user_id == current_user.id,
            UserResponse.is_correct == True,
            Concept.subject_id == subject.id
        ).all()
        
        solved_count = len(responses)
        if solved_count > 0:
            has_history = "Yes"
            # Get unique recent concepts
            concept_names = {r.question.concept.name for r in responses}
            recent_concepts = list(concept_names)[:3]

    # Check cache
    user_key = current_user.id if current_user.is_authenticated else 'anon'
    cache_key = f"{user_key}:{subject.id}:{solved_count}:{'-'.join(sorted(recent_concepts))}"
    if cache_key in OVERVIEW_CACHE:
        return jsonify({'overview': OVERVIEW_CACHE[cache_key]})

    prompt = OVERVIEW_PROMPT.format(
        persona=MATHYOU_TEACHER_PERSONA,
        discipline=subject.name,
        has_history=has_history,
        solved_count=solved_count,
        recent_concepts=", ".join(recent_concepts) if recent_concepts else "None"
    )

    if not GEMINI_API_KEY:
         return jsonify({'overview': f"Welcome to {subject.name}. (AI generation unavailable)"})

    for model_name in CANDIDATE_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt, generation_config=GENERATION_CONFIG)
            overview_text = response.text
            OVERVIEW_CACHE[cache_key] = overview_text
            return jsonify({'overview': overview_text})
        except Exception as e:
            logging.warning(f"Model {model_name} failed: {e}")
            continue
    return jsonify({'overview': f"Welcome to {subject.name}. Let's get started."})

@api_bp.route('/concept')
def api_concept():
    subject_slug = request.args.get('discipline')
    concept_slug = request.args.get('concept')
    concept = Concept.query.join(Subject).filter(
        Subject.slug == subject_slug,
        Concept.slug == concept_slug
    ).first()
    if not concept:
        return jsonify({'error': 'Concept not found'}), 404
    return jsonify({
        'name': concept.name,
        'formula': concept.formula,
        'explanation': concept.explanation,
        'core_idea': concept.core_idea,
        'real_world_application': concept.real_world_application,
        'mathematical_demonstration': concept.mathematical_demonstration,
        'study_plan': concept.study_plan,
        'questions': [q.legacy_id for q in concept.questions]
    })

@api_bp.route('/question/<string:legacy_id>')
def api_question(legacy_id):
    if legacy_id.startswith('gemini_trigger_'):
        if legacy_id in GENERATED_QUESTION_CACHE:
            return jsonify(GENERATED_QUESTION_CACHE[legacy_id])

        concept_slug = legacy_id.replace('gemini_trigger_', '')
        concept = Concept.query.filter_by(slug=concept_slug).first()
        concept_name = concept.name if concept else concept_slug.replace('-', ' ')
        prompt = f"Provide a real-world example of a math problem that demonstrates the concept of {concept_name}. The output should be a practical scenario followed by a question, but do not provide the answer immediately. Format it as a practice problem."
        ai_content = "This concept is mastered! Here is a real-world application..."
        success = False
        for model_name in CANDIDATE_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt, generation_config=GENERATION_CONFIG)
                ai_content = response.text
                success = True
                break
            except Exception as e:
                logging.warning(f"Model {model_name} failed: {e}")
                continue
        
        if not success:
            ai_content = f"Great job! You've mastered {concept_name}. Try applying this to real-world physics or engineering problems."

        response_data = {
            'id': legacy_id,
            'problem': ai_content,
            'difficulty': 'Real World Application',
            'explanation': 'This is an advanced application of the concept you have mastered.',
            'type': 'numerical',
            'answer': '0'
        }
        GENERATED_QUESTION_CACHE[legacy_id] = response_data
        return jsonify(response_data)

    current_app.logger.info(f"API request received for question with legacy_id: '{legacy_id}'")
    question = Question.query.filter_by(legacy_id=legacy_id).first_or_404()
    response_data = {
        'id': question.legacy_id,
        'problem': question.problem_text,
        'difficulty': question.difficulty,
        'explanation': question.explanation,
    }
    response_data.update(question.data)
    return jsonify(response_data)

@api_bp.route('/question/next')
def next_question():
    current_legacy_id = request.args.get('current_id')
    if not current_legacy_id:
        return jsonify({'error': 'current_id required'}), 400
    
    current_q = Question.query.filter_by(legacy_id=current_legacy_id).first_or_404()
    
    # Find candidates with same concept and difficulty, excluding the current one
    candidates = Question.query.filter_by(
        concept_id=current_q.concept_id,
        difficulty=current_q.difficulty
    ).filter(Question.id != current_q.id).all()
    
    next_q = random.choice(candidates) if candidates else current_q
        
    response_data = {
        'id': next_q.legacy_id,
        'problem': next_q.problem_text,
        'difficulty': next_q.difficulty,
        'explanation': next_q.explanation,
    }
    response_data.update(next_q.data)
    return jsonify(response_data)

@api_bp.route('/question/schema', methods=['GET'])
def get_question_schema():
    """Returns the documentation and schema for creating a new question."""
    return jsonify({
        "endpoint": "/api/question/create",
        "method": "POST",
        "description": "Creates a new practice question in the database.",
        "authentication": "Session cookie OR 'X-API-Key' header matching ADMIN_API_KEY env var.",
        "payload_schema": {
            "subject_slug": "string (Required, e.g., 'trigonometry')",
            "concept_slug": "string (Required, e.g., 'unit-circle')",
            "problem_text": "string (Required, supports LaTeX)",
            "difficulty": "string (Optional, default 'Medium')",
            "explanation": "string (Optional)",
            "data": {
                "type": "string ('multiple_choice' or 'numerical')",
                "choices": ["string", "string"] + " (Required if type is multiple_choice)",
                "answer": "string or int (Correct answer value or index)"
            },
            "legacy_id": "string (Optional, must be unique)"
        }
    })

@api_bp.route('/question/create', methods=['POST'])
def create_question():
    # Allow access via session (human) or API Key (agent)
    api_key = request.headers.get('X-API-Key')
    admin_key = os.environ.get('ADMIN_API_KEY')
    if not current_user.is_authenticated and (not admin_key or api_key != admin_key):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    subject_slug = data.get('subject_slug')
    concept_slug = data.get('concept_slug')
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

@api_bp.route('/question/submit_answer', methods=['POST'])
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
    correct_answer = question.data.get('answer')
    is_correct = str(user_answer).strip() == str(correct_answer).strip()
    response = UserResponse(
        user_id=current_user.id,
        question_id=question.id,
        response_data={'answer': user_answer},
        is_correct=is_correct
    )
    db.session.add(response)
    db.session.commit()
    ai_explanation = get_ai_feedback(question, user_answer, is_correct)
    
    if ai_explanation:
        # Store the generated feedback in the response data for persistence
        updated_data = response.response_data.copy() if response.response_data else {}
        updated_data['ai_explanation'] = ai_explanation
        response.response_data = updated_data
        db.session.commit()

    final_explanation = ai_explanation if ai_explanation else question.explanation
    return jsonify({
        'correct': is_correct,
        'explanation': final_explanation
    })