import sys
import os
import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the path to your app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base  # Import Base from your app

# This is the MetaData object for your app
target_metadata = Base.metadata  # Link to the correct metadata object

# Setup logging configuration
fileConfig(context.config.config_file_name)
logger = logging.getLogger('alembic.env')

# Get the database URL from the alembic.ini file
config = context.config

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    In this mode, we just generate the SQL to be executed, but we don't execute it.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Run migrations in 'online' mode.
    In this mode, we execute the migrations directly on the database.
    """
    # Connect to the database
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Determine if we are in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
