from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models import CareerRoadmap, Resource
from typing import List
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/career", tags=["Career"])

@router.get("/roadmaps", response_model=List[CareerRoadmap])
async def get_career_roadmaps():
    roadmaps = await db.career_roadmaps.find({}, {"_id": 0}).to_list(100)
    return roadmaps

@router.get("/roadmaps/{roadmap_id}", response_model=CareerRoadmap)
async def get_roadmap(roadmap_id: str):
    roadmap = await db.career_roadmaps.find_one({"roadmap_id": roadmap_id}, {"_id": 0})
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return roadmap
