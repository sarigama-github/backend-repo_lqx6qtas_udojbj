import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

from database import db, create_document, get_documents
from schemas import Harvest, Investment

app = FastAPI(title="Lobster Harvest & Investing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Lobster Harvest & Investing API"}

# Schema exposure for tooling
@app.get("/schema")
def get_schema():
    return {
        "harvest": Harvest.model_json_schema(),
        "investment": Investment.model_json_schema(),
    }

# Health + DB test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or "Unknown"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Create endpoints (use new field names to avoid pydantic date clash)
@app.post("/harvest")
def create_harvest(payload: Harvest):
    try:
        inserted_id = create_document("harvest", payload)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/harvest")
def list_harvest(limit: Optional[int] = 100):
    try:
        docs = get_documents("harvest", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
            for k, v in list(d.items()):
                if isinstance(v, (date,)):
                    d[k] = v.isoformat()
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/investment")
def create_investment(payload: Investment):
    try:
        inserted_id = create_document("investment", payload)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/investment")
def list_investments(limit: Optional[int] = 100):
    try:
        docs = get_documents("investment", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
            for k, v in list(d.items()):
                if isinstance(v, (date,)):
                    d[k] = v.isoformat()
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
