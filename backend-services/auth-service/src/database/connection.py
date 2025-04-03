from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.config import DATABASE_URL

engine = create_engine(DATABASE_URL,
                        pool_size=10,
                        max_overflow=5,
                        pool_timeout=30,
                        pool_recycle=1800,
                        echo=True
                     )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()