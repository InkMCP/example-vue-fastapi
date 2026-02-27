from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()

# In-memory items store
items = [
    {"id": 1, "name": "First item", "created_at": datetime.now().isoformat()},
    {"id": 2, "name": "Second item", "created_at": datetime.now().isoformat()},
]
next_id = 3


class ItemCreate(BaseModel):
    name: str


@app.get("/api/items")
def list_items():
    return items


@app.post("/api/items", status_code=201)
def create_item(item: ItemCreate):
    global next_id
    if not item.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")
    new_item = {
        "id": next_id,
        "name": item.name.strip(),
        "created_at": datetime.now().isoformat(),
    }
    next_id += 1
    items.append(new_item)
    return new_item


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    global items
    items = [i for i in items if i["id"] != item_id]
    return {"ok": True}


# Serve frontend static files in production
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        return FileResponse(os.path.join(frontend_dist, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
