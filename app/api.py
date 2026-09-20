from fastapi import FastAPI
from pydantic import BaseModel

from app.analyzer import scan_repository


app = FastAPI()


class ReviewRequest(BaseModel):
    path: str


@app.get("/")
def home():
    return {
        "message": "AI Code Reviewer API is running"
    }


@app.post("/review")
def review(request: ReviewRequest):
    result = scan_repository(request.path)
    return result