import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.inventory.location.enums import LocationClass


class LocationMixin:
    store_id: Mapped[uuid.UUID] = mapped_column(Uuid, index=True)
    location_class: Mapped[LocationClass] = mapped_column(index=True)
    lot_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("lot.id", ondelete="SET NULL"), index=True)
    partner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, index=True, nullable=True)


class StockMixin(LocationMixin):
    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, index=True)
    location_type_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("location_type.id", ondelete="SET NULL"), index=True)
    location_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("location.id", ondelete="SET NULL"), index=True)