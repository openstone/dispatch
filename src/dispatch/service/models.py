from datetime import datetime
from pydantic import Field
from dispatch.models import EvergreenBase, EvergreenMixin, PrimaryKey

from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy_utils import TSVectorType

from dispatch.database.core import Base
from dispatch.models import TimeStampMixin, ProjectMixin, Pagination
from dispatch.project.models import ProjectRead
from dispatch.search_filter.models import SearchFilterRead


assoc_service_filters = Table(
    "assoc_service_filters",
    Base.metadata,
    Column("service_id", Integer, ForeignKey("service.id", ondelete="CASCADE")),
    Column("search_filter_id", Integer, ForeignKey("search_filter.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("service_id", "search_filter_id"),
)


# SQLAlchemy models...
class Service(Base, TimeStampMixin, ProjectMixin, EvergreenMixin):
    __table_args__ = (UniqueConstraint("external_id", "project_id"),)
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    name = Column(String)
    type = Column(String, default="pagerduty-oncall")
    description = Column(String)
    external_id = Column(String)
    health_metrics = Column(Boolean, default=False)
    shift_hours_type = Column(Integer, default=24)

    # Relationships
    filters = relationship("SearchFilter", secondary=assoc_service_filters, backref="services")

    search_vector = Column(TSVectorType("name", regconfig="pg_catalog.simple"))


# Pydantic models...
class ServiceBase(EvergreenBase):
    description: str | None = None
    external_id: str | None = None
    health_metrics: bool | None = None
    is_active: bool | None = None
    name: str | None = None
    type: str | None = None
    shift_hours_type: int | None = Field(24, nullable=True)


class ServiceCreate(ServiceBase):
    filters: list[SearchFilterRead | None] = []
    project: ProjectRead


class ServiceUpdate(ServiceBase):
    filters: list[SearchFilterRead | None] = []


class ServiceRead(ServiceBase):
    id: PrimaryKey
    filters: list[SearchFilterRead | None] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ServicePagination(Pagination):
    items: list[ServiceRead] = []
