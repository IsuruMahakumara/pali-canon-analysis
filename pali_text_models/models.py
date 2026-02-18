"""SQLModel data models for Pali Canon database - reusable in notebooks and FastAPI"""
import os
from sqlmodel import Field, SQLModel, create_engine, Session

# Database connection settings
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pali_canon:anicca@localhost:5432/pali_canon_db"
)

# SQLModel models
class Sutta(SQLModel, table=True):
    """A single verse/segment from the Pali Canon"""
    index: str = Field(primary_key=True)
    nikaya: str
    vagga: str
    sutta_id: str
    text: str | None = None
    hela_text: str | None = None


# Engine factory - creates engine with connection pooling
def get_engine(echo: bool = False):
    """Create SQLModel engine for PostgreSQL"""
    return create_engine(DATABASE_URL, echo=echo)


# Session helper for use in notebooks
def get_session(echo: bool = False):
    """Create a new database session"""
    engine = get_engine(echo=echo)
    return Session(engine)


# Initialize tables
def create_tables(engine=None):
    """Create all tables in the database"""
    if engine is None:
        engine = get_engine()
    SQLModel.metadata.create_all(engine)

