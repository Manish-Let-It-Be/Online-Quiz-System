from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    password: str
    role: str

@dataclass
class Category:
    id: Optional[int]
    name: str
    description: str

@dataclass
class Quiz:
    id: Optional[int]
    category_id: int
    title: str
    description: str
    time_limit: int

@dataclass
class Question:
    id: Optional[int]
    quiz_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str

@dataclass
class QuizResult:
    id: Optional[int]
    user_id: int
    quiz_id: int
    score: int
    time_taken: int
    date_taken: datetime