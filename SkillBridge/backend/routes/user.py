from flask import Blueprint, request, jsonify, render_template
from app import db
from models import User, Skill, UserSkill
from flask_login import login_required, current_user
import numpy as np
import json

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    data = request.json or request.form
    # accept skills as list of {skill_id, proficiency, need}
    skills = data.get('skills', [])
    vec = np.zeros(120)
    # persist user skills
    UserSkill.query.filter_by(user_id=current_user.id).delete()
    for s in skills:
        sid = int(s.get('skill_id'))
        prof = int(s.get('proficiency', 0))
        need = bool(s.get('need', False))
        us = UserSkill(user_id=current_user.id, skill_id=sid, proficiency=prof, need=need)
        db.session.add(us)
        if prof > 0:
            idx = sid - 1
            if 0 <= idx < 120:
                vec[idx] = prof
    current_user.set_skill_vector(list(vec))
    current_user.profile_complete = True
    db.session.commit()
    return jsonify({'message': 'profile saved'})


@user_bp.route('/skills', methods=['GET'])
def get_skills():
    from flask import current_app
    try:
        with current_app.app_context():
            skills = Skill.query.all()
            return jsonify([{'id': s.id, 'name': s.name, 'category': s.category} for s in skills])
    except Exception:
        # fallback sample data (prevents 500 if DB not yet initialized)
        sample = [
            {'id': 1, 'name': 'Python', 'category': 'backend'},
            {'id': 2, 'name': 'Machine Learning', 'category': 'ml'},
            {'id': 3, 'name': 'UI Design', 'category': 'design'},
        ]
        return jsonify(sample)
