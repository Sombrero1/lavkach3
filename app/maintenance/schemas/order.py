from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field, HttpUrl, conint
from pydantic.types import UUID4, condecimal, constr, Decimal
from app.maintenance.models import Order, OrderLine, OrderStatus
from core.repository.base import BaseRepo
from app.store.schemas import StoreSchema
from app.user.schemas import GetUserListResponseSchema
from pydantic import ConfigDict

class OrderLineBaseScheme(BaseModel, BaseRepo):
    title: str
    description:str
    order_id: UUID4
    quantity: Optional[int]
    cost = Optional[condecimal(decimal_places=2)]

    class Config:
        model = OrderLine
        arbitrary_types_allowed = True

class OrderLineUpdateScheme(OrderLineBaseScheme):
    pass

class OrderLineCreateScheme(OrderLineBaseScheme):
    class Config:
        model = OrderLine

class OrderLineScheme(OrderLineCreateScheme):
    id: UUID4
    lsn: int
    store: StoreSchema
    user_created: GetUserListResponseSchema
    supplier_user: GetUserListResponseSchema

    class Config:
        model = OrderLine
        orm_mode = True
        # alias_generator = to_camel
        # allow_population_by_field_name = True

##############################################################################################################
class OrderBaseScheme(BaseModel, BaseRepo):
    description: str
    supplier_id: UUID4
    status: OrderStatus
    asset_id:UUID4
    store_id: UUID4
    user_created_id: UUID4
    supplier_user_id: UUID4
    class Config:
        model = Order
class OrderUpdateScheme(OrderBaseScheme):
    pass
class OrderCreateScheme(OrderBaseScheme):
    order_lines: Optional[OrderLineScheme]
    class Config:
        model = Order

class OrderScheme(OrderCreateScheme):
    id: UUID4
    lsn: int
    number: int
    store: StoreSchema
    user_created: GetUserListResponseSchema
    supplier_user: GetUserListResponseSchema
    #order_lines: OrderLineScheme
    class Config:
        model = Order
        orm_mode = True
        arbitrary_types_allowed = True
        #alias_generator = to_camel
        #allow_population_by_field_name = True
