from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from app.models import Call
from sqlalchemy import text


class CallRepository:
    def __init__(self, session: Session):
        self.session = session

    def health_check(self) -> bool:
        try:
            # Run a basic query to make sure this is working.
            statement = select(Call).limit(1)
            results = self.session.exec(statement)
            results.all()
            return True
        except Exception:
            return False

    def get_call(self, call_id: UUID) -> Optional[Call]:
        call = self.session.get(Call, call_id)
        return call

    def get_call_by_sid(self, sid: str) -> Optional[Call]:
        statement = select(Call).where(Call.sid == sid)
        result = self.session.exec(statement).first()
        return result

    def create_call(self, call: Call) -> Call:
        self.session.add(call)
        self.session.commit()
        self.session.refresh(call)
        return call

    def update_call(self, call_id: UUID, call_update: Call) -> Optional[Call]:
        call = self.session.get(Call, call_id)
        if not call:
            return None

        for key, value in call_update.model_dump(exclude_unset=True).items():
            setattr(call, key, value)

        self.session.commit()
        self.session.refresh(call)
        return call

    def delete_call(self, call_id: UUID) -> bool:
        call = self.session.get(Call, call_id)
        if not call:
            return False
        self.session.delete(call)
        self.session.commit()
        return True
