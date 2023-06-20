from pydantic import BaseModel, Field, UUID4
from pydantic.types import Optional
from core.schemas.timestamps import TimeStampScheme
from core.types.types import TypeCountry, TypePhone, TypeLocale, TypeCurrency
from app.basic.partner.models.partner_models import PartnerType

class PartnerBaseScheme(BaseModel):
    title: str = Field(description="Title")
    type: PartnerType
    external_id: Optional[str]
    parent_id: Optional[str]
    phone_number: Optional[TypePhone]
    email: Optional[str]
    country: Optional[TypeCountry]
    locale: Optional[TypeLocale]
    currency: Optional[TypeCurrency]


class PartnerUpdateScheme(PartnerBaseScheme):
    pass


class PartnerCreateScheme(PartnerBaseScheme):
    pass

class PartnerParent(PartnerBaseScheme, TimeStampScheme):
    id: UUID4
    lsn: int
    country: TypeCountry
    locale: TypeLocale
    currency: TypeCurrency

class PartnerScheme(PartnerParent, TimeStampScheme):
    partner: Optional[PartnerParent]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
