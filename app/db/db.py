from sqlalchemy import Column, Integer, String, select, update
from sqlalchemy.orm import declarative_base 
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
import os


postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_user = os.getenv('POSTGRES_USER')
postgres_db = os.getenv('POSTGRES_DB')

Base = declarative_base()


class Screenshot(Base):
    __tablename__ = 'screenshots'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.id=}, {self.url=}, {self.filename=}'

DATABASE_URL = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@db:5432/{postgres_db}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_table(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def new_screenshot(async_session: async_sessionmaker[AsyncSession],
                         url: str, filename: str) -> Screenshot:
    async with async_session() as session:
        async with session.begin():
            new_obj = Screenshot(url=url, filename=filename)
            session.add(new_obj)
            await session.commit()
            return new_obj 


async def get_screenshot(async_session: async_sessionmaker[AsyncSession], 
                   id: int = None, url: str = None) -> Screenshot:
    screenshot_obj: Screenshot = None
    async with async_session() as session:
        async with session.begin():
            if id:
                screenshot_obj = await session.execute(select(Screenshot).where(Screenshot.id == id))
                screenshot_obj = screenshot_obj.scalars().first()
            elif url:
                screenshot_obj = await session.execute(select(Screenshot).where(Screenshot.url == url))
                screenshot_obj = screenshot_obj.scalars().first()
            return screenshot_obj 


async def edit_screenshot(async_session: async_sessionmaker[AsyncSession],
                    filename: str, id: int = None, url: str = None) -> Screenshot:
    async with async_session() as session:
        async with session.begin():
            screenshot_obj = await get_screenshot(async_session, id, url)
            if screenshot_obj is None:
                return
            await session.execute(update(Screenshot).where(Screenshot.url == url).values(filename=filename))
            await session.commit()
            return screenshot_obj
