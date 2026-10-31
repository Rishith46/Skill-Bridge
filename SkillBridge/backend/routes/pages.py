from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required
import os

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    return render_template('index.html')


@pages_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@pages_bp.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')


@pages_bp.route('/create_project')
@login_required
def create_project_page():
    return render_template('create_project.html')


@pages_bp.route('/matches')
@login_required
def matches_page():
    return render_template('matches.html')


@pages_bp.route('/hub')
@login_required
def hub_page():
    return render_template('hub.html')


@pages_bp.route('/favicon.ico')
def favicon():
    # return 204 to avoid file not found logs, or serve a placeholder if available
    return ('', 204)
