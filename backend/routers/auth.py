from fastapi import APIRouter, HTTPException, Depends, Header
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import UserCreate, User, UserLogin, Token, ParentOTPRequest, ParentOTPVerify
from auth.jwt_handler import create_access_token, verify_token
from auth.password import hash_password, verify_password
from auth.otp_service import otp_service
from typing import Optional
import os
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = await db.users.find_one({"user_id": payload.get("user_id")}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@router.post("/register")
async def register(user_data: UserCreate):
    existing = await db.users.find_one({"institution_id": user_data.institution_id}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Institution ID already registered")
    
    existing_email = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(**user_data.model_dump(exclude={"password"}))
    user_dict = user.model_dump()
    user_dict["password_hash"] = hash_password(user_data.password)
    user_dict["created_at"] = user_dict["created_at"].isoformat()
    if user_dict.get("last_login"):
        user_dict["last_login"] = user_dict["last_login"].isoformat()
    
    await db.users.insert_one(user_dict)
    
    if user_data.role == "student":
        from models import Student
        student = Student(
            user_id=user.user_id,
            grade="BTech",
            grade_year=1,
            parent_mobile=user_data.mobile,
            institution_name="Demo Institution"
        )
        student_dict = student.model_dump()
        student_dict["created_at"] = student_dict["created_at"].isoformat()
        await db.students.insert_one(student_dict)
    
    return {"message": "Registration successful", "user_id": user.user_id}

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    user = await db.users.find_one({"institution_id": credentials.institution_id}, {"_id": 0})
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get("is_active", True):
        raise HTTPException(status_code=401, detail="Account is inactive")
    
    from datetime import datetime
    await db.users.update_one(
        {"user_id": user["user_id"]},
        {"$set": {"last_login": datetime.utcnow().isoformat()}}
    )
    
    token_data = {
        "user_id": user["user_id"],
        "role": user["role"],
        "institution_id": user["institution_id"]
    }
    access_token = create_access_token(token_data)
    
    user_response = {k: v for k, v in user.items() if k != "password_hash"}
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }

@router.post("/parent/send-otp")
async def send_parent_otp(request: ParentOTPRequest):
    students = await db.students.find({"parent_mobile": request.mobile}, {"_id": 0}).to_list(10)
    
    if not students:
        raise HTTPException(status_code=404, detail="No students linked to this mobile number")
    
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
    
    students = await db.students.find({"parent_mobile": request.mobile}, {"_id": 0}).to_list(10)
    
    if not students:
        raise HTTPException(status_code=404, detail="No students linked to this mobile number")
    
    student_ids = [s["student_id"] for s in students]
    user_ids = [s["user_id"] for s in students]
    
    users_list = await db.users.find({"user_id": {"$in": user_ids}}, {"_id": 0, "password_hash": 0}).to_list(10)
    
    token_data = {
        "user_id": "parent_" + request.mobile,
        "role": "parent",
        "student_ids": student_ids,
        "mobile": request.mobile
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "role": "parent",
            "mobile": request.mobile,
            "students": students,
            "users": users_list
        }
    }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "student":
        student = await db.students.find_one({"user_id": current_user["user_id"]}, {"_id": 0})
        current_user["student_profile"] = student
    return current_user
