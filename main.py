# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
from models import Application
from db import db, applications_collection
from ocr_utils import extract_text_from_image, categorize_cashflow
from digital_footprint import process_tiktok_data
from train import train_model as train_model_func
from predict import predict_eligibility

app = FastAPI()

# Upload a cashflow record file and process OCR + categorization
@app.post("/upload_cashflow")
async def upload_cashflow(file: UploadFile = File(...)):
    try:
        text = extract_text_from_image(file)
        processed = categorize_cashflow(text)
        return processed
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Submit a full application
@app.post("/apply")
async def apply(app_data: Application):
    data = app_data.dict()
    result = await applications_collection.insert_one(data)
    return {"message": "Application submitted", "id": str(result.inserted_id)}

# Update digital footprint for an application (e.g. TikTok data)
@app.post("/update_digital/{app_id}")
async def update_digital(app_id: str, tiktok_data: dict):
    processed = process_tiktok_data(tiktok_data)
    update_result = await applications_collection.update_one(
        {"_id": app_id}, {"$set": {"digital_footprint.tiktok": processed}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Application not found or update failed")
    return {"message": "Digital footprint updated"}

# Train the RandomForest model
@app.post("/train")
async def train():
    try:
        model_path = await train_model_func(db)
        return {"message": "Model trained", "model_path": model_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Predict loan eligibility based on cashflow records in the application
@app.post("/predict")
async def predict(app_data: Application):
    try:
        prediction = predict_eligibility(app_data.cash_flow)
        return {"eligible": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)