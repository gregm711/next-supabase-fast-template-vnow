from app.dependencies import get_call_service, get_current_user_id
from fastapi import APIRouter, Request, WebSocket, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from app.services.calls import (
    CallService,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",  # bring this back after testing and when we can change on twilio
    tags=["calls"],
    responses={404: {"description": "Not found"}},
)


@router.get("/some-unprotected-endpoint")
async def some_unprotected_endpoint():
    return JSONResponse(content={"message": "Hello, world!"})

@router.get("/auth-health-check")
async def health_check(user_id: str = Depends(get_current_user_id)):
    return JSONResponse(content={"message": f"Hello user with id {user_id}!"})


@router.get("/health-check")
async def health_check_endpoint(
    request: Request,
    call_service: CallService = Depends(get_call_service),
) -> JSONResponse:
    res = call_service.repository_health_check()
    return JSONResponse(
        {"status": "up", "database_check": res, "request_host": request.url.hostname}
    )


@router.api_route("/incoming-call-eleven", methods=["GET", "POST"])
async def handle_incoming_call(
    request: Request, call_service: CallService = Depends(get_call_service)
) -> HTMLResponse:
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    from_number = form_data.get("From")
    to_number = form_data.get("To")

    # Combined check for all required fields and their types
    if (
        not call_sid
        or not isinstance(call_sid, str)
        or not from_number
        or not isinstance(from_number, str)
        or not to_number
        or not isinstance(to_number, str)
        or not request.url.hostname
        or not isinstance(request.url.hostname, str)
    ):
        logger.error("Invalid or missing call data in twilio form {form_data}")
        return HTMLResponse(
            content="Invalid or missing call data. "
            "Please ensure Call SID, From number, To number, and hostname are provided and are of the correct type.",
            status_code=400,
        )

    res = await call_service.handle_incoming_call(
        call_sid,
        from_number,
        to_number,
        request.url.hostname,
    )
    return HTMLResponse(content=str(res), media_type="application/xml")


@router.websocket("/media-stream-eleven/{call_sid}")
async def handle_media_stream(
    websocket: WebSocket,
    call_sid: str,
    call_service: CallService = Depends(get_call_service),
) -> None:
    await call_service.handle_media_stream(websocket, call_sid)


@router.post("/call-status-eleven")
async def call_status_eleven(
    request: Request, call_service: CallService = Depends(get_call_service)
) -> JSONResponse:
    form_data = await request.form()

    stream_event = form_data.get("StreamEvent")
    call_sid = form_data.get("CallSid")
    if (
        not call_sid
        or not isinstance(call_sid, str)
        or not stream_event
        or not isinstance(stream_event, str)
    ):
        logger.error("Invalid request data")
        return JSONResponse({"success": False})
    success = await call_service.handle_call_status(call_sid, stream_event)
    return JSONResponse({"success": success})
