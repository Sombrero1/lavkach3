from sqlalchemy import Column, Unicode, BigInteger, Boolean, UUID, ForeignKey

from core.db import Base
from core.db.mixins import TimestampMixin, CompanyMixin
import uuid
from enum import Enum

class UserType(str, Enum):
    COMMON: str = 'common'
    STORE: str = 'store'
    COURIER: str = 'courier'

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    nickname = Column(Unicode(255), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    type = Column(Unicode(20), nullable=False, default=UserType.COMMON)
