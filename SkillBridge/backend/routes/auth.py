from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from models import User
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('pages.dashboard'))
        return render_template('auth.html', mode='register')
    data = request.form or request.json
    name, email, password = (data.get('name') or '').strip(), (data.get('email') or '').strip().lower(), data.get('password') or ''
    if not (name and email and password):
        return _auth_error('Name, email, and password are required.', 'auth.register', 400)
    if len(password) < 8:
        return _auth_error('Password must contain at least 8 characters.', 'auth.register', 400)
    if User.query.filter_by(email=email).first():
        return _auth_error('An account already exists for this email. Please sign in.', 'auth.login', 400)
    user = User(name=name, email=email, password_hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
    db.session.add(user)
    db.session.commit()
    login_user(user)
    if request.is_json:
        return jsonify({'message': 'registered'})
    flash('Your account has been created. Welcome to SkillBridge!', 'success')
    return redirect(url_for('pages.dashboard'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('pages.dashboard'))
        return render_template('auth.html', mode='login')
    data = request.form or request.json
    email, password = (data.get('email') or '').strip().lower(), data.get('password') or ''
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return _auth_error('Invalid email or password.', 'auth.login', 401)
    login_user(user)
    if request.is_json:
        return jsonify({'message': 'ok'})
    return redirect(url_for('pages.dashboard'))


def _auth_error(message, endpoint, status):
    if request.is_json:
        return jsonify({'error': message}), status
    flash(message, 'error')
    return redirect(url_for(endpoint))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
