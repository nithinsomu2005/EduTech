from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

class UserBase(BaseModel):
    institution_id: str
    email: EmailStr
    full_name: str
    mobile: str
    role: str

class UserCreate(UserBase):
    password: str
    grade: Optional[str] = None
    stream: Optional[str] = None

class User(UserBase):
    model_config = ConfigDict(extra="ignore")
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = True
    profile_image: Optional[str] = None

class UserLogin(BaseModel):
    institution_id: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class ParentOTPRequest(BaseModel):
    mobile: str

class ParentOTPVerify(BaseModel):
    mobile: str
    otp: str

class StudentBase(BaseModel):
    user_id: str
    grade: str
    grade_year: int
    stream: Optional[str] = None
    parent_mobile: str
    institution_name: str
    dob: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    model_config = ConfigDict(extra="ignore")
    student_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    total_credits: int = 0
    level: int = 1
    placement_readiness: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CourseBase(BaseModel):
    title: str
    grade_level: str
    subject: str
    video_url: str
    duration_minutes: int
    credits: int
    description: str
    thumbnail: str
    order: int = 0

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    model_config = ConfigDict(extra="ignore")
    course_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    marks: int = 1

class QuizBase(BaseModel):
    course_id: str
    title: str
    questions: List[QuestionBase]
    passing_marks: int
    total_marks: int

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    model_config = ConfigDict(extra="ignore")
    quiz_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: dict

class ProgressBase(BaseModel):
    student_id: str
    course_id: str

class ProgressUpdate(BaseModel):
    video_completed: Optional[bool] = None
    watch_duration: Optional[int] = None

class Progress(ProgressBase):
    model_config = ConfigDict(extra="ignore")
    progress_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    video_completed: bool = False
    watch_duration: int = 0
    quiz_attempts: int = 0
    quiz_passed: bool = False
    quiz_score: int = 0
    credits_earned: int = 0
    completed_at: Optional[datetime] = None
    last_accessed: datetime = Field(default_factory=datetime.utcnow)

class Badge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    badge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    icon: str
    criteria: dict
    rarity: str

class StudentBadge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    student_id: str
    badge_id: str
    earned_at: datetime = Field(default_factory=datetime.utcnow)

class Certificate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    certificate_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    course_id: str
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    certificate_url: str

class Resource(BaseModel):
    model_config = ConfigDict(extra="ignore")
    resource_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    grade_level: str
    type: str
    title: str
    subject: str
    url: str
    thumbnail: str
    year: Optional[int] = None
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Challenge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    challenge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    grade_levels: List[str]
    credits_reward: int
    type: str
    difficulty: str

class CareerRoadmap(BaseModel):
    model_config = ConfigDict(extra="ignore")
    roadmap_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    skills: List[str]
    milestones: List[dict]
    job_roles: List[str]
    avg_salary: str
