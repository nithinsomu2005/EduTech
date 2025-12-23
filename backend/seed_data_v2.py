import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_data_v2():
    print("🌱 Seeding New EdTech Platform (Grade-Isolated)")
    print("=" * 60)
    
    await db.students.delete_many({})
    await db.courses.delete_many({})
    await db.quizzes.delete_many({})
    await db.progress.delete_many({})
    
    print("\n📚 Creating Grade-Specific Courses...")
    courses_data = [
        # KG
        {"standard": "KG", "subject": "Rhymes", "title": "ABC Song", "video_url": "https://www.youtube.com/watch?v=BELlZKpi1Zs", "duration": 3, "credits": 50, "thumbnail": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400"},
        {"standard": "KG", "subject": "Colors", "title": "Learn Colors", "video_url": "https://www.youtube.com/watch?v=skvA00Ush88", "duration": 5, "credits": 50, "thumbnail": "https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=400"},
        
        # Class 6
        {"standard": "6", "subject": "Science", "title": "Photosynthesis", "video_url": "https://www.youtube.com/watch?v=UPBMG5EYydo", "duration": 12, "credits": 100, "thumbnail": "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=400"},
        {"standard": "6", "subject": "Mathematics", "title": "Fractions Basics", "video_url": "https://www.youtube.com/watch?v=uDfiyH-40bE", "duration": 15, "credits": 100, "thumbnail": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400"},
        
        # Class 10
        {"standard": "10", "subject": "Science", "title": "Chemical Reactions", "video_url": "https://www.youtube.com/watch?v=8IlzKri08kk", "duration": 15, "credits": 150, "thumbnail": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=400"},
        {"standard": "10", "subject": "Mathematics", "title": "Quadratic Equations", "video_url": "https://www.youtube.com/watch?v=9vKqVkMQHKk", "duration": 18, "credits": 150, "thumbnail": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400"},
        
        # Class 12
        {"standard": "12", "subject": "Physics", "title": "Newton's Laws", "video_url": "https://www.youtube.com/watch?v=kKKM8Y-u7ds", "duration": 20, "credits": 200, "thumbnail": "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=400"},
        {"standard": "12", "subject": "Chemistry", "title": "Organic Chemistry", "video_url": "https://www.youtube.com/watch?v=cRCxdBV8YKQ", "duration": 22, "credits": 200, "thumbnail": "https://images.unsplash.com/photo-1532634922-8fe0b757fb13?w=400"},
        
        # BTECH
        {"standard": "BTECH", "subject": "DSA", "title": "Data Structures Intro", "video_url": "https://www.youtube.com/watch?v=Hj_rA0dhr2I", "duration": 25, "credits": 250, "thumbnail": "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400"},
        {"standard": "BTECH", "subject": "Web Dev", "title": "HTML CSS Basics", "video_url": "https://www.youtube.com/watch?v=UB1O30fR-EE", "duration": 30, "credits": 250, "thumbnail": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400"},
    ]
    
    courses = []
    quizzes = []
    
    for c_data in courses_data:
        course_id = str(uuid.uuid4())
        quiz_id = str(uuid.uuid4())
        
        course = {
            "course_id": course_id,
            "standard": c_data["standard"],
            "subject": c_data["subject"],
            "title": c_data["title"],
            "description": f"Learn {c_data['title']} for Class {c_data['standard']}",
            "video_url": c_data["video_url"],
            "duration_minutes": c_data["duration"],
            "credits": c_data["credits"],
            "thumbnail": c_data["thumbnail"],
            "quiz_id": quiz_id,
            "created_at": datetime.utcnow().isoformat()
        }
        courses.append(course)
        
        quiz = {
            "quiz_id": quiz_id,
            "course_id": course_id,
            "standard": c_data["standard"],
            "subject": c_data["subject"],
            "questions": [
                {
                    "question": f"What is the main topic of this lesson?",
                    "options": [c_data["title"], "Something else", "Not sure", "Other topic"],
                    "correct_answer": c_data["title"]
                },
                {
                    "question": f"Which subject does this belong to?",
                    "options": [c_data["subject"], "History", "Geography", "Art"],
                    "correct_answer": c_data["subject"]
                },
                {
                    "question": f"What class is this for?",
                    "options": [f"Class {c_data['standard']}", "All classes", "No class", "Unknown"],
                    "correct_answer": f"Class {c_data['standard']}"
                }
            ],
            "passing_score": 60
        }
        quizzes.append(quiz)
    
    await db.courses.insert_many(courses)
    await db.quizzes.insert_many(quizzes)
    
    print(f"✅ Created {len(courses)} courses (grade-isolated)")
    print(f"✅ Created {len(quizzes)} quizzes")
    
    print("\n👤 Creating demo student...")
    from auth.password import hash_password
    
    demo_student = {
        "student_id": str(uuid.uuid4()),
        "name": "Nanda",
        "username": "nanda_123",
        "mobile": "9876543210",
        "password_hash": hash_password("demo123"),
        "standard": "6",
        "total_credits": 0,
        "level": 1,
        "role": "student",
        "created_at": datetime.utcnow().isoformat()
    }
    
    await db.students.insert_one(demo_student)
    print(f"✅ Created demo student: {demo_student['username']}")
    
    print("\n" + "=" * 60)
    print("🎉 Seeding Complete!")
    print(f"   📚 Courses by grade: KG(2), 6(2), 10(2), 12(2), BTECH(2)")
    print(f"   👤 Demo student: nanda_123 / demo123 (Class 6)")
    print(f"   📱 Parent login: 9876543210 (will get OTP)")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data_v2())
