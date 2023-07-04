import uuid

from sqlalchemy import Column, Unicode, BigInteger, Uuid, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy_utils import CurrencyType, CountryType, LocaleType

from core.db import Base
from core.db.mixins import TimestampMixin


class Company(Base, TimestampMixin):
    __tablename__ = "company"
    lsn_seq = Sequence(f'company_lsn_seq')
    lsn = Column(BigInteger, lsn_seq, onupdate=lsn_seq.next_value(), index=True)
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(Unicode(255), nullable=False, index=True)
    external_id = Column(Unicode(255), nullable=True, unique=True)
    country = Column(CountryType, default='US')
    locale = Column(LocaleType, default='en_US')
    currency = Column(CurrencyType, nullable=False, default="USD")
    stores = relationship("Store", lazy='selectin', back_populates="company")
