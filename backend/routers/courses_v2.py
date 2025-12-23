from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from models_v2 import CourseModel, QuizModel, QuizSubmission, ProgressModel
from routers.auth_v2 import get_current_student
from datetime import datetime
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("")
async def get_my_courses(current_student: dict = Depends(get_current_student)):
    student_standard = current_student["standard"]
    
    courses = await db.courses.find(
        {"standard": student_standard},
        {"_id": 0}
    ).to_list(100)
    
    progress_list = await db.progress.find(
        {"student_id": current_student["student_id"]},
        {"_id": 0}
    ).to_list(100)
    
    progress_map = {p["course_id"]: p for p in progress_list}
    
    for course in courses:
        course["progress"] = progress_map.get(course["course_id"], None)
    
    return courses

@router.get("/{course_id}")
async def get_course(course_id: str, current_student: dict = Depends(get_current_student)):
    course = await db.courses.find_one({"course_id": course_id}, {"_id": 0})
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course["standard"] != current_student["standard"]:
        raise HTTPException(status_code=403, detail="Access denied: Course not for your standard")
    
    progress = await db.progress.find_one({
        "student_id": current_student["student_id"],
        "course_id": course_id
    }, {"_id": 0})
    
    if not progress:
        new_progress = ProgressModel(
            student_id=current_student["student_id"],
            course_id=course_id
        )
        progress_dict = new_progress.model_dump()
        progress_dict["updated_at"] = progress_dict["updated_at"].isoformat()
        await db.progress.insert_one(progress_dict)
        progress = progress_dict
    
    course["progress"] = progress
    return course

@router.post("/complete-video/{course_id}")
async def complete_video(course_id: str, watch_duration: int, current_student: dict = Depends(get_current_student)):
    course = await db.courses.find_one({"course_id": course_id}, {"_id": 0})
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course["standard"] != current_student["standard"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    video_completed = watch_duration >= (course["duration_minutes"] * 0.9)
    
    await db.progress.update_one(
        {"student_id": current_student["student_id"], "course_id": course_id},
        {"$set": {
            "video_completed": video_completed,
            "watch_duration": watch_duration,
            "updated_at": datetime.utcnow().isoformat()
        }},
        upsert=True
    )
    
    return {"video_completed": video_completed, "quiz_unlocked": video_completed}

@router.get("/quiz/{course_id}")
async def get_quiz(course_id: str, current_student: dict = Depends(get_current_student)):
    course = await db.courses.find_one({"course_id": course_id}, {"_id": 0})
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course["standard"] != current_student["standard"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    progress = await db.progress.find_one({
        "student_id": current_student["student_id"],
        "course_id": course_id
    }, {"_id": 0})
    
    if not progress or not progress.get("video_completed"):
        raise HTTPException(status_code=400, detail="Complete video first")
    
    quiz = await db.quizzes.find_one({"course_id": course_id}, {"_id": 0})
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return quiz

@router.post("/submit-quiz")
async def submit_quiz(submission: QuizSubmission, current_student: dict = Depends(get_current_student)):
    quiz = await db.quizzes.find_one({"quiz_id": submission.quiz_id}, {"_id": 0})
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    course = await db.courses.find_one({"course_id": quiz["course_id"]}, {"_id": 0})
    
    if course["standard"] != current_student["standard"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    correct_answers = 0
    total_questions = len(quiz["questions"])
    
    for question in quiz["questions"]:
        q_text = question["question"]
        if submission.answers.get(q_text) == question["correct_answer"]:
            correct_answers += 1
    
    score = int((correct_answers / total_questions) * 100)
    passed = score >= quiz["passing_score"]
    credits_earned = course["credits"] if passed else 0
    
    await db.progress.update_one(
        {"student_id": current_student["student_id"], "course_id": quiz["course_id"]},
        {"$set": {
            "quiz_completed": True,
            "score": score,
            "credits_earned": credits_earned,
            "completed_at": datetime.utcnow().isoformat() if passed else None,
            "updated_at": datetime.utcnow().isoformat()
        }}
    )
    
    if passed:
        new_credits = current_student.get("total_credits", 0) + credits_earned
        new_level = (new_credits // 500) + 1
        
        await db.students.update_one(
            {"student_id": current_student["student_id"]},
            {"$set": {
                "total_credits": new_credits,
                "level": new_level
            }}
        )
    
    return {
        "score": score,
        "total": 100,
        "passed": passed,
        "credits_earned": credits_earned,
        "correct_answers": correct_answers,
        "total_questions": total_questions
    }

@router.get("/stats")
async def get_stats(current_student: dict = Depends(get_current_student)):
    progress_list = await db.progress.find(
        {"student_id": current_student["student_id"]},
        {"_id": 0}
    ).to_list(100)
    
    completed_courses = sum(1 for p in progress_list if p.get("quiz_completed"))
    total_courses = await db.courses.count_documents({"standard": current_student["standard"]})
    
    return {
        "name": current_student["name"],
        "username": current_student["username"],
        "standard": current_student["standard"],
        "total_credits": current_student.get("total_credits", 0),
        "level": current_student.get("level", 1),
        "completed_courses": completed_courses,
        "total_courses": total_courses,
        "progress_percentage": int((completed_courses / total_courses * 100)) if total_courses > 0 else 0
    }
