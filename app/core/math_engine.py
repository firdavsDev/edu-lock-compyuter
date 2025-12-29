# Savol generator (Question generator)
import random

from app.config import MAX_NUMBER, MIN_NUMBER


class MathQuestion:
    def __init__(self, text: str, correct_answer: int):
        self.text = text
        self.correct_answer = correct_answer


class MathEngine:

    def generate(self) -> MathQuestion:
        a = random.randint(MIN_NUMBER, MAX_NUMBER)
        b = random.randint(MIN_NUMBER, MAX_NUMBER)
        op = random.choice(["+", "-", "*", "/"])

        if op == "/":
            a = a * b  # Ensure divisibility

        expression = f"{a} {op} {b}"
        correct = int(eval(expression))

        return MathQuestion(expression, correct)

    def check(self, question: MathQuestion, user_answer: str) -> bool:
        try:
            return int(user_answer) == question.correct_answer
        except ValueError:
            return False
