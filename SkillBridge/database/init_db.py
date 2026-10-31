"""Initialize the SQLite database and seed skills."""
import os
import sys

# ensure backend folder is importable when running this script directly
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE, 'backend'))

from app import create_app, db
from models import Skill

app = create_app()


def seed_skills():
    categories = ['Programming', 'Data', 'Design', 'DevOps']
    with app.app_context():
        # create 120 example skills
        for i in range(1, 121):
            name = f"Skill {i}"
            s = Skill(name=name, category=categories[i % len(categories)])
            db.session.add(s)
        db.session.commit()
        print('seeded skills')


if __name__ == '__main__':
    seed_skills()
