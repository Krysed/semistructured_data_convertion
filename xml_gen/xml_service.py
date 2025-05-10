from fastapi import FastAPI
from pydantic import BaseModel
from generate_xml import generate_and_save_xml
import logging
import traceback

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class GenerationRequest(BaseModel):
    num_of_records: int = 10000
    currency: str = "PLN"

@app.post("/generate")
def generate(request: GenerationRequest):
    logger.info("Received request to generate XML")
    logger.debug(f"Request data: num_of_records={request.num_of_records}, currency={request.currency}")
    try:
        generate_and_save_xml(request.num_of_records, request.currency)
        logger.info("XML generated successfully.")
        return {"status": "success", "message": "XML generated."}
    except Exception as e:
        logger.error("Failed to generate XML")
        logger.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}
