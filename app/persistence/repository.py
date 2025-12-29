# CRUD operations
from app.persistence.db import Database
from app.persistence.models import Answer, Session


class SessionRepository:

    def get_by_date(self, date: str) -> Session | None:
        conn = Database.connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM sessions WHERE date = ?", (date,))
        row = cur.fetchone()

        if not row:
            return None

        return Session(
            date=row["date"],
            answered_count=row["answered_count"],
            completed=bool(row["completed"]),
        )

    def create(self, session: Session):
        conn = Database.connect()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO sessions VALUES (?, ?, ?)",
            (session.date, session.answered_count, int(session.completed)),
        )
        conn.commit()

    def update(self, session: Session):
        conn = Database.connect()
        cur = conn.cursor()

        cur.execute(
            """
        UPDATE sessions
        SET answered_count = ?, completed = ?
        WHERE date = ?
        """,
            (session.answered_count, int(session.completed), session.date),
        )

        conn.commit()


class AnswerRepository:

    def save(self, answer: Answer):
        conn = Database.connect()
        cur = conn.cursor()

        cur.execute(
            """
        INSERT INTO answers
        (session_date, question, user_answer, correct_answer, is_correct)
        VALUES (?, ?, ?, ?, ?)
        """,
            (
                answer.session_date,
                answer.question,
                answer.user_answer,
                answer.correct_answer,
                int(answer.is_correct),
            ),
        )

        conn.commit()
