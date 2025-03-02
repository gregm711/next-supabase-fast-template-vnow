import datetime
from uuid import UUID, uuid4
from sqladmin import ModelView
from sqlmodel import Field, SQLModel
from typing import Optional

from app.enums import CallStatus


# ORM model
class Call(SQLModel, table=True):
    __tablename__ = "calls"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    sid: str
    from_number: str
    to_number: str
    status: CallStatus = Field(default=CallStatus.INITIALIZED)
    eleven_labs_conversation_id: Optional[str] = None


# Admin Dashboard ModelView. This can be modified so that only certain fields are displayed or modifiable.
class CallAdmin(ModelView, model=Call):
    column_list = [
        Call.id,
        Call.sid,
        Call.from_number,
        Call.to_number,
        Call.created_at,
        Call.updated_at,
        Call.status,
        Call.eleven_labs_conversation_id,
    ]
    name_plural = "Calls"
