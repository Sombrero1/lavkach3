from fastapi import APIRouter

from app.basic.user.api.user_api import user_router
from app.basic.partner.api.partner_api import partner_router
from app.basic.auth.api.auth import auth_router
from app.basic.company.api.company_api import company_router
from app.basic.store.api.store_api import store_router
from .maintenance.api.manufacturer_api import manufacturer_router
from .maintenance.api.asset_log_api import asset_log_router
from .maintenance.api.asset_type_api import asset_type_router
from .maintenance.api.asset_api import asset_router
from .maintenance.api.model_api import model_router
from .maintenance.api.order_api import order_router

router = APIRouter()
router.include_router(user_router, prefix="/api/users", tags=["User"])
router.include_router(partner_router, prefix="/api/partner", tags=["Partner"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(company_router, prefix="/api/company", tags=["Company"])
router.include_router(store_router, prefix="/api/store", tags=["Store"])
router.include_router(manufacturer_router, prefix="/api/manufacturer", tags=["Manufacturer"])
router.include_router(model_router, prefix="/api/model", tags=["Model"])
router.include_router(asset_type_router, prefix="/api/assets_type", tags=["AssetType"])
router.include_router(asset_router, prefix="/api/asset", tags=["Asset"])
router.include_router(asset_log_router, prefix="/api/asset_log", tags=["AssetLog"])
router.include_router(order_router, prefix="/api/order", tags=["Order"])



__all__ = ["router"]
