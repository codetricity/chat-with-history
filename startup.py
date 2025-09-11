#!/usr/bin/env python3
"""
Startup script for production deployment
Handles database initialization and hybrid search setup in the correct order
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import after path setup
from db import create_tables  # noqa: E402
from scripts.setup_hybrid_search import setup_hybrid_search  # noqa: E402

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize the database by creating all tables"""
    logger.info("🔄 Initializing database...")
    try:
        # Import here to get the current DATABASE_URL
        from db import DATABASE_URL
        logger.info(f"Database URL: {DATABASE_URL}")

        await create_tables()
        logger.info("✅ Database initialized successfully")

        # Verify tables were created
        import aiosqlite
        import os
        db_path = DATABASE_URL.replace("sqlite+aiosqlite:///", "").replace("./", "")
        # Ensure absolute path for Fly volumes
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(db_path)
        
        logger.info(f"Verifying database at: {db_path}")
        logger.info(f"Database file exists: {os.path.exists(db_path)}")
        
        async with aiosqlite.connect(db_path) as db:
            cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = await cursor.fetchall()
            table_names = [row[0] for row in tables]
            logger.info(f"Created tables: {table_names}")

        return True
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_hybrid_search_setup():
    """Run hybrid search setup after database is initialized"""
    logger.info("🔄 Setting up hybrid search...")
    try:
        await setup_hybrid_search()
        logger.info("✅ Hybrid search setup completed")
        return True
    except Exception as e:
        logger.error(f"❌ Hybrid search setup failed: {e}")
        # Don't fail the entire startup if hybrid search setup fails
        # The app can still run without it
        return False


async def startup_sequence():
    """Run the complete startup sequence"""
    logger.info("🚀 Starting application initialization...")
    logger.info("=" * 50)

    # Step 0: Ensure data directory exists and check volume mount
    import os
    data_dir = "/data"
    logger.info(f"Checking data directory: {data_dir}")
    logger.info(f"Data directory exists: {os.path.exists(data_dir)}")
    if os.path.exists(data_dir):
        logger.info(f"Data directory contents: {os.listdir(data_dir)}")
    else:
        logger.info(f"Creating data directory: {data_dir}")
        os.makedirs(data_dir, exist_ok=True)

    # Step 1: Initialize database
    db_success = await initialize_database()
    if not db_success:
        logger.error("❌ Critical: Database initialization failed. Exiting.")
        sys.exit(1)

    # Step 2: Setup hybrid search (non-critical)
    hybrid_success = await run_hybrid_search_setup()
    if not hybrid_success:
        logger.warning("⚠️  Hybrid search setup failed, but continuing with app startup")

    logger.info("=" * 50)
    logger.info("✅ Application initialization complete!")
    logger.info("🌐 Starting FastAPI server...")


if __name__ == "__main__":
    asyncio.run(startup_sequence())
