from datetime import datetime
from typing import Optional, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field
from pydantic.types import UUID4
from app.basic.product.models.product_models import Product
from core.schemas.list_schema import GenericListSchema
from core.schemas.timestamps import TimeStampScheme
from app.basic.company.schemas import CompanyScheme
from app.basic.uom.schemas import UomScheme


class ProductBaseScheme(BaseModel):
    company_id: UUID4
    vars: Optional[dict] = None
    title: str
    description: Optional[str] = None
    external_id: Optional[str] = None
    product_type: str = None
    uom_id: UUID4
    product_category_id: UUID4
    product_storage_type_id: UUID4
    barcodes: list[str]


class ProductUpdateScheme(ProductBaseScheme):
    title: Optional[str] = None
    product_type: Optional[str] = None
    uom_id: UUID4 = None
    product_category_id: UUID4 = None
    product_storage_type_id: UUID4 = None
    barcodes: Optional[list[str]] = None


class ProductCreateScheme(ProductBaseScheme):
    pass


class ProductScheme(ProductCreateScheme, TimeStampScheme):
    lsn: int
    id: UUID4
    company: CompanyScheme
    uom: UomScheme

    class Config:
        orm_mode = True


class ProductFilter(Filter):
    lsn__gt: Optional[int] = Field(alias="cursor")
    id__in: Optional[List[UUID4]] = Field(alias="id")
    created_at_gte: Optional[datetime] = Field(description="bigger or equal created")
    created_at_lt: Optional[datetime] = Field(description="less created")
    updated_at_gte: Optional[datetime] = Field(description="bigger or equal updated")
    updated_at_lt: Optional[datetime] = Field(description="less updated")
    company_id__in: Optional[List[UUID4]] = Field(alias="company_id")
    title__in: Optional[List[str]] = Field(description="title")
    order_by: Optional[List[str]]
    search: Optional[str]

    class Config:
        populate_by_name = True

    class Constants(Filter.Constants):
        model = Product
        ordering_field_name = "order_by"
        search_field_name = "search"
        search_model_fields = ["title", "external_id"]


class ProductListSchema(GenericListSchema):
    data: Optional[List[ProductScheme]]
