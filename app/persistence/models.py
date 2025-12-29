# Database schema
from dataclasses import dataclass


@dataclass
class Session:
    date: str
    answered_count: int
    completed: bool


@dataclass
class Answer:
    session_date: str
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool
