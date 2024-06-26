from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field
from pydantic.types import UUID4

from app.inventory.location.enums import PutawayStrategy, LocationClass
from app.inventory.order.models import OrderType
from app.inventory.order.models.order_models import OrderClass, BackOrderAction, ReservationMethod
from core.schemas import BaseFilter
from core.schemas.list_schema import GenericListSchema
from core.schemas.timestamps import TimeStampScheme


class OrderTypeBaseScheme(BaseModel):
    prefix: str = Field(title='Prefix', table=True, form=True)
    order_class: OrderClass = Field(title='Order Class', table=True, form=True)
    title: str = Field(title='Titile', table=True, form=True)
    allowed_location_src_ids: Optional[list[UUID4]] = Field(
        default=[], model='location',
        title='Allowed locations source'
    )
    exclude_location_src_ids: Optional[list[UUID4]] = Field(
        default=[], model='location',
        title='Exclude locations source'
    )
    allowed_location_dest_ids: Optional[list[UUID4]] = Field(
        default=[], model='location',
        title='Allowed locations dest'
    )
    exclude_location_dest_ids: Optional[list[UUID4]] = Field(
        default=[], model='location',
        title='Exclude locations dest'
    )
    allowed_location_type_src_ids: Optional[list[UUID4]] = Field(
        default=[], model='location_type',
        title='Allowed locations type source',
    )
    exclude_location_type_src_ids: Optional[list[UUID4]] = Field(
        default=[], model='location_type',
        title='Exclude locations type source'
    )
    allowed_location_type_dest_ids: Optional[list[UUID4]] = Field(
        default=[], model='location_type',
        title='Allowed locations type dest',
    )
    exclude_location_type_dest_ids: Optional[list[UUID4]] = Field(
        default=[], model='location_type',
        title='Exclude locations type dest '
    )
    allowed_location_class_src_ids: Optional[list[LocationClass]] = Field(
        default=[],
        title='Allowed locations class source'
    )
    exclude_location_class_src_ids: Optional[list[LocationClass]] = Field(
        default=[],
        title='Exclude locations class source',
    )
    allowed_location_class_dest_ids: Optional[list[LocationClass]] = Field(
        default=[],
        title='Allowed locations class dest '
    )
    exclude_location_class_dest_ids: Optional[list[LocationClass]] = Field(
        default=[],
        title='Exclude locations class dest ',
    )
    order_type_id: Optional[UUID4] = Field(default=None, title='Back Order', form=True, model='order_type')
    backorder_action_type: BackOrderAction = Field(default=BackOrderAction.ASK, title='Backorder action', form=True)
    store_id: Optional[UUID4] = Field(default=None, title='Store', table=True, form=True, model='store')
    partner_id: Optional[UUID4] = Field(default=None, title='Partner', table=True, form=True, model='partner')
    reservation_time_before: Optional[int] = Field(default=None, title='Reserve time before', form=True)
    allowed_package_ids: Optional[list[UUID4]] = Field(default=[], model='location', title='Allowed packages dest',
                                                       form=True)
    exclude_package_ids: Optional[list[UUID4]] = Field(default=[], model='location', title='Exclude packages dest',
                                                       form=True)
    is_homogeneity: bool = Field(default=False, title='Is homogeneity', form=True)
    is_allow_create_package: bool = Field(default=True, title='Is allow create package', form=True)
    is_can_create_order_manualy: bool = Field(default=True, title='Can create order manualy', form=True)
    is_overdelivery: bool = Field(default=False, title='Is overdelivery', form=True)
    barcode: str = Field(title='Barcode', table=True, form=True)
    reservation_method: ReservationMethod = Field(default=ReservationMethod.AT_CONFIRM, title='Reservation method',
                                                  table=True, form=True)
    strategy: PutawayStrategy = Field(default=PutawayStrategy.FEFO, title='Strategy', form=True)

    class Config:
        extra = 'allow'
        from_attributes = True
        orm_model = OrderType


class OrderTypeUpdateScheme(OrderTypeBaseScheme):
    ...


class OrderTypeCreateScheme(OrderTypeBaseScheme):
    ...


class OrderTypeScheme(OrderTypeCreateScheme, TimeStampScheme):
    vars: Optional[dict] = None
    company_id: UUID4 = Field(model='company', title='Company')
    lsn: int
    id: UUID4
    created_by: UUID4 = Field(model='user')
    edited_by: UUID4 = Field(model='user')


class OrderTypeFilter(BaseFilter):
    store_id__in: Optional[List[UUID4]] = Field(default=None, model='store')

    class Config:
        populate_by_name = True

    class Constants(Filter.Constants):
        model = OrderType
        ordering_field_name = "order_by"
        search_field_name = "search"
        search_model_fields = ["title", "barcode"]


class OrderTypeListSchema(GenericListSchema):
    data: Optional[List[OrderTypeScheme]]
