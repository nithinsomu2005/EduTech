from fastapi import APIRouter, HTTPException, Depends, Header
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
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
    mobile = current_parent["parent_mobile"]
    
    students = await db.students.find(
        {"mobile": mobile},
        {"_id": 0, "password_hash": 0}
    ).to_list(10)
    
    for student in students:
        progress_list = await db.progress.find(
            {"student_id": student["student_id"]},
            {"_id": 0}
        ).to_list(100)
        
        completed = sum(1 for p in progress_list if p.get("quiz_completed"))
        total = await db.courses.count_documents({"standard": student["standard"]})
        
        student["completed_courses"] = completed
        student["total_courses"] = total
        student["progress_percentage"] = int((completed / total * 100)) if total > 0 else 0
    
    return students

@router.get("/child-progress/{student_id}")
async def get_child_progress(student_id: str, current_parent: dict = Depends(get_current_parent)):
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
    
    for progress in progress_list:
        course = await db.courses.find_one(
            {"course_id": progress["course_id"]},
            {"_id": 0}
        )
        progress["course_info"] = course
    
    return {
        "student": student,
        "progress": progress_list
    }
