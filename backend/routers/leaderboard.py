from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("")
async def get_leaderboard(institution: str = None, limit: int = 50):
    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user_info"
            }
        },
        {
            "$unwind": "$user_info"
        },
        {
            "$sort": {"total_credits": -1}
        },
        {
            "$limit": limit
        },
        {
            "$project": {
                "_id": 0,
                "student_id": 1,
                "total_credits": 1,
                "level": 1,
                "institution_name": 1,
                "full_name": "$user_info.full_name",
                "profile_image": "$user_info.profile_image"
            }
        }
    ]
    
    if institution:
        pipeline.insert(0, {"$match": {"institution_name": institution}})
    
    leaderboard = await db.students.aggregate(pipeline).to_list(limit)
    
    for idx, entry in enumerate(leaderboard):
        entry["rank"] = idx + 1
    
    return leaderboard
