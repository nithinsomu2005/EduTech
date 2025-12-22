from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from models import Progress, ProgressUpdate, QuizSubmission
from routers.auth import get_current_user
from datetime import datetime
from typing import List
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.post("/start")
async def start_course(course_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can start courses")
    
    student = await db.students.find_one({"user_id": current_user["user_id"]}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    course = await db.courses.find_one({"course_id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    existing = await db.progress.find_one({
        "student_id": student["student_id"],
        "course_id": course_id
    }, {"_id": 0})
    
    if existing:
        return {"message": "Course already started", "progress": existing}
    
    progress = Progress(student_id=student["student_id"], course_id=course_id)
    progress_dict = progress.model_dump()
    progress_dict["last_accessed"] = progress_dict["last_accessed"].isoformat()
    if progress_dict.get("completed_at"):
        progress_dict["completed_at"] = progress_dict["completed_at"].isoformat()
    
    await db.progress.insert_one(progress_dict)
    return {"message": "Course started", "progress": progress_dict}

@router.put("/video-complete")
async def complete_video(course_id: str, watch_duration: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can update progress")
    
    student = await db.students.find_one({"user_id": current_user["user_id"]}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    course = await db.courses.find_one({"course_id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    progress = await db.progress.find_one({
        "student_id": student["student_id"],
        "course_id": course_id
    }, {"_id": 0})
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found. Start the course first.")
    
    video_completed = watch_duration >= (course["duration_minutes"] * 0.9)
    
    await db.progress.update_one(
        {"student_id": student["student_id"], "course_id": course_id},
        {"$set": {
            "video_completed": video_completed,
            "watch_duration": watch_duration,
            "last_accessed": datetime.utcnow().isoformat()
        }}
    )
    
    return {
        "message": "Video progress updated",
        "video_completed": video_completed,
        "quiz_unlocked": video_completed
    }

@router.post("/submit-quiz")
async def submit_quiz(submission: QuizSubmission, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can submit quizzes")
    
    student = await db.students.find_one({"user_id": current_user["user_id"]}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    quiz = await db.quizzes.find_one({"quiz_id": submission.quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    progress = await db.progress.find_one({
        "student_id": student["student_id"],
        "course_id": quiz["course_id"]
    }, {"_id": 0})
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    if not progress.get("video_completed"):
        raise HTTPException(status_code=400, detail="Complete the video first")
    
    score = 0
    for question in quiz["questions"]:
        question_id = question["question"]
        if submission.answers.get(question_id) == question["correct_answer"]:
            score += question["marks"]
    
    quiz_passed = score >= quiz["passing_marks"]
    
    course = await db.courses.find_one({"course_id": quiz["course_id"]}, {"_id": 0})
    credits_earned = course["credits"] if quiz_passed else 0
    
    await db.progress.update_one(
        {"student_id": student["student_id"], "course_id": quiz["course_id"]},
        {"$set": {
            "quiz_attempts": progress.get("quiz_attempts", 0) + 1,
            "quiz_passed": quiz_passed,
            "quiz_score": score,
            "credits_earned": credits_earned,
            "completed_at": datetime.utcnow().isoformat() if quiz_passed else None,
            "last_accessed": datetime.utcnow().isoformat()
        }}
    )
    
    if quiz_passed:
        new_credits = student.get("total_credits", 0) + credits_earned
        new_level = (new_credits // 500) + 1
        
        await db.students.update_one(
            {"student_id": student["student_id"]},
            {"$set": {
                "total_credits": new_credits,
                "level": new_level
            }}
        )
        
        await check_and_award_badges(student["student_id"], new_credits, new_level)
    
    return {
        "score": score,
        "total": quiz["total_marks"],
        "passed": quiz_passed,
        "credits_earned": credits_earned,
        "message": "Congratulations! You passed!" if quiz_passed else "Keep trying!"
    }

async def check_and_award_badges(student_id: str, total_credits: int, level: int):
    badges = await db.badges.find({}, {"_id": 0}).to_list(100)
    
    for badge in badges:
        already_earned = await db.student_badges.find_one({
            "student_id": student_id,
            "badge_id": badge["badge_id"]
        })
        
        if already_earned:
            continue
        
        criteria = badge["criteria"]
        should_award = False
        
        if criteria["type"] == "credits" and total_credits >= criteria["threshold"]:
            should_award = True
        elif criteria["type"] == "level" and level >= criteria["threshold"]:
            should_award = True
        
        if should_award:
            from models import StudentBadge
            student_badge = StudentBadge(student_id=student_id, badge_id=badge["badge_id"])
            badge_dict = student_badge.model_dump()
            badge_dict["earned_at"] = badge_dict["earned_at"].isoformat()
            await db.student_badges.insert_one(badge_dict)

@router.get("/my-progress", response_model=List[Progress])
async def get_my_progress(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can view progress")
    
    student = await db.students.find_one({"user_id": current_user["user_id"]}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    progress_list = await db.progress.find(
        {"student_id": student["student_id"]},
        {"_id": 0}
    ).to_list(100)
    
    return progress_list
