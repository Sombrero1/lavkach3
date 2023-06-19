from app.store.models.store_models import Store
from app.store.schemas.store_schemas import StoreCreateScheme, StoreUpdateScheme
from core.db.session import session
from core.service.base import BaseService


class StoreService(BaseService[Store, StoreCreateScheme, StoreUpdateScheme]):
    def __init__(self, db_session: session=session):
        super(StoreService, self).__init__(Store, db_session)


