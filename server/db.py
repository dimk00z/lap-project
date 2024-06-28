from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def init_db(engine) -> None:
    Base.metadata.create_all(bind=engine)
