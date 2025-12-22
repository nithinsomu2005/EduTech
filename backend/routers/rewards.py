from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from models import Badge, Certificate
from routers.auth import get_current_user
from typing import List
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/rewards", tags=["Rewards"])

@router.get("/badges", response_model=List[Badge])
async def get_all_badges():
    badges = await db.badges.find({}, {"_id": 0}).to_list(100)
    return badges

@router.get("/my-badges")
async def get_my_badges(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students have badges")
    
    student = await db.students.find_one({"user_id": current_user["user_id"]}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    student_badges = await db.student_badges.find(
        {"student_id": student["student_id"]},
        {"_id": 0}
    ).to_list(100)
    
    badge_ids = [sb["badge_id"] for sb in student_badges]
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

@router.get("/certificates")
async def get_my_certificates(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students have certificates")
    
    student = await db.students.find_one({"user_id": current_user["user_id"]}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    certificates = await db.certificates.find(
        {"student_id": student["student_id"]},
        {"_id": 0}
    ).to_list(100)
    
    return certificates

@router.get("/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students have stats")
    
    student = await db.students.find_one({"user_id": current_user["user_id"]}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    completed_courses = await db.progress.count_documents({
        "student_id": student["student_id"],
        "quiz_passed": True
    })
    
    total_badges = await db.student_badges.count_documents({
        "student_id": student["student_id"]
    })
    
    credits_to_next_level = ((student.get("level", 1)) * 500) - student.get("total_credits", 0)
    
    return {
        "total_credits": student.get("total_credits", 0),
        "level": student.get("level", 1),
        "credits_to_next_level": credits_to_next_level,
        "completed_courses": completed_courses,
        "total_badges": total_badges,
        "placement_readiness": student.get("placement_readiness", 0)
    }
