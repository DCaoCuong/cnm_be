import sys
from os.path import abspath, dirname
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

# 1. Thiết lập đường dẫn để Alembic tìm thấy module 'app'
BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# 2. Import cấu hình và Base
from app.core.config import settings
from app.models import Base

from alembic import context

# Đối tượng cấu hình Alembic
config = context.config

# Thiết lập logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Gán metadata để autogenerate hoạt động
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Chạy migrations ở chế độ 'offline'."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Chạy migrations ở chế độ 'online'."""
    
    # Lấy cấu hình từ file .ini
    configuration = config.get_section(config.config_ini_section, {})
    
    # QUAN TRỌNG: Ghi đè URL từ alembic.ini bằng URL từ settings (.env)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()