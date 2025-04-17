from fastapi import APIRouter
from api.admin import router as admin_router

router = APIRouter()
router.include_router(admin_router, prefix="/admin", tags=["admin"]) 