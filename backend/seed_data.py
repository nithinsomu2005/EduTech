import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timedelta

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_data():
    print("🌱 Seeding database...")
    
    await db.courses.delete_many({})
    await db.quizzes.delete_many({})
    await db.badges.delete_many({})
    await db.career_roadmaps.delete_many({})
    await db.resources.delete_many({})
    
    print("📚 Creating courses...")
    courses = [
        {
            "course_id": str(uuid.uuid4()),
            "title": "Introduction to Shapes and Colors",
            "grade_level": "KG",
            "subject": "Mathematics",
            "video_url": "https://www.youtube.com/watch?v=skvA00Ush88",
            "duration_minutes": 5,
            "credits": 50,
            "description": "Learn basic shapes and colors through fun animations",
            "thumbnail": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400",
            "order": 1,
            "created_by": "admin",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "course_id": str(uuid.uuid4()),
            "title": "Photosynthesis - How Plants Make Food",
            "grade_level": "6-10",
            "subject": "Science",
            "video_url": "https://www.youtube.com/watch?v=UPBMG5EYydo",
            "duration_minutes": 10,
            "credits": 100,
            "description": "Understanding the process of photosynthesis in plants",
            "thumbnail": "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=400",
            "order": 1,
            "created_by": "admin",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "course_id": str(uuid.uuid4()),
            "title": "Newton's Laws of Motion",
            "grade_level": "Inter",
            "subject": "Physics",
            "video_url": "https://www.youtube.com/watch?v=kKKM8Y-u7ds",
            "duration_minutes": 15,
            "credits": 150,
            "description": "Deep dive into Newton's three laws of motion",
            "thumbnail": "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=400",
            "order": 1,
            "created_by": "admin",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "course_id": str(uuid.uuid4()),
            "title": "Data Structures: Arrays and Linked Lists",
            "grade_level": "BTech",
            "subject": "Computer Science",
            "video_url": "https://www.youtube.com/watch?v=Hj_rA0dhr2I",
            "duration_minutes": 20,
            "credits": 200,
            "description": "Understanding fundamental data structures",
            "thumbnail": "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400",
            "order": 1,
            "created_by": "admin",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "course_id": str(uuid.uuid4()),
            "title": "Introduction to Web Development",
            "grade_level": "BTech",
            "subject": "Computer Science",
            "video_url": "https://www.youtube.com/watch?v=UB1O30fR-EE",
            "duration_minutes": 25,
            "credits": 200,
            "description": "Learn HTML, CSS and JavaScript basics",
            "thumbnail": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400",
            "order": 2,
            "created_by": "admin",
            "created_at": datetime.utcnow().isoformat()
        }
    ]
    
    await db.courses.insert_many(courses)
    print(f"✅ Created {len(courses)} courses")
    
    print("📝 Creating quizzes...")
    quizzes = [
        {
            "quiz_id": str(uuid.uuid4()),
            "course_id": courses[1]["course_id"],
            "title": "Photosynthesis Quiz",
            "questions": [
                {
                    "question": "What is the primary pigment in photosynthesis?",
                    "options": ["Carotene", "Chlorophyll", "Xanthophyll", "Melanin"],
                    "correct_answer": "Chlorophyll",
                    "marks": 10
                },
                {
                    "question": "What gas do plants absorb during photosynthesis?",
                    "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
                    "correct_answer": "Carbon Dioxide",
                    "marks": 10
                },
                {
                    "question": "What is the main product of photosynthesis?",
                    "options": ["Water", "Glucose", "Carbon Dioxide", "Oxygen"],
                    "correct_answer": "Glucose",
                    "marks": 10
                }
            ],
            "passing_marks": 20,
            "total_marks": 30,
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "quiz_id": str(uuid.uuid4()),
            "course_id": courses[3]["course_id"],
            "title": "Data Structures Quiz",
            "questions": [
                {
                    "question": "What is the time complexity of accessing an array element?",
                    "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
                    "correct_answer": "O(1)",
                    "marks": 10
                },
                {
                    "question": "Which data structure uses LIFO principle?",
                    "options": ["Queue", "Stack", "Array", "Linked List"],
                    "correct_answer": "Stack",
                    "marks": 10
                }
            ],
            "passing_marks": 12,
            "total_marks": 20,
            "created_at": datetime.utcnow().isoformat()
        }
    ]
    
    await db.quizzes.insert_many(quizzes)
    print(f"✅ Created {len(quizzes)} quizzes")
    
    print("🏆 Creating badges...")
    badges = [
        {
            "badge_id": str(uuid.uuid4()),
            "name": "First Steps",
            "description": "Complete your first course",
            "icon": "🎯",
            "criteria": {"type": "credits", "threshold": 50},
            "rarity": "common"
        },
        {
            "badge_id": str(uuid.uuid4()),
            "name": "Knowledge Seeker",
            "description": "Earn 500 credits",
            "icon": "📚",
            "criteria": {"type": "credits", "threshold": 500},
            "rarity": "rare"
        },
        {
            "badge_id": str(uuid.uuid4()),
            "name": "Rising Star",
            "description": "Reach Level 3",
            "icon": "⭐",
            "criteria": {"type": "level", "threshold": 3},
            "rarity": "rare"
        },
        {
            "badge_id": str(uuid.uuid4()),
            "name": "Master Learner",
            "description": "Earn 1000 credits",
            "icon": "🏅",
            "criteria": {"type": "credits", "threshold": 1000},
            "rarity": "epic"
        },
        {
            "badge_id": str(uuid.uuid4()),
            "name": "Legend",
            "description": "Reach Level 5",
            "icon": "👑",
            "criteria": {"type": "level", "threshold": 5},
            "rarity": "legendary"
        }
    ]
    
    await db.badges.insert_many(badges)
    print(f"✅ Created {len(badges)} badges")
    
    print("💼 Creating career roadmaps...")
    roadmaps = [
        {
            "roadmap_id": str(uuid.uuid4()),
            "title": "Full Stack Developer",
            "skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "MongoDB", "Git"],
            "milestones": [
                {"title": "Frontend Basics", "duration": "2 months", "resources": ["https://www.freecodecamp.org"]},
                {"title": "Backend Development", "duration": "2 months", "resources": ["https://nodejs.org/en/docs/"]},
                {"title": "Full Stack Projects", "duration": "2 months", "resources": ["https://github.com/topics/full-stack"]}
            ],
            "job_roles": ["Full Stack Developer", "Web Developer", "Software Engineer"],
            "avg_salary": "₹6-12 LPA"
        },
        {
            "roadmap_id": str(uuid.uuid4()),
            "title": "Data Scientist",
            "skills": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization", "Pandas"],
            "milestones": [
                {"title": "Python & Statistics", "duration": "3 months", "resources": ["https://www.kaggle.com/learn"]},
                {"title": "Machine Learning", "duration": "3 months", "resources": ["https://www.coursera.org/learn/machine-learning"]},
                {"title": "Real-world Projects", "duration": "3 months", "resources": ["https://www.kaggle.com/competitions"]}
            ],
            "job_roles": ["Data Scientist", "ML Engineer", "Data Analyst"],
            "avg_salary": "₹8-15 LPA"
        },
        {
            "roadmap_id": str(uuid.uuid4()),
            "title": "Mobile App Developer",
            "skills": ["React Native", "Flutter", "UI/UX", "API Integration", "Firebase"],
            "milestones": [
                {"title": "Mobile Development Basics", "duration": "2 months", "resources": ["https://reactnative.dev/docs/getting-started"]},
                {"title": "Advanced Features", "duration": "2 months", "resources": ["https://flutter.dev/docs"]},
                {"title": "Publish Apps", "duration": "1 month", "resources": ["https://developer.android.com"]}
            ],
            "job_roles": ["Mobile Developer", "App Developer", "React Native Developer"],
            "avg_salary": "₹5-10 LPA"
        }
    ]
    
    await db.career_roadmaps.insert_many(roadmaps)
    print(f"✅ Created {len(roadmaps)} career roadmaps")
    
    print("📖 Creating resources...")
    resources = [
        {
            "resource_id": str(uuid.uuid4()),
            "grade_level": "6-10",
            "type": "textbook",
            "title": "NCERT Science Class 10",
            "subject": "Science",
            "url": "https://ncert.nic.in/textbook.php?jesc1=0-11",
            "thumbnail": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400",
            "description": "Official NCERT Science textbook for Class 10",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "resource_id": str(uuid.uuid4()),
            "grade_level": "Inter",
            "type": "question_paper",
            "title": "JEE Main 2024 Question Paper",
            "subject": "Physics",
            "url": "https://jeemain.nta.nic.in/",
            "thumbnail": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400",
            "year": 2024,
            "description": "JEE Main Physics question paper with solutions",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "resource_id": str(uuid.uuid4()),
            "grade_level": "BTech",
            "type": "formula_sheet",
            "title": "DSA Cheat Sheet",
            "subject": "Computer Science",
            "url": "https://www.geeksforgeeks.org/data-structures/",
            "thumbnail": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=400",
            "description": "Comprehensive Data Structures and Algorithms reference",
            "created_at": datetime.utcnow().isoformat()
        }
    ]
    
    await db.resources.insert_many(resources)
    print(f"✅ Created {len(resources)} resources")
    
    print("🎉 Database seeded successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
