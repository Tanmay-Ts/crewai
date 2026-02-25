import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

# Load env
load_dotenv(override=True)

# Crew / worker imports
from celery_app import celery_app
from celery.result import AsyncResult
from worker import process_document
from database import init_db

# =========================
# App setup
# =========================
app = FastAPI(title="Financial Document Analyzer")

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize database
init_db()


# =========================
# Helper: save uploaded file
# =========================
async def save_upload_file(upload_file: UploadFile) -> str:
    try:
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(upload_file.filename)[1]
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")

        contents = await upload_file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return file_path

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")


# =========================
# API: Submit analysis job
# =========================
@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(...),
):
    """
    Upload a financial PDF and start background analysis.
    Returns a Celery task_id for status tracking.
    """
    try:
        # Save file locally
        file_path = await save_upload_file(file)

        # Send job to Celery worker
        task = process_document.delay(file_path, query)

        return JSONResponse(
            content={
                "status": "processing",
                "task_id": task.id,
                "message": "Analysis started in background",
                "file_path": file_path,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# API: Check task status
# =========================
@app.get("/status/{task_id}")
def get_status(task_id: str):
    """
    Check background task status.
    """
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == "PENDING":
        return {"status": "pending"}

    if task_result.state == "SUCCESS":
        return {
            "status": "completed",
            "result": task_result.result,
        }

    if task_result.state == "FAILURE":
        return {
            "status": "failed",
            "error": str(task_result.result),
        }

    return {"status": task_result.state}


# =========================
# Health check
# =========================
@app.get("/")
def root():
    return {"message": "Financial Document Analyzer is running 🚀"}


# =========================
# Local run
# =========================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Windows-stable
    )