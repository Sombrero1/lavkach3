import uuid
from typing import TypeVar

from pydantic import BaseModel, Field
from pydantic.types import UUID4, List
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from app.maintenance.models import AssetStatus
from app.maintenance.models.maintenance_models import AssetLog
from app.maintenance.schemas.asset_log_schemas import AssetLogBaseScheme
from app.maintenance.schemas.asset_type_schemas import AssetTypeScheme
from app.maintenance.schemas.manufacturer_schemas import ManufacturerScheme
from app.maintenance.schemas.model_schemas import ModelScheme
from app.maintenance.schemas.order_schemas import OrderScheme
from app.basic.store.schemas import StoreScheme
from app.basic.user.schemas import GetUserListResponseSchema
from core.db.session import Base, session
from core.service.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)
from core.schemas.timestamps import TimeStampScheme

class AssetLo(BaseModel):
    async def create(self) -> ModelType:
        entity = self.Config.model(**self.dict())
        session.add(entity)


        try:
            await session.commit()
            await session.refresh(entity)
        except IntegrityError as e:
            await session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(status_code=409, detail=f"Conflict Error entity {str(e)}")
            else:
                raise e
        except Exception as e:
            raise HTTPException(status_code=409, detail=f"Conflict Error entity {str(e)}")
        else:
            log = AssetLog(
                asset_id=entity.id,
                action='init',
                from_=None,
                to=None,
            )
            session.add(log)
            await session.commit()
            await session.refresh(entity)

        return entity

    async def update(
        self,
        id: uuid.UUID,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        entity = await self.get_by_id(id.__str__())

        query = (
            update(self.Config.model)
            .where(self.Config.model.id == id.__str__())
            .values(**self.dict())
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)
        changes = dict(self)
        if 'store_id' in changes and entity.store_id != changes['store_id']:
            log = AssetLog(
                asset_id=id,
                action='store_id',
                from_=str(entity.store_id),
                to=str(changes['store_id']),
            )
            session.add(log)
        if 'status' in changes and entity.status != changes['status']:
            log = AssetLog(
                asset_id=id,
                action='status',
                from_=str(entity.store_id),
                to=str(changes['status']),
            )
            session.add(log)
        if 'at_user_id' in changes and entity.at_user_id != changes['at_user_id']:
            log = AssetLog(
                asset_id=id,
                action='at_user_id',
                from_=str(entity.at_user_id),
                to=str(changes['at_user_id']),
            )
            session.add(log)
        await session.commit()
        #await session.refresh(entity)
        entity = await self.get_by_id(id.__str__())
        return entity


class AssetBaseScheme(AssetLo):
    title: str = Field(description="Title")
    company_id: UUID4
    asset_type_id: UUID4
    manufacturer_id: UUID4
    store_id: UUID4
    model_id: UUID4
    status: AssetStatus
    at_user_id: UUID4
    user_created_id: UUID4
    barcode: str

class AssetUpdateScheme(AssetBaseScheme):
    pass
class AssetCreateScheme(AssetBaseScheme):
    pass
class AssetScheme(AssetCreateScheme, TimeStampScheme):
    id: UUID4
    lsn: int
    asset_type: AssetTypeScheme
    manufacturer: ManufacturerScheme
    store: StoreScheme
    model: ModelScheme
    user_created: GetUserListResponseSchema
    at_user: GetUserListResponseSchema
    orders: List[OrderScheme]
    asset_logs: List[AssetLogBaseScheme]
    class Config:
        orm_mode = True
