import datetime as dt
import uuid
from uuid import UUID
from enum import Enum

from sqlalchemy import bindparam
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import false
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy

from db.base import Base


class BaseMixin:
    @declared_attr.directive
    def __tablename__(cls):
        letters = ['_' + i.lower() if i.isupper() else i for i in cls.__name__]
        return ''.join(letters).lstrip('_') + 's'

    created_at: M[dt.datetime] = column(server_default=func.now())
    updated_at: M[dt.datetime | None] = column(nullable=True, onupdate=func.now())
    id: M[int] = column(primary_key=True, index=True)


class User(BaseMixin, Base):
    id: M[int] = column(primary_key=True, type_=BIGINT())
    age: M[int]
    gender: M[str]


class Mailing(BaseMixin, Base):
    min_age: M[int | None]
    max_age: M[int | None]
    gender: M[str | None]
    text: M[str]

