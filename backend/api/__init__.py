from fastapi import APIRouter
from .payment import router as payment_router
from .admin import router as admin_router
from .analyze import router as analyze_router

router = APIRouter()

router.include_router(payment_router, prefix="/payment", tags=["payment"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(analyze_router, prefix="/analyze", tags=["analyze"]) 