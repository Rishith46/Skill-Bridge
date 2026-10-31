from flask import Blueprint, request, jsonify, render_template
from app import db
from models import Project, User
from flask_login import login_required, current_user
import numpy as np
import json

project_bp = Blueprint('project', __name__)


@project_bp.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'GET':
        return render_template('projects.html')
    data = request.json or request.form
    title = data.get('title')
    description = data.get('description', '')
    required = data.get('required', [])
    vec = np.zeros(120)
    for r in required:
        sid = int(r.get('skill_id'))
        level = int(r.get('level', 0))
        idx = sid - 1
        if 0 <= idx < 120:
            vec[idx] = level
    p = Project(owner_id=current_user.id, title=title, description=description, required_vector=json.dumps(list(vec)))
    db.session.add(p)
    db.session.commit()
    return jsonify({'message': 'project_created', 'project_id': p.id})


@project_bp.route('/get_projects')
def get_projects():
    ps = Project.query.all()
    out = []
    for p in ps:
        out.append({'id': p.id, 'title': p.title, 'description': p.description, 'status': p.status})
    return jsonify(out)
