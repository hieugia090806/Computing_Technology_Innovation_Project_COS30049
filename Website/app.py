from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import re
from datetime import datetime
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS CONFIGURATION ---
# Allows the frontend (React/Vue/Figma prototype) to connect to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- IN-MEMORY DATABASE ---
# Stores real-time scan history for the Dashboard analytics
db_history = []

# --- LOAD MACHINE LEARNING MODELS ---
try:
    # Ensure these paths match your Backend/Model/ folder structure
    spam_pack = joblib.load('Backend/Model/spam_file_scanner.pkl')
    malware_pack = joblib.load('Backend/Model/malware_rf_model.pkl')
    news_pack = joblib.load('Backend/Model/ultimate_news_detector.pkl')

    # Assigning specific components based on your previous checks
    rf_spam, vec_spam = spam_pack['model'], spam_pack['cv']
    rf_malware, vec_malware = malware_pack['model'], malware_pack['vectorizer']
    rf_news, vec_news = news_pack['model'], news_pack['vectorizer']
    print("✅ Successfully loaded all models and vectorizers.")
except Exception as e:
    print(f"❌ Critical Error loading models: {e}")

# --- DATA MODELS ---
class ScanRequest(BaseModel):
    content: str

# --- API ENDPOINTS ---

@app.post("/scan")
async def scan_content(request: ScanRequest):
    """
    Analyzes the input string and classifies it as Spam, Malware, or News.
    Saves the result to history for real-time dashboard updates.
    """
    user_input = request.content
    if not user_input:
        raise HTTPException(status_code=400, detail="Input content is empty")

    # Smart Classification Logic
    if re.search(r'http|www|\.com|\.net|\.org|/', user_input):
        # Website/Link Classification
        X = vec_news.transform([user_input.lower()])
        pred = rf_news.predict(X)[0]
        label = "REAL" if str(pred).lower() in ['real', 'safe'] else "FAKE"
        category = "Link/News Detection"
    
    elif re.search(r'import |def |eval\(|os\.|script|{|}|;', user_input):
        # Source Code/Malware Classification
        X = vec_malware.transform([user_input.lower()])
        pred = rf_malware.predict(X)[0]
        label = "MALICIOUS" if str(pred) == '1' else "SAFE"
        category = "Malware Analysis"
    
    else:
        # Standard Text/Spam Classification
        X = vec_spam.transform([user_input.lower()])
        pred = rf_spam.predict(X)[0]
        label = "SPAM" if str(pred).lower() in ['1', 'spam'] else "HAM (SAFE)"
        category = "Spam Filter"

    # Save to history for Analytics
    entry = {
        "id": len(db_history) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "result": label,
        "content_preview": user_input[:40] + "..." if len(user_input) > 40 else user_input
    }
    db_history.append(entry)

    return entry

@app.get("/analytics/figures")
async def get_dashboard_figures():
    """
    Returns data formatted for Pie Charts and Bar Charts.
    Used by Frontend to render real-time analytics.
    """
    if not db_history:
        return {"message": "No data available yet. Start scanning!"}

    # Count categories for Pie Chart
    cat_counts = dict(Counter(item['category'] for item in db_history))
    
    # Calculate Threat vs Safe ratio
    results = [item['result'] for item in db_history]
    threat_summary = {
        "Threats": sum(1 for r in results if r in ["SPAM", "MALICIOUS", "FAKE"]),
        "Safe": sum(1 for r in results if r in ["HAM (SAFE)", "SAFE", "REAL"])
    }

    return {
        "category_distribution": cat_counts,
        "safety_ratio": threat_summary,
        "total_scanned": len(db_history)
    }

@app.get("/analytics/table")
async def get_recent_history():
    """
    Returns the most recent scan records for the UI table.
    """
    # Returns last 15 records, newest first
    return db_history[-15:][::-1]