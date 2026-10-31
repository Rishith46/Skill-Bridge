from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import sys

# Routes import the extension as ``from app import db``.  Keeping this alias
# prevents Flask's module loader from importing this file a second time as
# ``app`` (which would otherwise create a different SQLAlchemy instance).
sys.modules.setdefault('app', sys.modules[__name__])

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'skillbridge.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # user loader required by flask-login
    @login_manager.user_loader
    def load_user(user_id):
        try:
            from models import User
            return User.query.get(int(user_id))
        except Exception:
            return None

    # register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.project import project_bp
    from routes.matching import matching_bp
    from routes.collab import collab_bp
    from routes.analytics import analytics_bp
    from routes.pages import pages_bp
    from routes.career import career_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(collab_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(career_bp)

    # create DB file if missing
    with app.app_context():
        from models import User, Skill, UserSkill, Project, Collaboration
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
