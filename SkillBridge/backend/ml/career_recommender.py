"""Transparent, local career-role recommendation logic."""
import re


ROLE_CATALOG = [
    {
        "title": "Software Developer",
        "description": "Builds, tests, and maintains web, mobile, or desktop applications.",
        "skills": ["python", "javascript", "programming fundamentals", "git", "databases", "problem solving"],
        "keywords": ["software", "developer", "web", "application", "backend", "frontend", "full stack"],
        "minimum_coding": 2,
    },
    {
        "title": "Frontend Developer",
        "description": "Creates accessible, responsive user interfaces and connects them to product APIs.",
        "skills": ["html", "css", "javascript", "react", "git", "responsive design"],
        "keywords": ["frontend", "ui", "ux", "website", "web design", "react"],
        "minimum_coding": 2,
    },
    {
        "title": "Backend Developer",
        "description": "Designs APIs, databases, and server-side services that power applications.",
        "skills": ["python", "java", "node.js", "sql", "apis", "databases", "git"],
        "keywords": ["backend", "api", "server", "database", "cloud", "systems"],
        "minimum_coding": 3,
    },
    {
        "title": "Data Analyst",
        "description": "Turns data into dashboards, reports, and practical insights for decisions.",
        "skills": ["excel", "sql", "python", "statistics", "data visualization", "power bi"],
        "keywords": ["data", "analytics", "dashboard", "business", "visualization", "insights"],
        "minimum_coding": 1,
    },
    {
        "title": "Data Scientist",
        "description": "Uses data, statistics, and predictive models to solve complex problems.",
        "skills": ["python", "sql", "statistics", "machine learning", "data visualization", "pandas"],
        "keywords": ["data science", "machine learning", "analytics", "prediction", "research", "ai"],
        "minimum_coding": 3,
    },
    {
        "title": "Machine Learning Engineer",
        "description": "Builds, evaluates, and deploys machine-learning systems into products.",
        "skills": ["python", "machine learning", "statistics", "tensorflow", "pytorch", "deployment"],
        "keywords": ["machine learning", "ml", "ai", "deep learning", "models", "automation"],
        "minimum_coding": 4,
    },
    {
        "title": "UI/UX Designer",
        "description": "Researches user needs and designs intuitive, polished digital experiences.",
        "skills": ["figma", "user research", "wireframing", "prototyping", "visual design", "usability testing"],
        "keywords": ["design", "ui", "ux", "users", "figma", "creative", "product"],
        "minimum_coding": 1,
    },
    {
        "title": "QA Automation Engineer",
        "description": "Improves software quality by designing test plans and automated test suites.",
        "skills": ["python", "javascript", "testing", "selenium", "apis", "git"],
        "keywords": ["testing", "quality", "qa", "automation", "bugs", "reliability"],
        "minimum_coding": 2,
    },
]

CODING_LEVELS = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}


def _terms(value):
    return set(re.findall(r"[a-z0-9+#.]+", (value or "").lower()))


def _has_skill(skill, profile_text, profile_terms):
    skill_terms = _terms(skill)
    return skill.lower() in profile_text or skill_terms.issubset(profile_terms)


def recommend(skills, coding_knowledge, interests="", project_text=""):
    """Return five ranked roles plus the skills still needed for each role."""
    profile_text = " ".join([skills or "", interests or "", project_text or ""]).lower()
    profile_terms = _terms(profile_text)
    coding_level = CODING_LEVELS.get((coding_knowledge or "").lower(), 1)
    results = []

    for role in ROLE_CATALOG:
        matching = [skill for skill in role["skills"] if _has_skill(skill, profile_text, profile_terms)]
        missing = [skill for skill in role["skills"] if skill not in matching]
        interest_matches = sum(1 for keyword in role["keywords"] if keyword in profile_text)
        coding_fit = 1 if coding_level >= role["minimum_coding"] else max(0, 1 - (role["minimum_coding"] - coding_level) * 0.25)
        # Skills carry most weight; stated interests and project evidence refine the ranking.
        score = (len(matching) / len(role["skills"])) * 65 + min(interest_matches, 4) * 8 + coding_fit * 3
        results.append({
            "title": role["title"],
            "description": role["description"],
            "skills_needed": role["skills"],
            "matching_skills": matching,
            "learn": missing,
            "match_score": round(min(score, 99)),
        })

    return sorted(results, key=lambda item: item["match_score"], reverse=True)[:5]
