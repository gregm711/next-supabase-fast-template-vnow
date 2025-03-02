from enum import Enum


class CallStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    STREAMING = "STREAMING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"  # Assuming we will get some failed/canceled status from Twilio or Eleven Labs if the call fails.
