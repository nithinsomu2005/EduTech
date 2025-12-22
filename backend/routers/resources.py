from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models import Resource
from typing import List
import os

client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("", response_model=List[Resource])
async def get_resources(grade_level: str = None, type: str = None, subject: str = None):
    query = {}
    if grade_level:
        query["grade_level"] = grade_level
    if type:
        query["type"] = type
    if subject:
        query["subject"] = subject
    
    resources = await db.resources.find(query, {"_id": 0}).to_list(100)
    return resources

@router.get("/{resource_id}", response_model=Resource)
async def get_resource(resource_id: str):
    resource = await db.resources.find_one({"resource_id": resource_id}, {"_id": 0})
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
