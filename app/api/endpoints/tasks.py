from fastapi import APIRouter


router = APIRouter(
    prefix="/task",
)

@router.get("/")
def index():
    return {"status": "fastapi task_manager service is running."}