import xml.etree.ElementTree as ET
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import Request, Response
import logging
import httpx
import json
import os
import yaml

XML_GEN_CONTAINER = "xml-gen"  # <- container name

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

secrets_path = os.getenv("DB_CONFIG_PATH")
with open(secrets_path, "r") as f:
    config = json.load(f)

templates = Jinja2Templates(directory="templates")
mongo_user = config.get("username")
mongo_pass = config.get("password")
mongo_host = "mongodb"
mongo_url = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017"

app = FastAPI()
client = AsyncIOMotorClient(mongo_url)
db = client["mydatabase"]
collection = db["mycollection"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico")
async def favicon():
    return {}

@app.post("/generate_xml")
async def generate_xml(
    num_of_records: int = Body(10000),
    currency: str = Body("PLN")
):
    logger.info("Triggering XML generation on xml-gen container...")
    logger.debug(f"Payload: num_of_records={num_of_records}, currency={currency}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{XML_GEN_CONTAINER}:8001/generate",
                json={"num_of_records": num_of_records, "currency": currency}
            )
            logger.info("Response received from xml-gen.")
            logger.debug(f"Response body: {response.text}")
        return JSONResponse(content={"status": "success", "message": "XML generated."})

    except Exception as e:
        logger.error("Error communicating with xml-gen:")
        logger.exception(e)
        return {"error": str(e)}

@app.get("/get_xml")
async def get_xml():
    file_path = "/app/data/generated_users.xml"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            xml_content = f.read()
        return Response(content=xml_content, media_type="application/xml")
    else:
        return Response(content="", media_type="application/xml")

@app.post("/convert_xml_to_json")
async def convert_xml_to_json():
    xml_path = "/app/data/generated_users.xml"

    if not os.path.exists(xml_path):
        return JSONResponse(status_code=404, content={"message": "XML file not found."})

    try:
        # Parse XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        records = []
        for user_elem in root.findall("user"):
            record = {child.tag: child.text for child in user_elem}
            records.append(record)

        if records:
            await collection.insert_many(records)

        return {
            "status": "success",
            "message": f"Inserted {len(records)} records into MongoDB."
        }
    except Exception as e:
        logger.exception("Failed to convert XML to JSON and insert into MongoDB.")
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/download_yml")
async def download_yml():
    cursor = collection.find()
    records = await cursor.to_list(length=10000)

    if not records:
        return JSONResponse(status_code=404, content={"message": "No records found in MongoDB."})

    yml_content = yaml.dump(records, default_flow_style=False)

    return StreamingResponse(
        iter([yml_content]),
        media_type="application/x-yaml",
        headers={"Content-Disposition": "attachment; filename=data.yml"}
    )
