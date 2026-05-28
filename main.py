from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os

from ocr_engine import extract_text

from extractor import (
    extract_invoice_number,
    extract_total_amount,
    extract_gst_amount,
    extract_vendor_name
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("temp", exist_ok=True)


@app.get("/")
def home():

    return {
        "message": "EasyOCR Invoice API Running"
    }


@app.post("/scan-invoice")
async def scan_invoice(
    file: UploadFile = File(...)
):

    try:

        file_path = f"temp/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text(file_path)

        vendor_name = extract_vendor_name(text)

        invoice_number = extract_invoice_number(text)

        gst_amount = extract_gst_amount(text)

        total_amount = extract_total_amount(text)

        return {
            "vendor_name": vendor_name,
            "invoice_number": invoice_number,
            "gst_amount": gst_amount,
            "total_amount": total_amount,
            "raw_text": text
        }

    except Exception as e:

        return {
            "error": str(e)
        }
