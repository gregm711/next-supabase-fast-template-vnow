import asyncio
from typing import Any, Callable, Optional
import queue
import threading
import base64
from elevenlabs.conversational_ai.conversation import AudioInterface
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class TwilioAudioInterface(AudioInterface):

    def __init__(self, websocket: WebSocket) -> None:
        self.websocket: WebSocket = websocket
        self.output_queue: queue.Queue[bytes] = queue.Queue()
        self.should_stop: threading.Event = threading.Event()
        self.stream_sid: Optional[str] = None
        self.input_callback: Optional[Callable[[bytes], None]] = None
        self.output_thread: Optional[threading.Thread] = None
        self.is_running: bool = False

    def start(self, input_callback: Callable[[bytes], None]) -> None:
        logger.info("Starting audio interface")
        self.should_stop.clear()
        self.input_callback = input_callback
        self.is_running = True  # Set before starting thread
        self.output_thread = threading.Thread(target=self._output_thread)
        self.output_thread.daemon = True
        self.output_thread.start()
        logger.info("Audio interface started")

    def stop(self) -> None:
        self.is_running = False
        self.should_stop.set()
        self.interrupt()
        self.input_callback = None
        self.stream_sid = None

    def output(self, audio: bytes) -> None:
        if self.is_running:
            self.output_queue.put(audio)

    def interrupt(self) -> None:
        try:
            while True:
                self.output_queue.get_nowait()
        except queue.Empty:
            pass

    async def handle_twilio_message(self, data: dict[str, Any]) -> None:
        try:
            event_type = data.get("event")
            if event_type == "start":
                self.stream_sid = data["start"]["streamSid"]
                self.is_running = True  # Ensure running on start event
                logger.info(f"Started stream with stream_sid: {self.stream_sid}")
            elif event_type == "media" and self.input_callback and self.is_running:
                audio_data = base64.b64decode(data["media"]["payload"])
                self.input_callback(audio_data)
        except Exception as e:
            logger.error(f"Error in input_callback: {e}")
            self.stop()

    def _output_thread(self) -> None:
        while not self.should_stop.is_set():
            try:
                audio = self.output_queue.get(timeout=0.2)
                if self.stream_sid and self.is_running:
                    audio_payload = base64.b64encode(audio).decode("utf-8")
                    audio_delta = {
                        "event": "media",
                        "streamSid": self.stream_sid,
                        "media": {"payload": audio_payload},
                    }
                    asyncio.run(self._send_audio_message(audio_delta))
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in output thread: {e}")

    async def _send_audio_message(self, message: dict[str, Any]) -> None:
        try:
            await self.websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending audio message: {e}")
            self.stop()

    async def _send_clear_message(self) -> None:
        if self.stream_sid:
            try:
                clear_message = {"event": "clear", "streamSid": self.stream_sid}
                await self.websocket.send_json(clear_message)
            except Exception as e:
                logger.error(f"Error sending clear message: {e}")
