import json
import traceback
import os
import signal
import uuid

from app.models import Call
from app.repositories.calls import CallRepository
from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from twilio.twiml.voice_response import VoiceResponse, Connect
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from app.utils.twilio_audio_interface import TwilioAudioInterface
from app.enums import CallStatus
import logging

logger = logging.getLogger(__name__)

GLOBAL_CONVERSATION_STORE: dict[str, Conversation] = (
    {}
)  # TODO: This works, but there MUST be a way to store the conversation state in the database. This is a temporary solution.


class CallService:

    def __init__(self, call_repository: CallRepository) -> None:
        self.eleven_labs_agent_id = os.environ["ELEVENLABS_AGENT_ID"]
        self.eleven_labs_client = ElevenLabs()
        self.conversation_store: dict[str, Conversation] = GLOBAL_CONVERSATION_STORE
        self.call_repository = call_repository

    def _cleanup_handler(self, call_sid: str) -> None:
        """
        Cleanup function to handle the termination of a conversation session.
        """
        conversation = self.conversation_store.pop(call_sid, None)
        if conversation:
            conversation.end_session()  # type: ignore
            logger.info(f"Cleaned up conversation for Call SID: {call_sid}")
            call = self.call_repository.get_call_by_sid(call_sid)
            if call:
                call.eleven_labs_conversation_id = conversation._conversation_id
                call.status = CallStatus.COMPLETED
                self.call_repository.update_call(call.id, call)

    def repository_health_check(self) -> bool:
        return self.call_repository.health_check()

    async def handle_incoming_call(
        self, call_sid: str, from_number: str, to_number: str, request_host: str
    ) -> VoiceResponse:
        """
        Handles incoming calls from Twilio and initiates a VoiceResponse with a media stream.
        """
        call = Call(
            id=uuid.uuid4(),
            sid=call_sid,
            from_number=from_number,
            to_number=to_number,
            status=CallStatus.INITIALIZED,
        )
        self.call_repository.create_call(call)

        voice_response = VoiceResponse()
        connect = Connect()
        connect.stream(
            url=f"wss://{request_host}/media-stream-eleven/{call_sid}",
            status_callback=f"https://{request_host}/call-status-eleven",
            status_callback_method="POST",
        )
        voice_response.append(connect)
        return voice_response

    async def handle_media_stream(self, websocket: WebSocket, call_sid: str) -> None:
        """
        Handles the WebSocket media stream for a specific call SID.
        """
        await websocket.accept()
        logger.info(f"WebSocket connection established for Call SID: {call_sid}")
        audio_interface = TwilioAudioInterface(websocket)

        # Register signal handler for graceful shutdown (only once is needed)
        try:
            signal.signal(
                signal.SIGINT, lambda sig, frame: self._cleanup_handler(call_sid)
            )
        except ValueError as e:
            logger.info(f"Could not set signal handler: {e}")

        try:
            conversation = Conversation(
                client=self.eleven_labs_client,
                agent_id=self.eleven_labs_agent_id,
                requires_auth=False,
                audio_interface=audio_interface,
                callback_agent_response=lambda text: logger.info(f"Agent said: {text}"),
                callback_user_transcript=lambda text: logger.info(f"User said: {text}"),
            )
            conversation.start_session()  # type: ignore
            logger.info(f"Conversation session started for Call SID: {call_sid}")

            call_obj = self.call_repository.get_call_by_sid(call_sid)
            if call_obj:
                call_obj.status = CallStatus.STREAMING
                self.call_repository.update_call(call_obj.id, call_obj)

            self.conversation_store[call_sid] = conversation

            async for message in websocket.iter_text():
                if not message:
                    continue
                data = json.loads(message)
                await audio_interface.handle_twilio_message(data)

        except WebSocketDisconnect as e:
            logger.error(f"WebSocketDisconnect for Call SID {call_sid}: {e}")
            self._cleanup_handler(call_sid)

        except Exception as e:
            logger.error(
                f"Error in media stream WebSocket for Call SID {call_sid}: {e}"
            )
            traceback.print_exc()
            self._cleanup_handler(call_sid)

    async def handle_call_status(self, call_sid: str, stream_event: str) -> bool:
        """
        Handles status callbacks from Twilio when the call ends or changes state.
        """
        logger.info(f"Stream Event: {stream_event}")
        if stream_event == "stream-stopped":
            logger.info(
                f"Stream stopped for Call SID: {call_sid}. Triggering conversation cleanup."
            )
            self._cleanup_handler(call_sid)

        return True
