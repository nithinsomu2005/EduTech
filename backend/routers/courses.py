from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from models import Course, CourseCreate, Quiz, QuizCreate
from routers.auth import get_current_user
from typing import List
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("", response_model=List[Course])
async def get_courses(grade_level: str = None, subject: str = None):
    query = {}
    if grade_level:
        query["grade_level"] = grade_level
    if subject:
        query["subject"] = subject
    
    courses = await db.courses.find(query, {"_id": 0}).sort("order", 1).to_list(100)
    return courses

@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: str):
    course = await db.courses.find_one({"course_id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/{course_id}/quiz", response_model=Quiz)
async def get_course_quiz(course_id: str):
    quiz = await db.quizzes.find_one({"course_id": course_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found for this course")
    return quiz

@router.post("", response_model=Course)
async def create_course(course: CourseCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    course_obj = Course(**course.model_dump(), created_by=current_user["user_id"])
    course_dict = course_obj.model_dump()
    course_dict["created_at"] = course_dict["created_at"].isoformat()
    
    await db.courses.insert_one(course_dict)
    return course_obj

@router.post("/quiz", response_model=Quiz)
async def create_quiz(quiz: QuizCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    course = await db.courses.find_one({"course_id": quiz.course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    quiz_obj = Quiz(**quiz.model_dump())
    quiz_dict = quiz_obj.model_dump()
    quiz_dict["created_at"] = quiz_dict["created_at"].isoformat()
    
    await db.quizzes.insert_one(quiz_dict)
    return quiz_obj
