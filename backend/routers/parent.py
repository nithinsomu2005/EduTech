from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from routers.auth import get_current_user
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/parent", tags=["Parent"])

@router.get("/children")
async def get_children(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "parent":
        raise HTTPException(status_code=403, detail="Only parents can access this")
    
    student_ids = current_user.get("student_ids", [])
    students = await db.students.find(
        {"student_id": {"$in": student_ids}},
        {"_id": 0}
    ).to_list(10)
    
    for student in students:
        user = await db.users.find_one({"user_id": student["user_id"]}, {"_id": 0, "password_hash": 0})
        student["user_info"] = user
    
    return students

@router.get("/progress/{student_id}")
async def get_child_progress(student_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "parent":
        raise HTTPException(status_code=403, detail="Only parents can access this")
    
    if student_id not in current_user.get("student_ids", []):
        raise HTTPException(status_code=403, detail="Not authorized to view this student")
    
    student = await db.students.find_one({"student_id": student_id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    progress_list = await db.progress.find(
        {"student_id": student_id},
        {"_id": 0}
    ).sort("last_accessed", -1).to_list(50)
    
    for progress in progress_list:
        course = await db.courses.find_one({"course_id": progress["course_id"]}, {"_id": 0})
        progress["course_info"] = course
    
    return {
        "student": student,
        "progress": progress_list
    }

@router.get("/activity/{student_id}")
async def get_child_activity(student_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "parent":
        raise HTTPException(status_code=403, detail="Only parents can access this")
    
    if student_id not in current_user.get("student_ids", []):
        raise HTTPException(status_code=403, detail="Not authorized to view this student")
    
    recent_progress = await db.progress.find(
        {"student_id": student_id},
        {"_id": 0}
    ).sort("last_accessed", -1).limit(10).to_list(10)
    
    for item in recent_progress:
        course = await db.courses.find_one({"course_id": item["course_id"]}, {"_id": 0})
        item["course_title"] = course.get("title") if course else "Unknown Course"
    
    recent_badges = await db.student_badges.find(
        {"student_id": student_id},
        {"_id": 0}
    ).sort("earned_at", -1).limit(5).to_list(5)
    
    for item in recent_badges:
        badge = await db.badges.find_one({"badge_id": item["badge_id"]}, {"_id": 0})
        item["badge_name"] = badge.get("name") if badge else "Unknown Badge"
        item["badge_icon"] = badge.get("icon") if badge else ""
    
    return {
        "recent_courses": recent_progress,
        "recent_badges": recent_badges
    }
