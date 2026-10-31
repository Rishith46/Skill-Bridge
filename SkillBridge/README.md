# SkillBridge

SkillBridge is a collaboration platform connecting students by complementary skills.

Setup (Windows):

1. Create a Python 3.10+ virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r backend/requirements.txt
```

3. Initialize the database and seed skills:

```powershell
python backend\init_db.py
python database\sample_data.py
```

4. Run the app:

```powershell
python backend\app.py
```

The app serves the frontend templates and API on http://127.0.0.1:5000

Notes:
- Tailwind and Chart.js are loaded via CDN for development.
- This project is scaffolded for SQLite; switch SQLALCHEMY_DATABASE_URI in `backend/app.py` for PostgreSQL in production.
