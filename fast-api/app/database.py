import os
from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
print(f"DATABASE_URL: {DATABASE_URL}")
print(f"engine: {engine}")


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
