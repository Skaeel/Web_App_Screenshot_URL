from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Screenshot(Base):
    __tablename__ = 'screenshots'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.id=}, {self.url=}, {self.filename=}'


engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@db:5432/postgres"
)


Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()


def new_screenshot(url: str, filename: str) -> Screenshot:
    new_obj = Screenshot(url=url, filename=filename)
    session.add(new_obj)
    session.commit()
    return new_obj


def get_screenshot(id: int = None, url: str = None) -> Screenshot:
    screenshot_obj: Screenshot = None
    if id:
        screenshot_obj = session.query(Screenshot).filter(
            Screenshot.id == id).first()
    elif url:
        screenshot_obj = session.query(Screenshot).filter(
            Screenshot.url == url).first()
    return screenshot_obj


def delete_screenshot(id: int = None, url: str = None) -> None:
    screenshot_obj = get_screenshot(id, url)
    if screenshot_obj is None:
        return

    session.delete(screenshot_obj)
    session.commit()


def edit_screenshot(filename: str, id: int = None, url: str = None) -> None | Screenshot:
    screenshot_obj = get_screenshot(id, url)
    if screenshot_obj is None:
        return

    screenshot_obj.filename = filename
    session.commit()
    return screenshot_obj
