import xml.etree.ElementTree as ET
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, Body, APIRouter, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
import logging
import httpx
import json
import os
import yaml

XML_GEN_CONTAINER = "xml-gen"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

secrets_path = os.getenv("DB_CONFIG_PATH")
with open(secrets_path, "r") as f:
    config = json.load(f)

mongo_url = f"mongodb://{config['username']}:{config['password']}@mongodb:27017"
client = AsyncIOMotorClient(mongo_url)
db = client["mydatabase"]
collection = db["mycollection"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator_router = APIRouter(prefix="/generator")
viewer_router = APIRouter(prefix="/viewer")
stats_router = APIRouter(prefix="/stats")

@generator_router.post("/generate_xml")
async def generate_xml(num_of_records: int = Body(10000), currency: str = Body("PLN")):
    try:
        async with httpx.AsyncClient() as http:
            res = await http.post(f"http://{XML_GEN_CONTAINER}:8001/generate", json={"num_of_records": num_of_records, "currency": currency})
        logger.info("XML generation triggered.")
        return JSONResponse(content={"status": "success", "message": "XML generated."})
    except Exception as e:
        logger.exception("Error during XML generation.")
        return JSONResponse(status_code=500, content={"message": str(e)})

@generator_router.get("/get_xml")
async def get_xml():
    file_path = "/app/data/generated_users.xml"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return Response(content=f.read(), media_type="application/xml")
    return Response(content="", media_type="application/xml")

@generator_router.post("/convert_xml_to_json")
async def convert_xml_to_json():
    xml_path = "/app/data/generated_users.xml"
    if not os.path.exists(xml_path):
        return JSONResponse(status_code=404, content={"message": "XML file not found."})
    try:
        root = ET.parse(xml_path).getroot()
        records = [{child.tag: child.text for child in user} for user in root.findall("user")]
        if records:
            await collection.insert_many(records)
        return {"status": "success", "message": f"Inserted {len(records)} records into MongoDB."}
    except Exception as e:
        logger.exception("XML to JSON conversion failed.")
        return JSONResponse(status_code=500, content={"message": str(e)})

@generator_router.get("/download_yml")
async def download_yml():
    records = await collection.find().to_list(length=10000)
    if not records:
        return JSONResponse(status_code=404, content={"message": "No records in MongoDB."})
    yml_content = yaml.dump(records, default_flow_style=False)
    return StreamingResponse(iter([yml_content]), media_type="application/x-yaml", headers={"Content-Disposition": "attachment; filename=data.yml"})

@stats_router.get("/top_cities_by_debt")
async def top_cities_by_debt() -> dict[str, Any]:
    try:
        pipeline = [
            {"$match": {"currency": "PLN"}},
            {"$project": {"city": 1, "debt": {"$toDouble": "$debt"}}},
            {"$group": {"_id": "$city", "total_debt": {"$sum": "$debt"}}},
            {"$sort": {"total_debt": -1}},
            {"$limit": 10}
        ]
        result = await collection.aggregate(pipeline).to_list(length=100)
        if not result:
            raise HTTPException(status_code=404, detail="No records found.")
        return {"status": "success", "data": result}
    except Exception as e:
        logger.exception("Aggregation failed.")
        raise HTTPException(status_code=500, detail="Internal server error")

@stats_router.get("/all_records")
async def all_records():
    try:
        records = await collection.find().to_list(length=None)
        for r in records:
            r["id"] = str(r.pop("_id"))
        return {"status": "success", "data": records}
    except Exception as e:
        logger.exception("Failed to fetch all records.")
        raise HTTPException(status_code=500, detail="Internal server error")

app.include_router(generator_router, prefix="/api")
app.include_router(viewer_router, prefix="/api")
app.include_router(stats_router, prefix="/api")
