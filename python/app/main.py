from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI()

# Include the API router
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Content Generation API started"}
