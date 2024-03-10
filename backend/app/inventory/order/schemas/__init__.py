from pydantic import BaseModel

from .order_schemas import (
    OrderBaseScheme,
OrderCreateScheme,
    OrderUpdateScheme,
    OrderScheme,
    OrderFilter,
    OrderListSchema
)
from .order_type_schemas import (
    OrderTypeBaseScheme,
OrderTypeCreateScheme,
    OrderTypeUpdateScheme,
    OrderTypeScheme,
    OrderTypeFilter,
    OrderTypeListSchema
)


class ExceptionResponseSchema(BaseModel):
    error: str
