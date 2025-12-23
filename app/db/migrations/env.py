import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool, inspect, text
from sqlalchemy.engine import reflection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from app.db.base import Base
from app.core.config import settings

import app.models
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def get_table_details():
    """Print detailed information about all tables in the metadata."""
    print("\n=== Database Schema Information ===")
    for table_name, table in target_metadata.tables.items():
        # print(f"\nTable: {table_name}")
        # print("Columns:")
        for column in table.columns:
            nullable = "NULL" if column.nullable else "NOT NULL"
            default = f"DEFAULT {column.default}" if column.default else ""
            print(f"  - {column.name}: {column.type} {nullable} {default}")
        
        print("Indexes:")
        for index in table.indexes:
            print(f"  - {index.name}: {', '.join(col.name for col in index.columns)}")
        
        print("Foreign Keys:")
        for fk in table.foreign_keys:
            print(f"  - {fk.parent.name} -> {fk.target_fullname}")

def include_object(object, name, type_, reflected, compare_to):
    """
    Determine which database objects should be generated in migrations.
    
    Args:
        object: The object being considered
        name: The object's name
        type_: The type of object (table, column, index, etc.)
        reflected: True if the object was reflected from the database
        compare_to: The object being compared to, or None
        
    Returns:
        bool: True if the object should be included in the migration
    """
    # Always include new tables, columns, and indexes
    if not reflected:
        return True 
    # Skip dropping tables but include all other changes
    if type_ == "table" and reflected and compare_to is None:
        print(f"Ignoring drop of table: {name}")
        return False 
    return True

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(
        url=url, target_metadata=target_metadata,literal_binds=True, dialect_opts={"paramstyle": "named"}, compare_type=True, compare_server_default=True, include_object=include_object, render_as_batch=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Print table information before running migrations
    get_table_details()
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = engine_from_config(configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True, compare_server_default=True, include_object=include_object, render_as_batch=True
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()