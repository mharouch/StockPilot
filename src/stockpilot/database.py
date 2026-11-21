import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DEFAULT_DATABASE_URL = "sqlite:///data/stockpilot.db"
DATABASE_URL_ENV_VAR = "STOCKPILOT_DATABASE_URL"


class Base(DeclarativeBase):
    """Base class for database models."""


def get_database_url():
    """Return the configured database URL."""
    return os.getenv(
        DATABASE_URL_ENV_VAR,
        DEFAULT_DATABASE_URL,
    )


def create_database_engine(database_url=None):
    """Create a SQLAlchemy engine."""
    selected_database_url = database_url or get_database_url()

    return create_engine(selected_database_url)


def create_session_factory(engine):
    """Create database sessions bound to an engine."""
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )


def initialize_database(database_url=None):
    """Create the configured database and its tables."""
    engine = create_database_engine(database_url)

    from src.stockpilot.models import StockLevel

    StockLevel.metadata.create_all(engine)

    return engine


def main():
    """Initialize the configured database."""
    engine = initialize_database()

    print(f"Database initialized: {engine.url}")

    engine.dispose()


if __name__ == "__main__":
    main()
