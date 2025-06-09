from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    is_banned = Column(Boolean, default=False)
    language = Column(String, default="ru")

    reminders = relationship("Reminder", back_populates="user")


class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String, nullable=False)
    remind_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="reminders")


# Async DB engine and session
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)