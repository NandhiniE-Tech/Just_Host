from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# MySQL Database URL with proper encoding
DATABASE_URL = "mysql+pymysql://root:Nandhini$25@localhost/Bharathiyar_Bot?charset=utf8mb4"

# Create Engine with connection pool settings
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Keep for debugging
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

# Create Base
Base = declarative_base()

# Create Session with expire_on_commit=False
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)
