from fastapi import APIRouter, HTTPException, Depends, Header
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from datetime import datetime, timezone
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/parent", tags=["Parent"])

async def get_current_parent(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    from auth.jwt_handler import verify_token
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload or payload.get("role") != "parent":
        raise HTTPException(status_code=401, detail="Invalid parent token")
    
    return payload


@router.get("/children")
async def get_children(current_parent: dict = Depends(get_current_parent)):
    """Get all children linked to parent's mobile number"""
    mobile = current_parent["parent_mobile"]
    
    students = await db.students.find(
        {"mobile": mobile},
        {"_id": 0, "password_hash": 0}
    ).to_list(10)
    
    children = []
    for student in students:
        # Get progress stats
        progress_list = await db.progress.find(
            {"student_id": student["student_id"]},
            {"_id": 0}
        ).to_list(100)
        
        completed = sum(1 for p in progress_list if p.get("quiz_passed"))
        total = await db.courses.count_documents({"standard": student["standard"]})
        
        children.append({
            "student_id": student["student_id"],
            "name": student.get("name", "Student"),
            "username": student.get("username", ""),
            "standard": student.get("standard", ""),
            "grade_year": student.get("standard", ""),
            "stream": None,
            "total_credits": student.get("total_credits", 0),
            "level": student.get("level", 1),
            "completed_courses": completed,
            "total_courses": total,
            "progress_percentage": int((completed / total * 100)) if total > 0 else 0,
            "user_info": {
                "full_name": student.get("name", "Student")
            }
        })
    
    return children


@router.get("/progress/{student_id}")
async def get_child_progress(student_id: str, current_parent: dict = Depends(get_current_parent)):
    """Get detailed progress for a specific child"""
    if student_id not in current_parent.get("student_ids", []):
        raise HTTPException(status_code=403, detail="Not authorized to view this student")
    
    student = await db.students.find_one(
        {"student_id": student_id},
        {"_id": 0, "password_hash": 0}
    )
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    progress_list = await db.progress.find(
        {"student_id": student_id},
        {"_id": 0}
    ).sort("updated_at", -1).to_list(50)
    
    # Add course info to each progress item
    for progress in progress_list:
        course = await db.courses.find_one(
            {"course_id": progress["course_id"]},
            {"_id": 0}
        )
        progress["course_info"] = course
    
    return {
        "student": {
            "student_id": student["student_id"],
            "name": student.get("name", "Student"),
            "username": student.get("username", ""),
            "standard": student.get("standard", ""),
            "total_credits": student.get("total_credits", 0),
            "level": student.get("level", 1),
            "mobile": student.get("mobile", "")
        },
        "progress": progress_list
    }


@router.get("/activity/{student_id}")
async def get_child_activity(student_id: str, current_parent: dict = Depends(get_current_parent)):
    """Get recent activity for a specific child"""
    if student_id not in current_parent.get("student_ids", []):
        raise HTTPException(status_code=403, detail="Not authorized to view this student")
    
    # Get recent progress
    progress_list = await db.progress.find(
        {"student_id": student_id},
        {"_id": 0}
    ).sort("updated_at", -1).to_list(10)
    
    recent_courses = []
    for progress in progress_list:
        course = await db.courses.find_one(
            {"course_id": progress["course_id"]},
            {"_id": 0}
        )
        if course:
            recent_courses.append({
                "course_id": progress["course_id"],
                "course_title": course.get("title", "Unknown Course"),
                "subject": course.get("subject", ""),
                "video_completed": progress.get("video_completed", False),
                "quiz_passed": progress.get("quiz_passed", False),
                "score": progress.get("score", 0),
                "watch_duration": progress.get("watch_duration", 0),
                "credits_earned": progress.get("credits_earned", 0),
                "updated_at": progress.get("updated_at", "")
            })
    
    # Get recent badges
    student_badges = await db.student_badges.find(
        {"student_id": student_id},
        {"_id": 0}
    ).sort("earned_at", -1).to_list(10)
    
    recent_badges = []
    for sb in student_badges:
        badge = await db.badges.find_one(
            {"badge_id": sb["badge_id"]},
            {"_id": 0}
        )
        if badge:
            recent_badges.append({
                "badge_id": badge["badge_id"],
                "badge_name": badge.get("name", "Badge"),
                "badge_icon": badge.get("icon", "🏆"),
                "description": badge.get("description", ""),
                "earned_at": sb.get("earned_at", "")
            })
    
    return {
        "recent_courses": recent_courses,
        "recent_badges": recent_badges
    }
