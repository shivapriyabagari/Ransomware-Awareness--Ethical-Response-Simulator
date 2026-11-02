from datetime import datetime

from flask import Blueprint, jsonify, request

from models.user import public_user
from simulator.scenarios import (
    get_alerts,
    get_incident_steps,
    get_phishing_emails,
    get_quiz_questions,
    get_scenarios,
)
from utils.helpers import auth_required, generate_id, get_collection

data_bp = Blueprint('data', __name__)


@data_bp.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@data_bp.route('/api/dashboard', methods=['GET'])
@auth_required
def dashboard(user):
    simulations = get_collection('simulation_results')
    results = []
    if hasattr(simulations, 'find'):
        results = list(simulations.find({'user_id': user['_id']}))
    else:
        results = [item for item in simulations if item.get('user_id') == user['_id']]

    quiz_results = get_collection('quiz_results')
    quiz_items = []
    if hasattr(quiz_results, 'find'):
        quiz_items = list(quiz_results.find({'user_id': user['_id']}))
    else:
        quiz_items = [item for item in quiz_results if item.get('user_id') == user['_id']]

    total_simulations = len(results)
    avg_score = round(sum((item.get('score', 0) for item in results), 0) / total_simulations, 1) if total_simulations else 0
    quiz_score = round(sum((item.get('score', 0) for item in quiz_items), 0) / len(quiz_items), 1) if quiz_items else 0

    activities = get_collection('activity_logs')
    activity_list = []
    if hasattr(activities, 'find'):
        activity_list = list(activities.find({'user_id': user['_id']}).sort('timestamp', -1).limit(5))
    else:
        activity_list = [item for item in activities if item.get('user_id') == user['_id']]

    return jsonify({
        'welcome': f'Welcome back, {user.get("name", "Operator")}!',
        'total_simulations_completed': total_simulations,
        'threat_awareness_score': max(0, min(100, round(avg_score if avg_score else 86, 1))),
        'quiz_performance': round(quiz_score if quiz_score else 89, 1),
        'completed_learning_modules': max(3, min(8, total_simulations + len(quiz_items) // 2)),
        'recent_activity': activity_list[:5],
        'learning_progress': [
            {'label': 'Ransomware', 'value': min(100, 60 + total_simulations * 10)},
            {'label': 'Phishing', 'value': min(100, 65 + len(quiz_items) * 4)},
            {'label': 'Incident', 'value': min(100, 50 + total_simulations * 6)},
            {'label': 'Backup', 'value': min(100, 70 + len(quiz_items) * 3)}
        ],
        'recommended_activities': [
            'Review the latest phishing indicators and invalid link patterns.',
            'Complete the backup & recovery module before the next drill.',
            'Analyze the simulated suspicious login alerts in the threat dashboard.'
        ]
    })


@data_bp.route('/api/simulator/scenarios', methods=['GET'])
def scenarios():
    return jsonify({'scenarios': get_scenarios()})


@data_bp.route('/api/simulator/complete', methods=['POST'])
@auth_required
def simulation_complete(user):
    payload = request.get_json(silent=True) or {}
    chosen = payload.get('choice') or {}
    result = {
        '_id': generate_id(),
        'user_id': user['_id'],
        'scenario_id': payload.get('scenarioId'),
        'choice_label': chosen.get('label'),
        'score': chosen.get('score', 0),
        'explanation': chosen.get('explanation', 'Educational review completed.'),
        'completed_at': datetime.utcnow().isoformat() + 'Z',
    }
    collection = get_collection('simulation_results')
    if hasattr(collection, 'insert_one'):
        collection.insert_one(result)
    else:
        collection.append(result)

    log = {
        '_id': generate_id(),
        'user_id': user['_id'],
        'title': 'Simulation completed',
        'description': f"Learner completed a ransomware awareness scenario with score {result['score']}.",
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }
    activity_collection = get_collection('activity_logs')
    if hasattr(activity_collection, 'insert_one'):
        activity_collection.insert_one(log)
    else:
        activity_collection.append(log)

    return jsonify({'status': 'saved', 'result': result})


@data_bp.route('/api/threats', methods=['GET'])
def threats():
    return jsonify({'alerts': get_alerts()})


@data_bp.route('/api/phishing/emails', methods=['GET'])
def phishing_emails():
    return jsonify({'emails': get_phishing_emails()})


@data_bp.route('/api/phishing/submit', methods=['POST'])
@auth_required
def phishing_submit(user):
    payload = request.get_json(silent=True) or {}
    email_id = payload.get('emailId')
    decision = payload.get('decision')
    correct = payload.get('isSuspicious')
    score = 100 if decision == 'suspicious' and correct else 0

    log = {
        '_id': generate_id(),
        'user_id': user['_id'],
        'title': 'Phishing assessment',
        'description': f"Email {email_id} reviewed with result {decision}.",
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }
    activity_collection = get_collection('activity_logs')
    if hasattr(activity_collection, 'insert_one'):
        activity_collection.insert_one(log)
    else:
        activity_collection.append(log)

    return jsonify({'score': score, 'correct': correct})


@data_bp.route('/api/incident/steps', methods=['GET'])
def incident_steps():
    return jsonify({'steps': get_incident_steps()})


@data_bp.route('/api/incident/submit', methods=['POST'])
@auth_required
def incident_submit(user):
    payload = request.get_json(silent=True) or {}
    score = payload.get('score', 100)
    result = {
        '_id': generate_id(),
        'user_id': user['_id'],
        'title': 'Incident response review',
        'score': score,
        'completed_at': datetime.utcnow().isoformat() + 'Z'
    }
    collection = get_collection('simulation_results')
    if hasattr(collection, 'insert_one'):
        collection.insert_one(result)
    else:
        collection.append(result)
    return jsonify({'status': 'saved', 'score': score})


@data_bp.route('/api/backup/status', methods=['GET'])
def backup_status():
    return jsonify({
        'dummyFiles': ['finance-backup.zip', 'hr-archive.tar.gz', 'research-dataset.db'],
        'backupStatus': 'Healthy',
        'lastBackup': '2026-11-02T02:00:00Z',
        'retentionPolicy': '30-day offline retention',
        'recoveryReadiness': 'Ready for demonstration'
    })


@data_bp.route('/api/backup/restore', methods=['POST'])
@auth_required
def backup_restore(user):
    return jsonify({
        'status': 'restored',
        'message': 'The simulated recovery flow completed successfully in the training environment.',
        'recoveredFiles': ['finance-backup.zip', 'hr-archive.tar.gz']
    })


@data_bp.route('/api/quiz/questions', methods=['GET'])
def quiz_questions():
    return jsonify({'questions': get_quiz_questions()})


@data_bp.route('/api/quiz/submit', methods=['POST'])
@auth_required
def quiz_submit(user):
    payload = request.get_json(silent=True) or {}
    answers = payload.get('answers', [])
    questions = get_quiz_questions()
    score = 0
    for item in questions:
        answer_index = next((idx for idx, answer in enumerate(answers) if answer.get('id') == item['id']), None)
        if answer_index is not None:
            provided = answers[answer_index].get('selected')
            if provided == item['answer']:
                score += 1

    percent = round((score / len(questions)) * 100, 1)
    result = {
        '_id': generate_id(),
        'user_id': user['_id'],
        'score': percent,
        'total_questions': len(questions),
        'completed_at': datetime.utcnow().isoformat() + 'Z',
    }
    collection = get_collection('quiz_results')
    if hasattr(collection, 'insert_one'):
        collection.insert_one(result)
    else:
        collection.append(result)

    activity_collection = get_collection('activity_logs')
    activity = {
        '_id': generate_id(),
        'user_id': user['_id'],
        'title': 'Quiz completed',
        'description': f"Quiz score: {percent}%.",
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }
    if hasattr(activity_collection, 'insert_one'):
        activity_collection.insert_one(activity)
    else:
        activity_collection.append(activity)

    return jsonify({'score': percent, 'totalQuestions': len(questions)})


@data_bp.route('/api/reports', methods=['GET'])
@auth_required
def reports(user):
    simulation_collection = get_collection('simulation_results')
    quiz_collection = get_collection('quiz_results')

    simulations = []
    if hasattr(simulation_collection, 'find'):
        simulations = list(simulation_collection.find({'user_id': user['_id']}))
    else:
        simulations = [item for item in simulation_collection if item.get('user_id') == user['_id']]

    quiz_items = []
    if hasattr(quiz_collection, 'find'):
        quiz_items = list(quiz_collection.find({'user_id': user['_id']}))
    else:
        quiz_items = [item for item in quiz_collection if item.get('user_id') == user['_id']]

    total_simulations = len(simulations)
    average_quiz = round(sum((item.get('score', 0) for item in quiz_items), 0) / len(quiz_items), 1) if quiz_items else 0
    module_completion = min(100, 45 + total_simulations * 8 + len(quiz_items) * 4)

    chart_data = [
        {'name': 'Week 1', 'score': 55},
        {'name': 'Week 2', 'score': 68},
        {'name': 'Week 3', 'score': 79},
        {'name': 'Week 4', 'score': average_quiz if average_quiz else 85},
    ]

    return jsonify({
        'totalCompletedSimulations': total_simulations,
        'averageQuizScore': average_quiz,
        'moduleCompletion': round(module_completion, 1),
        'learningProgress': chart_data,
        'recentActivity': [
            {'label': 'Threat detection review', 'value': 'Completed'},
            {'label': 'Phishing awareness drill', 'value': 'Scored 90%'},
            {'label': 'Backup recovery review', 'value': 'Ready'}
        ]
    })


@data_bp.route('/api/profile', methods=['GET'])
@auth_required
def profile(user):
    return jsonify({'user': public_user(user)})
