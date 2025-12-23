from fastapi import APIRouter, HTTPException, Depends, Header
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List
from datetime import datetime, timezone
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(tags=["Student"])

async def get_current_student(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    from auth.jwt_handler import verify_token
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    student = await db.students.find_one({"student_id": payload.get("student_id")}, {"_id": 0, "password_hash": 0})
    if not student:
        raise HTTPException(status_code=401, detail="Student not found")
    
    return student


# ============ PROGRESS ROUTES ============
@router.post("/progress/start")
async def start_course(course_id: str, current_student: dict = Depends(get_current_student)):
    course = await db.courses.find_one({"course_id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    existing = await db.progress.find_one({
        "student_id": current_student["student_id"],
        "course_id": course_id
    }, {"_id": 0})
    
    if existing:
        return {"message": "Course already started", "progress": existing}
    
    import uuid
    progress = {
        "progress_id": str(uuid.uuid4()),
        "student_id": current_student["student_id"],
        "course_id": course_id,
        "video_completed": False,
        "watch_duration": 0,
        "quiz_completed": False,
        "quiz_passed": False,
        "score": 0,
        "credits_earned": 0,
        "completed_at": None,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.progress.insert_one(progress)
    del progress["_id"] if "_id" in progress else None
    return {"message": "Course started", "progress": progress}


@router.put("/progress/video-complete")
async def complete_video(course_id: str, watch_duration: int, current_student: dict = Depends(get_current_student)):
    course = await db.courses.find_one({"course_id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    video_completed = watch_duration >= (course.get("duration_minutes", 10) * 0.9)
    
    await db.progress.update_one(
        {"student_id": current_student["student_id"], "course_id": course_id},
        {"$set": {
            "video_completed": video_completed,
            "watch_duration": watch_duration,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }},
        upsert=True
    )
    
    return {
        "message": "Video progress updated",
        "video_completed": video_completed,
        "quiz_unlocked": video_completed
    }


@router.post("/progress/submit-quiz")
async def submit_quiz(submission: dict, current_student: dict = Depends(get_current_student)):
    quiz_id = submission.get("quiz_id")
    answers = submission.get("answers", {})
    
    quiz = await db.quizzes.find_one({"quiz_id": quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    course = await db.courses.find_one({"course_id": quiz["course_id"]}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check video completion
    progress = await db.progress.find_one({
        "student_id": current_student["student_id"],
        "course_id": quiz["course_id"]
    }, {"_id": 0})
    
    if not progress or not progress.get("video_completed"):
        raise HTTPException(status_code=400, detail="Complete the video first")
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz["questions"])
    
    for question in quiz["questions"]:
        q_text = question["question"]
        if answers.get(q_text) == question["correct_answer"]:
            correct_answers += 1
    
    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    passed = score >= quiz.get("passing_score", 60)
    credits_earned = course.get("credits", 10) if passed else 0
    
    # Update progress
    await db.progress.update_one(
        {"student_id": current_student["student_id"], "course_id": quiz["course_id"]},
        {"$set": {
            "quiz_completed": True,
            "quiz_passed": passed,
            "score": score,
            "credits_earned": credits_earned,
            "completed_at": datetime.now(timezone.utc).isoformat() if passed else None,
            "updated_at": datetime.now(timezone.utc).isoformat()
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
        
        # Award badges
        await check_and_award_badges(current_student["student_id"], new_credits, new_level)
        
        return {
            "score": score,
            "total": 100,
            "passed": passed,
            "credits_earned": credits_earned,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "new_credits": new_credits,
            "new_level": new_level
        }
    
    return {
        "score": score,
        "total": 100,
        "passed": passed,
        "credits_earned": credits_earned,
        "correct_answers": correct_answers,
        "total_questions": total_questions
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
        
        criteria = badge.get("criteria", {})
        should_award = False
        
        if criteria.get("type") == "credits" and total_credits >= criteria.get("threshold", 0):
            should_award = True
        elif criteria.get("type") == "level" and level >= criteria.get("threshold", 0):
            should_award = True
        
        if should_award:
            import uuid
            student_badge = {
                "id": str(uuid.uuid4()),
                "student_id": student_id,
                "badge_id": badge["badge_id"],
                "earned_at": datetime.now(timezone.utc).isoformat()
            }
            await db.student_badges.insert_one(student_badge)


@router.get("/progress/my-progress")
async def get_my_progress(current_student: dict = Depends(get_current_student)):
    progress_list = await db.progress.find(
        {"student_id": current_student["student_id"]},
        {"_id": 0}
    ).to_list(100)
    
    return progress_list


# ============ REWARDS ROUTES ============
@router.get("/rewards/stats")
async def get_stats(current_student: dict = Depends(get_current_student)):
    completed_courses = await db.progress.count_documents({
        "student_id": current_student["student_id"],
        "quiz_passed": True
    })
    
    total_badges = await db.student_badges.count_documents({
        "student_id": current_student["student_id"]
    })
    
    credits_to_next_level = ((current_student.get("level", 1)) * 500) - current_student.get("total_credits", 0)
    
    return {
        "total_credits": current_student.get("total_credits", 0),
        "level": current_student.get("level", 1),
        "credits_to_next_level": max(0, credits_to_next_level),
        "completed_courses": completed_courses,
        "total_badges": total_badges,
        "placement_readiness": current_student.get("placement_readiness", 0)
    }


@router.get("/rewards/my-badges")
async def get_my_badges(current_student: dict = Depends(get_current_student)):
    student_badges = await db.student_badges.find(
        {"student_id": current_student["student_id"]},
        {"_id": 0}
    ).to_list(100)
    
    badge_ids = [sb["badge_id"] for sb in student_badges]
    
    if not badge_ids:
        return []
    
    badges = await db.badges.find(
        {"badge_id": {"$in": badge_ids}},
        {"_id": 0}
    ).to_list(100)
    
    for badge in badges:
        for sb in student_badges:
            if sb["badge_id"] == badge["badge_id"]:
                badge["earned_at"] = sb["earned_at"]
                break
    
    return badges


# ============ COURSES ROUTES ============
@router.get("/courses")
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


@router.get("/courses/{course_id}")
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
        import uuid
        progress = {
            "progress_id": str(uuid.uuid4()),
            "student_id": current_student["student_id"],
            "course_id": course_id,
            "video_completed": False,
            "watch_duration": 0,
            "quiz_completed": False,
            "quiz_passed": False,
            "score": 0,
            "credits_earned": 0,
            "completed_at": None,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.progress.insert_one(progress)
        progress.pop("_id", None)
    
    course["progress"] = progress
    return course


@router.get("/courses/{course_id}/quiz")
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
