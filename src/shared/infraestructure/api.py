from fastapi import APIRouter, Request, Response

router = APIRouter()

@router.get("/")
def read_root():
    return {"msg": "HelloWorld"}