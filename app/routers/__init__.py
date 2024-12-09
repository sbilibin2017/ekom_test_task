from fastapi import APIRouter

from app.routers.form import router as form_router

router = APIRouter()

router.include_router(form_router)
