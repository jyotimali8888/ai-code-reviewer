from pathlib import Path

from fastapi import FastAPI, HTTPException
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
    path = Path(request.path)

    if not path.exists():
        raise HTTPException(
            status_code=400,
            detail="The specified path does not exist."
        )

    if not path.is_dir():
        raise HTTPException(
            status_code=400,
            detail="The specified path is not a directory."
        )

    result = scan_repository(request.path)

    return result