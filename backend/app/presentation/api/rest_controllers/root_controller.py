import logging
from fastapi import APIRouter, HTTPException

router = APIRouter()

class RootRequestError(Exception):
    pass

@router.get("/")
async def root():
    try:
        # Logic to check for redirects or generate a welcome message
        return {"message": "Welcome to the API!"}
    except Exception as e:
        logging.error(f"Error handling root request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
