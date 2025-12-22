from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from routers.auth import get_current_user
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/teacher", tags=["Teacher"])

@router.get("/students")
async def get_teacher_students(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this")
    
    teacher_institution = current_user.get("institution_id")
    
    users = await db.users.find(
        {"role": "student", "institution_id": teacher_institution},
        {"_id": 0, "password_hash": 0}
    ).to_list(100)
    
    students_data = []
    for user in users:
        student = await db.students.find_one({"user_id": user["user_id"]}, {"_id": 0})
        if student:
            combined = {
                **user,
                "grade": student.get("grade"),
                "stream": student.get("stream"),
                "total_credits": student.get("total_credits", 0),
                "level": student.get("level", 1)
            }
            students_data.append(combined)
    
    active_students = len([s for s in students_data if s.get("total_credits", 0) > 0])
    
    stats = {
        "active_students": active_students,
        "total_courses": await db.courses.count_documents({}),
        "avg_completion": 0 if not students_data else int(sum(s.get("total_credits", 0) for s in students_data) / len(students_data) / 50)
    }
    
    return {
        "students": students_data,
        "stats": stats
    }
