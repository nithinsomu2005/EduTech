import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime
import sys
sys.path.insert(0, '/app/backend')
from auth.password import hash_password

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_data():
    print("🌱 Seeding EdTech Platform")
    print("=" * 60)
    
    await db.students.delete_many({})
    await db.courses.delete_many({})
    await db.quizzes.delete_many({})
    await db.progress.delete_many({})
    
    courses_data = [
        {"standard": "KG", "subject": "Rhymes", "title": "ABC Song", "video_url": "https://www.youtube.com/watch?v=BELlZKpi1Zs", "duration": 3, "credits": 50},
        {"standard": "KG", "subject": "Colors", "title": "Learn Colors", "video_url": "https://www.youtube.com/watch?v=skvA00Ush88", "duration": 5, "credits": 50},
        {"standard": "6", "subject": "Science", "title": "Photosynthesis", "video_url": "https://www.youtube.com/watch?v=UPBMG5EYydo", "duration": 12, "credits": 100},
        {"standard": "6", "subject": "Mathematics", "title": "Fractions", "video_url": "https://www.youtube.com/watch?v=uDfiyH-40bE", "duration": 15, "credits": 100},
        {"standard": "10", "subject": "Science", "title": "Chemical Reactions", "video_url": "https://www.youtube.com/watch?v=8IlzKri08kk", "duration": 15, "credits": 150},
        {"standard": "10", "subject": "Mathematics", "title": "Quadratic Equations", "video_url": "https://www.youtube.com/watch?v=9vKqVkMQHKk", "duration": 18, "credits": 150},
        {"standard": "12", "subject": "Physics", "title": "Newton's Laws", "video_url": "https://www.youtube.com/watch?v=kKKM8Y-u7ds", "duration": 20, "credits": 200},
        {"standard": "12", "subject": "Chemistry", "title": "Organic Chemistry", "video_url": "https://www.youtube.com/watch?v=cRCxdBV8YKQ", "duration": 22, "credits": 200},
        {"standard": "BTECH", "subject": "DSA", "title": "Data Structures", "video_url": "https://www.youtube.com/watch?v=Hj_rA0dhr2I", "duration": 25, "credits": 250},
        {"standard": "BTECH", "subject": "Web Dev", "title": "HTML CSS Basics", "video_url": "https://www.youtube.com/watch?v=UB1O30fR-EE", "duration": 30, "credits": 250},
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
            "description": f"Learn {c_data['title']}",
            "video_url": c_data["video_url"],
            "duration_minutes": c_data["duration"],
            "credits": c_data["credits"],
            "thumbnail": "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400",
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
                    "question": f"What is the main topic?",
                    "options": [c_data["title"], "Something else", "Not sure", "Other"],
                    "correct_answer": c_data["title"]
                },
                {
                    "question": f"Which subject?",
                    "options": [c_data["subject"], "History", "Geography", "Art"],
                    "correct_answer": c_data["subject"]
                },
                {
                    "question": f"What class?",
                    "options": [c_data["standard"], "All classes", "No class", "Unknown"],
                    "correct_answer": c_data["standard"]
                }
            ],
            "passing_score": 60
        }
        quizzes.append(quiz)
    
    await db.courses.insert_many(courses)
    await db.quizzes.insert_many(quizzes)
    
    print(f"✅ Created {len(courses)} courses")
    
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
    print(f"✅ Demo: nanda_123 / demo123 (Class 6)")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
