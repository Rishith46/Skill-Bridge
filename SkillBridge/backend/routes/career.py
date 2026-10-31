from io import BytesIO

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required

from ml.career_recommender import CODING_LEVELS, recommend


career_bp = Blueprint("career", __name__)
ALLOWED_DOCUMENTS = {"txt", "md", "pdf", "docx"}
MAX_DOCUMENT_SIZE = 5 * 1024 * 1024


def extract_project_text(upload):
    """Extract a limited amount of text from an optional project document."""
    if not upload or not upload.filename:
        return ""
    extension = upload.filename.rsplit(".", 1)[-1].lower() if "." in upload.filename else ""
    if extension not in ALLOWED_DOCUMENTS:
        raise ValueError("Upload a .txt, .md, .pdf, or .docx project document.")
    content = upload.read(MAX_DOCUMENT_SIZE + 1)
    if len(content) > MAX_DOCUMENT_SIZE:
        raise ValueError("Project documents must be 5 MB or smaller.")
    if extension in {"txt", "md"}:
        return content.decode("utf-8", errors="ignore")[:20000]
    if extension == "pdf":
        from pypdf import PdfReader
        return " ".join(page.extract_text() or "" for page in PdfReader(BytesIO(content)).pages)[:20000]
    from docx import Document
    return " ".join(p.text for p in Document(BytesIO(content)).paragraphs)[:20000]


@career_bp.route("/career")
@login_required
def career_page():
    return render_template("career.html")


@career_bp.route("/api/career-recommendations", methods=["POST"])
@login_required
def career_recommendations():
    skills = (request.form.get("skills") or "").strip()
    coding_knowledge = (request.form.get("coding_knowledge") or "").strip().lower()
    interests = (request.form.get("interests") or "").strip()
    if not skills or coding_knowledge not in CODING_LEVELS:
        return jsonify({"error": "Skills and coding knowledge are required."}), 400
    try:
        project_text = extract_project_text(request.files.get("project_document"))
    except (ValueError, ImportError, OSError) as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"recommendations": recommend(skills, coding_knowledge, interests, project_text)})
