from flask import Blueprint, jsonify, render_template
from app import db
from models import Skill, User, Project, Collaboration
from flask_login import login_required

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics')
@login_required
def analytics_page():
    return render_template('analytics.html')


@analytics_bp.route('/api/skill_heatmap')
def skill_heatmap():
    skills = Skill.query.all()
    # sample: return counts per skill
    data = []
    for s in skills:
        count = len(s.__dict__)
        data.append({'skill': s.name, 'count': 0})
    return jsonify(data)
