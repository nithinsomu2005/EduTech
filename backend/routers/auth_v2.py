from fastapi import APIRouter, HTTPException, Depends, Header
from motor.motor_asyncio import AsyncIOMotorClient
from models_v2 import StudentRegister, StudentLogin, StudentModel, Token, ParentOTPRequest, ParentOTPVerify, generate_username
from auth.jwt_handler import create_access_token, verify_token
from auth.password import hash_password, verify_password
from auth.otp_service import otp_service
from typing import Optional
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_current_student(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    student = await db.students.find_one({"student_id": payload.get("student_id")}, {"_id": 0, "password_hash": 0})
    if not student:
        raise HTTPException(status_code=401, detail="Student not found")
    
    return student

@router.post("/register")
async def register_student(data: StudentRegister):
    existing = await db.students.find_one({"mobile": data.mobile}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    all_usernames = await db.students.find({}, {"username": 1, "_id": 0}).to_list(1000)
    existing_usernames = [u["username"] for u in all_usernames]
    
    username = generate_username(data.name, existing_usernames)
    
    student = StudentModel(
        name=data.name,
        username=username,
        mobile=data.mobile,
        password_hash=hash_password(data.password),
        standard=data.standard
    )
    
    student_dict = student.model_dump()
    student_dict["created_at"] = student_dict["created_at"].isoformat()
    
    await db.students.insert_one(student_dict)
    
    return {
        "message": "Registration successful",
        "username": username,
        "student_id": student.student_id
    }

@router.post("/login", response_model=Token)
async def login_student(credentials: StudentLogin):
    student = await db.students.find_one({"username": credentials.username}, {"_id": 0})
    
    if not student:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(credentials.password, student["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token_data = {
        "student_id": student["student_id"],
        "username": student["username"],
        "standard": student["standard"]
    }
    access_token = create_access_token(token_data)
    
    student_response = {k: v for k, v in student.items() if k != "password_hash"}
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": student_response
    }

@router.post("/parent/send-otp")
async def send_parent_otp(request: ParentOTPRequest):
    students = await db.students.find({"mobile": request.mobile}, {"_id": 0, "password_hash": 0}).to_list(10)
    
    if not students:
        raise HTTPException(status_code=404, detail="No students found with this mobile number")
    
    otp = otp_service.generate_otp(request.mobile)
    
    return {
        "message": "OTP sent successfully",
        "otp": otp,
        "students_count": len(students)
    }

@router.post("/parent/verify-otp", response_model=Token)
async def verify_parent_otp(request: ParentOTPVerify):
    if not otp_service.verify_otp(request.mobile, request.otp):
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    
    students = await db.students.find({"mobile": request.mobile}, {"_id": 0, "password_hash": 0}).to_list(10)
    
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    
    token_data = {
        "parent_mobile": request.mobile,
        "role": "parent",
        "student_ids": [s["student_id"] for s in students]
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "role": "parent",
            "mobile": request.mobile,
            "students": students
        }
    }

@router.get("/me")
async def get_me(current_student: dict = Depends(get_current_student)):
    return current_student
