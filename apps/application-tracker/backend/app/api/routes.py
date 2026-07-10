from fastapi import APIRouter
import psycopg

from app.models.email import E_Mail
from app.db.handler import SQLHandler
from app.core.config import DATABASE_URL

router = APIRouter()


@router.post("/api/classify_email")
def classify_email_post(email: E_Mail):
    if email.is_possibly_relevant():
        classification = email.classify()
        with psycopg.connect(DATABASE_URL) as db_connection:
            db_handler = SQLHandler(db_connection)
            db_handler.insert_email(classification)
            return {"classified": "True"}
    return {"classified": "False"}


@router.get("/api/database")
def get_database():
    with psycopg.connect(DATABASE_URL) as db_connection:
        db_handler = SQLHandler(db_connection)
        return db_handler.get_all_emails()


@router.post("/api/save_changes")
def save_changes(df: list[dict]):
    with psycopg.connect(DATABASE_URL) as db_connection:
        db_handler = SQLHandler(db_connection)
        db_handler.save_changes(df)

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/ready")
def ready():
    return {"status": "ready"}