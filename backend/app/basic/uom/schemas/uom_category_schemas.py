from datetime import datetime

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field, UUID4
from typing import Optional, List
from app.basic.uom.models.uom_category_models import UomCategory
from core.schemas import BaseFilter
from core.schemas.list_schema import GenericListSchema
from core.schemas.timestamps import TimeStampScheme


class UomCategoryBaseScheme(BaseModel):
    title: str = Field(description="Title")


class UomCategoryUpdateScheme(UomCategoryBaseScheme):
    pass


class UomCategoryCreateScheme(UomCategoryBaseScheme):
    company_id: UUID4


class UomCategoryScheme(UomCategoryCreateScheme, TimeStampScheme):
    id: UUID4
    lsn: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UomCategoryFilter(BaseFilter):
    title__in: Optional[str] = Field(default='', description="title")

    class Config:
        populate_by_name = True

    class Constants(Filter.Constants):
        model = UomCategory
        ordering_field_name = "order_by"
        search_field_name = "search"
        search_model_fields = ["title"]


class UomCategoryListSchema(GenericListSchema):
    data: Optional[List[UomCategoryScheme]]
