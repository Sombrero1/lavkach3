from fastapi import APIRouter, Depends
from app.bff.bff import index_router
from app.bff.apps.basic.basic_router import basic_router


bff_router = APIRouter()
bff_router.include_router(index_router, prefix="", tags=["frontend"])
bff_router.include_router(basic_router, prefix="/basic", tags=["frontend"])




