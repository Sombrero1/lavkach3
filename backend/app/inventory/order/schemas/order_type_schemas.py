from datetime import datetime
from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field
from pydantic.types import UUID4

from app.inventory.location.enums import PutawayStrategy
from core.schemas import BaseFilter
from core.schemas.list_schema import GenericListSchema
from core.schemas.timestamps import TimeStampScheme
from app.inventory.order.models import OrderType
from app.inventory.order.models.order_models import OrderClass, BackOrderAction, ReservationMethod



class OrderTypeBaseScheme(BaseModel):
    vars: Optional[dict] = None
    prefix: str
    order_class: OrderClass
    title: str
    allowed_location_src_ids: Optional[list[UUID4]] = None
    exclusive_location_src_ids: Optional[list[UUID4]] = None
    allowed_location_dest_ids: Optional[list[UUID4]] = None
    exclusive_location_dest_ids: Optional[list[UUID4]] = None
    backorder_order_type_id: Optional[UUID4] = None
    backorder_action_type: BackOrderAction
    store_id: Optional[UUID4] = None
    partner_id: Optional[UUID4] = None
    reservation_time_before: Optional[int] = None
    allowed_package_ids: Optional[list[UUID4]] = None
    exclusive_package_ids: Optional[list[UUID4]] = None
    is_homogeneity: bool = False
    is_allow_create_package: bool = True
    is_can_create_order_manualy: bool = True
    is_overdelivery: bool = False
    barcode: str
    created_by: UUID4
    edited_by: UUID4
    reservation_method: ReservationMethod

class OrderTypeUpdateScheme(OrderTypeBaseScheme):
    prefix: Optional[str] = None
    backorder_action_type: BackOrderAction = BackOrderAction.ASK
    strategy: PutawayStrategy = PutawayStrategy.FEFO
    reservation_method: ReservationMethod = ReservationMethod.AT_CONFIRM
    title: str = None
    barcode: str = None
    created_by: UUID4 = None
    edited_by: UUID4 = None


class OrderTypeCreateScheme(OrderTypeBaseScheme):
    company_id: UUID4


class OrderTypeScheme(OrderTypeCreateScheme, TimeStampScheme):
    lsn: int
    id: UUID4
    created_by: UUID4
    edited_by: UUID4

    class Config:
        orm_mode = True


class OrderTypeFilter(BaseFilter):
    store_id__in: Optional[List[UUID4]] = Field(alias="store_id", default=None)

    class Config:
        populate_by_name = True

    class Constants(Filter.Constants):
        model = OrderType
        ordering_field_name = "order_by"
        search_field_name = "search"
        search_model_fields = ["title", "barcode"]


class OrderTypeListSchema(GenericListSchema):
    data: Optional[List[OrderTypeScheme]]
