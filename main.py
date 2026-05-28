from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os

from pdf2image import convert_from_path

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
        "message": "Invoice OCR API Running"
    }


@app.post("/scan-invoice")
async def scan_invoice(
    file: UploadFile = File(...)
):

    file_path = f"temp/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extension = file.filename.split(".")[-1].lower()

    image_path = file_path

    if extension == "pdf":

        pages = convert_from_path(file_path)

        image_path = "temp/converted_page.jpg"

        pages[0].save(image_path, "JPEG")

    text = extract_text(image_path)

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
