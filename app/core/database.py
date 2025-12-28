from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings 

engine = create_engine(
    settings.DATABASE_URL,
    # Echo=True giúp bạn xem được các câu lệnh SQL mà Alembic/SQLAlchemy thực thi ở console
    echo=settings.DEBUG,           
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    future=True
)

# Tạo Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()
