from flask import Blueprint, request, jsonify
from app import db
from models import User, Project, UserSkill
from ml.cdm import compute_cdm
from ml.cf import CFEngine
from flask_login import login_required, current_user
import numpy as np

matching_bp = Blueprint('matching', __name__)


# Simple endpoint to get top 5 matches for a project
@matching_bp.route('/get_matches', methods=['POST'])
@login_required
def get_matches():
    data = request.json or request.form
    project_id = int(data.get('project_id'))
    alpha = float(data.get('alpha', 0.5))
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'project not found'}), 404
    R = project.get_required_vector()
    si = current_user.get_skill_vector()
    G = np.maximum(R - si, 0)  # gap vector (deficits)

    # build CF engine once
    cf = CFEngine(db)

    candidates = User.query.filter(User.id != current_user.id).all()
    results = []
    for u in candidates:
        sj = u.get_skill_vector()
        cdm_score = compute_cdm(si, sj, R, u.trust_score())
        cf_score = cf.predict_score(current_user.id, u.id)
        # dynamic alpha: new users (created < 7 days) 0.7 else 0.4
        days = (current_user.created_at - current_user.created_at).days
        dyn_alpha = 0.7 if days < 7 else 0.4
        final_alpha = dyn_alpha
        final = final_alpha * cdm_score + (1 - final_alpha) * cf_score
        results.append({'user_id': u.id, 'name': u.name, 'cdm': float(cdm_score), 'cf': float(cf_score), 'score': float(final), 'trust': float(u.trust_score()), 'badge': u.trust_badge()})

    results = sorted(results, key=lambda r: r['score'], reverse=True)[:5]
    return jsonify(results)
