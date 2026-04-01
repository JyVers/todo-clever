from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("POSTGRESQL_ADDON_URI", "")

if not DATABASE_URL:
    raise ValueError("POSTGRESQL_ADDON_URI environment variable is not set")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


def init_db():
    from sqlalchemy import text

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT typname FROM pg_type WHERE typname = 'statusenum'")
            )
            if not result.fetchone():
                conn.execute(text("CREATE TYPE statusenum AS ENUM ('pending', 'done')"))
                conn.commit()
    except Exception as e:
        print(f"Enum creation skipped: {e}")
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


def get_db():
    with SessionLocal() as session:
        yield session
