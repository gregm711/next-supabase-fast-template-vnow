from app.services.calls import CallService
from fastapi import Depends, HTTPException, Request
from sqlmodel import Session
from app.database import get_session
from app.repositories.calls import CallRepository


def get_call_repository(db_session: Session = Depends(get_session)) -> CallRepository:
    return CallRepository(session=db_session)


def get_call_service(
    call_repository: CallRepository = Depends(get_call_repository),
) -> CallService:
    return CallService(call_repository=call_repository)


def get_current_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="No authenticated user found")
    return user


def get_current_user_id(request: Request):
    user = get_current_user(request)
    return user.get("sub")
