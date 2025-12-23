from pydantic import BaseModel, Field, ConfigDict, validator
from typing import List, Optional
from datetime import datetime
import uuid
import random
import string

class StudentRegister(BaseModel):
    name: str
    mobile: str
    password: str
    standard: str  # KG, 1, 2, ... 12, BTECH

class StudentLogin(BaseModel):
    username: str
    password: str

class StudentModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    student_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    username: str
    mobile: str
    password_hash: str
    standard: str
    total_credits: int = 0
    level: int = 1
    role: str = "student"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CourseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    course_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    standard: str
    subject: str
    title: str
    description: str
    video_url: str
    duration_minutes: int
    credits: int
    thumbnail: str
    quiz_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class QuizModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    quiz_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    course_id: str
    standard: str
    subject: str
    questions: List[QuizQuestion]
    passing_score: int = 60

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: dict

class ProgressModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    progress_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    course_id: str
    video_completed: bool = False
    watch_duration: int = 0
    quiz_completed: bool = False
    score: int = 0
    credits_earned: int = 0
    completed_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ParentOTPRequest(BaseModel):
    mobile: str

class ParentOTPVerify(BaseModel):
    mobile: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

def generate_username(name: str, existing_usernames: list) -> str:
    base = name.lower().replace(' ', '_')
    base = ''.join(c for c in base if c.isalnum() or c == '_')
    
    while True:
        random_digits = ''.join(random.choices(string.digits, k=3))
        username = f"{base}_{random_digits}"
        if username not in existing_usernames:
            return username
