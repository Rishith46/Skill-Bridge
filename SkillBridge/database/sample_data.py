"""Create sample users, projects and collaborations for testing."""
import os
import sys

# ensure backend folder is importable when running this script directly
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE, 'backend'))

from app import create_app, db
from models import User, Skill, Project, Collaboration
import bcrypt, json

app = create_app()


def seed_sample():
    with app.app_context():
        # users
        pw = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        u1 = User(name='Alice', email='alice@example.com', password_hash=pw)
        u2 = User(name='Bob', email='bob@example.com', password_hash=pw)
        u3 = User(name='Carol', email='carol@example.com', password_hash=pw)
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        # sample project
        vec = [0] * 120
        vec[0] = 8
        p = Project(owner_id=u1.id, title='ML Project', description='Need data engineer', required_vector=json.dumps(vec))
        db.session.add(p)
        db.session.commit()

        # sample collaboration with rating
        coll = Collaboration(project_id=p.id, requester_id=u1.id, responder_id=u2.id, status='completed', rating=4)
        db.session.add(coll)
        db.session.commit()
        print('sample data seeded')


if __name__ == '__main__':
    seed_sample()
