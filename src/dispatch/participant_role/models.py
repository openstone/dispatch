from datetime import datetime


from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from dispatch.database.core import Base
from dispatch.models import DispatchBase, PrimaryKey

from .enums import ParticipantRoleType


class ParticipantRole(Base):
    id = Column(Integer, primary_key=True)
    assumed_at = Column(DateTime, default=datetime.utcnow)
    renounced_at = Column(DateTime)
    role = Column(String, default=ParticipantRoleType.participant)
    activity = Column(Integer, default=0)
    participant_id = Column(Integer, ForeignKey("participant.id", ondelete="CASCADE"))


# Pydantic models...
class ParticipantRoleBase(DispatchBase):
    role: str


class ParticipantRoleCreate(ParticipantRoleBase):
    role: ParticipantRoleType


class ParticipantRoleUpdate(ParticipantRoleBase):
    pass


class ParticipantRoleRead(ParticipantRoleBase):
    id: PrimaryKey
    assumed_at: datetime | None = None
    renounced_at: datetime | None = None
    activity: int | None = None


class ParticipantRoleReadMinimal(ParticipantRoleRead):
    pass


class ParticipantRolePagination(ParticipantRoleBase):
    items: list[ParticipantRoleRead] = []
