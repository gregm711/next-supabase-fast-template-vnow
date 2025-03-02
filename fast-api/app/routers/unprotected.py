from app.dependencies import get_call_service, get_current_user_id
from fastapi import APIRouter, Request, WebSocket, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from app.services.calls import (
    CallService,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/unprotected",  # bring this back after testing and when we can change on twilio
    tags=["unprotected"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def some_unprotected_endpoint():
    return JSONResponse(content={"message": "Hello, world!"})
