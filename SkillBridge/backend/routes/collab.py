from flask import Blueprint, request, jsonify
from app import db
from models import Collaboration, Project, User
from flask_login import login_required, current_user

collab_bp = Blueprint('collab', __name__)


@collab_bp.route('/request', methods=['POST'])
@login_required
def request_collab():
    data = request.json or request.form
    project_id = int(data.get('project_id'))
    responder_id = int(data.get('responder_id'))
    coll = Collaboration(project_id=project_id, requester_id=current_user.id, responder_id=responder_id, status='pending')
    db.session.add(coll)
    db.session.commit()
    return jsonify({'message': 'request_sent', 'id': coll.id})


@collab_bp.route('/accept', methods=['POST'])
@login_required
def accept():
    data = request.json or request.form
    collab_id = int(data.get('id'))
    coll = Collaboration.query.get(collab_id)
    if not coll:
        return jsonify({'error': 'not found'}), 404
    if coll.responder_id != current_user.id:
        return jsonify({'error': 'not authorized'}), 403
    coll.status = 'active'
    db.session.commit()
    return jsonify({'message': 'accepted'})


@collab_bp.route('/complete', methods=['POST'])
@login_required
def complete():
    data = request.json or request.form
    collab_id = int(data.get('id'))
    rating = int(data.get('rating', 0))
    coll = Collaboration.query.get(collab_id)
    if not coll:
        return jsonify({'error': 'not found'}), 404
    coll.status = 'completed'
    coll.rating = rating
    # update responder stats
    user = User.query.get(coll.responder_id)
    if user:
        # simple running average
        if user.avg_rating is None:
            user.avg_rating = rating
        else:
            user.avg_rating = (user.avg_rating + rating) / 2.0
        user.completion_rate = min(1.0, user.completion_rate + 0.1)
    db.session.commit()
    return jsonify({'message': 'completed'})


@collab_bp.route('/rate', methods=['POST'])
@login_required
def rate():
    data = request.json or request.form
    collab_id = int(data.get('id'))
    rating = int(data.get('rating', 0))
    coll = Collaboration.query.get(collab_id)
    if not coll:
        return jsonify({'error': 'not found'}), 404
    coll.rating = rating
    # update responder stats
    user = User.query.get(coll.responder_id)
    if user:
        if user.avg_rating is None:
            user.avg_rating = rating
        else:
            user.avg_rating = (user.avg_rating + rating) / 2.0
    db.session.commit()
    return jsonify({'message': 'rated'})
