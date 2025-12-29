from datetime import date

from app.config import QUESTIONS_PER_DAY
from app.persistence.models import Session
from app.persistence.repository import SessionRepository


class SessionManager:

    def __init__(self, repo: SessionRepository):
        self.repo = repo
        self.today = date.today().isoformat()

        self.session = self.repo.get_by_date(self.today)
        if not self.session:
            self.session = Session(date=self.today, answered_count=0, completed=False)
            self.repo.create(self.session)

    def can_continue(self) -> bool:
        return not self.session.completed

    def register_answer(self):
        self.session.answered_count += 1

        if self.session.answered_count >= QUESTIONS_PER_DAY:
            self.session.completed = True

        self.repo.update(self.session)
