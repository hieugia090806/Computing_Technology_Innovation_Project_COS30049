from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from datetime import datetime
from models_handler import handler
from classifier import input_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Swinburne Security Showcase API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    content: str

@app.get("/")
async def root():
    return {"message": "Backend is Live", "docs": "/docs", "status": 200}

@app.post("/analyze")
async def analyze(request: ScanRequest):
    """
    Main Endpoint for Frontend.
    Returns all vital metrics for Figma UI components.
    """
    try:
        category, ai_results = input_router.predict_logic(request.content, handler)
        
        # Wrapping everything for a professional Frontend Showcase
        return {
            "meta": {
                "scan_id": id(request.content),
                "timestamp": datetime.now().isoformat(),
                "category_detected": category
            },
            "ui_metrics": ai_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)