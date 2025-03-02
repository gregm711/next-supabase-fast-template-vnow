from fastapi import FastAPI
from sqladmin import Admin
from app.models import CallAdmin
from app.utils.logger import setup_logging
from app.database import engine
from app.routers.calls import router as calls_router
from app.routers.unprotected import router as unprotected_router
from app.utils.sqladmin_auth import AdminAuth
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.auth_middleware import AuthMiddleware
import os

logger = setup_logging()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

# Include your existing calls router (for Twilio endpoints).
app.include_router(calls_router)
app.include_router(unprotected_router)

# Admin Dashboard setup: https://aminalaee.dev/sqladmin/
authentication_backend = AdminAuth(secret_key=os.environ["ADMIN_SECRET_KEY"])
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(CallAdmin)
