from __future__ import annotations
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING, Any
from datetime import date

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field, field_validator, model_validator, model_serializer, computed_field
from pydantic.types import UUID4

from app.inventory.location.enums import PutawayStrategy
from app.inventory.order.schemas.move_schemas import MoveScheme
from core.schemas import BaseFilter
from core.schemas.filter_generic import CustomBaseModel

from core.schemas.list_schema import GenericListSchema
from core.schemas.timestamps import TimeStampScheme
from app.inventory.order.models import Order
from app.inventory.order.models.order_models import OrderStatus
from app.inventory.order.schemas.order_type_schemas import OrderTypeScheme


class OrderBaseScheme(CustomBaseModel):
    vars: Optional[dict] = None
    number: str
    order_id: Optional[UUID4] = Field(default=None, title='Parent', table=True, form=True)
    external_number: Optional[str] = Field(default=None, title='External ID', table=True, form=True)
    store_id: UUID4 = Field(title='Store', table=True, form=True)
    partner_id: Optional[UUID4] = Field(default=None, title='Partner', table=True, form=True)
    lot_id: Optional[UUID4] = Field(default=None, title='Lot', table=True, form=True)
    order_type_id: UUID4 = Field(title='Order Type', form=True)
    origin_type: Optional[str] = Field(default=None, title='Original Type', table=True, form=True)
    origin_number: Optional[str] = Field(default=None, title='Original', table=True, form=True)
    planned_date: Optional[datetime] = Field(default=None, title='Planned Date', table=True, form=True)
    actual_date: Optional[datetime] = Field(title='Actual Date', table=True, form=True)
    expiration_datetime: Optional[datetime] = Field(default=None, title='Expiration Date', table=True, form=True)
    users_ids: Optional[list[UUID4]] = Field(default=[], title='Users', form=True)
    description: Optional[str] = Field(default=None, title='Description', table=True, form=True)
    status: OrderStatus = Field(title='Status', table=True, form=True)
    created_by: UUID4 = Field(title='Created By', table=True)
    edited_by: UUID4 = Field(title='Edit By', table=True)


class OrderUpdateScheme(OrderBaseScheme):
    ...


class OrderCreateScheme(OrderBaseScheme):
    ...

    class Config:
        extra = 'allow'


class OrderScheme(OrderCreateScheme, TimeStampScheme):
    lsn: int
    id: UUID4
    company_id: UUID4
    move_list_rel: Optional[list[MoveScheme]] = Field(default=[], title='Order Movements', form=True)
    order_type_rel: OrderTypeScheme = Field(title='Order Type', table=True, form=True)


    @computed_field
    def title(self) -> str:
        return f'{self.order_type_rel.title}: [{self.number}]'

    class Config:
        orm_mode = True


def empty_erray(val):
    if val:
        return val


class OrderFilter(BaseFilter):
    planned_date__gte: Optional[datetime] = Field(description="bigger or equal planned date", default=None, filter=True)
    planned_date__lt: Optional[datetime] = Field(description="less planned date", default=None, filter=True)
    status__in: Optional[List[OrderStatus]] = Field(default=None, filter=True)
    store_id__in: Optional[List[UUID4]] = Field(default=None, filter=True)
    order_type_id__in: Optional[List[UUID4]] = Field(default=None, filter=True)

    class Constants(Filter.Constants):
        model = Order
        ordering_field_name = "order_by"
        search_model_fields = ["external_number", "origin_number", "number"]


class OrderListSchema(GenericListSchema):
    data: Optional[List[OrderScheme]]
