#!/usr/bin/env python3
"""
Oppkey Setup Tool (oppsetup.py)
A comprehensive setup tool for initializing the conversation browser application with all fake data.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from scripts.init_db import init_db
    from scripts.create_superuser import create_superuser
    from scripts.add_test_users import add_test_users
    from scripts.fake_data.add_sample_clients_projects import add_sample_data as add_clients_projects
    from scripts.fake_data.add_sample_content_templates import add_sample_templates
    from scripts.fake_data.setup_conversation_data import setup_conversation_data
    from scripts.check_users import check_users
    from scripts.test_auth import test_auth
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all script files are in the scripts/ directory")
    sys.exit(1)


def ensure_upload_dirs():
    """Ensure static upload directories exist regardless of current working directory."""
    project_root = Path(__file__).resolve().parent
    uploads_root = project_root / "static" / "uploads"
    uploads_root.mkdir(parents=True, exist_ok=True)


async def run_complete_setup():
    """Run complete setup with all fake data"""
    print("🚀 Running complete setup with fake data...")
    print("=" * 60)
    
    ensure_upload_dirs()
    
    try:
        # Step 1: Initialize database
        print("\n📊 Step 1: Initializing database...")
        await init_db()
        print("✅ Database initialized")
        
        # Step 2: Create superuser
        print("\n👤 Step 2: Creating superuser...")
        await create_superuser()
        print("✅ Superuser created: admin@example.com / admin123")
        
        # Step 3: Add test users
        print("\n👥 Step 3: Adding test users...")
        await add_test_users()
        print("✅ Test users added (password: test123)")
        
        # Step 4: Add clients and projects
        print("\n🏢 Step 4: Adding sample clients and projects...")
        await add_clients_projects()
        print("✅ 5 sample clients and 10 projects added")
        
        # Step 5: Add content templates
        print("\n📝 Step 5: Adding content templates...")
        await add_sample_templates()
        print("✅ 8 content templates added")
        
        # Step 6: Add conversation data
        print("\n💬 Step 6: Adding conversation data...")
        await setup_conversation_data()
        print("✅ Conversation data added")
        
        # Step 7: Verify setup
        print("\n🔍 Step 7: Verifying setup...")
        await check_users()
        print("✅ Setup verification complete")
        
        print("\n" + "=" * 60)
        print("🎉 Complete setup with fake data finished!")
        print("\n📋 What was created:")
        print("  - Database initialized")
        print("  - Superuser: admin@example.com / admin123")
        print("  - Test users: test123 (for all test users)")
        print("  - 5 sample clients (TechStart Inc., EcoFriendly Products, etc.)")
        print("  - 10 sample projects with budgets and timelines")
        print("  - 8 content templates (Blog Post, Social Media, etc.)")
        print("  - 8 conversation folders with 3 sub-folders")
        print("  - 12 sample conversations with realistic messages")
        print("\n🌐 Ready to start the application:")
        print("  uv run uvicorn main:app --reload")
        print("\n🔗 Access points:")
        print("  - Admin panel: http://localhost:8000/admin/")
        print("  - Conversation browser: http://localhost:8000/conversations")
        print("  - API docs: http://localhost:8000/docs")
        print("\n🔐 Login credentials:")
        print("  - Superuser: admin@example.com / admin123")
        print("  - Test users: test123 (for all test users)")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


async def run_minimal_setup():
    """Run minimal setup (database + superuser + users only)"""
    print("🚀 Running minimal setup...")
    print("=" * 40)
    
    ensure_upload_dirs()
    
    try:
        # Step 1: Initialize database
        print("\n📊 Step 1: Initializing database...")
        await init_db()
        print("✅ Database initialized")
        
        # Step 2: Create superuser
        print("\n👤 Step 2: Creating superuser...")
        await create_superuser()
        print("✅ Superuser created: admin@example.com / admin123")
        
        # Step 3: Add test users
        print("\n👥 Step 3: Adding test users...")
        await add_test_users()
        print("✅ Test users added (password: test123)")
        
        print("\n" + "=" * 40)
        print("✅ Minimal setup complete!")
        print("\n📋 What was created:")
        print("  - Database initialized")
        print("  - Superuser: admin@example.com / admin123")
        print("  - Test users: test123 (for all test users)")
        print("\n🌐 Ready to start the application:")
        print("  uv run uvicorn main:app --reload")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def show_help():
    """Show help information"""
    help_text = """
Oppkey Setup Tool (oppsetup.py)

A comprehensive setup tool for initializing the conversation browser application.

USAGE:
    uv run python oppsetup.py [command]

COMMANDS:
    init        Complete setup with all fake data (default)
    minimal     Minimal setup (database + superuser + users only)
    help        Show this help message

EXAMPLES:
    # Complete setup with all fake data
    uv run python oppsetup.py
    uv run python oppsetup.py init
    
    # Minimal setup (no fake data)
    uv run python oppsetup.py minimal
    
    # Show help
    uv run python oppsetup.py help

WHAT'S INCLUDED IN INIT SETUP:
    - Database initialization
    - Superuser creation (admin@example.com / admin123)
    - Test users (password: test123)
    - 5 sample clients and 10 projects
    - 8 content templates
    - 8 conversation folders with 3 sub-folders
    - 12 sample conversations with realistic messages

WHAT'S INCLUDED IN MINIMAL SETUP:
    - Database initialization
    - Superuser creation (admin@example.com / admin123)
    - Test users (password: test123)

ACCESS POINTS (after setup):
    - Admin panel: http://localhost:8000/admin/
    - Conversation browser: http://localhost:8000/conversations
    - API docs: http://localhost:8000/docs

LOGIN CREDENTIALS:
    - Superuser: admin@example.com / admin123
    - Test users: test123 (for all test users)
    """
    print(help_text)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Oppkey Setup Tool for Conversation Browser Application",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["init", "minimal", "help"],
        default="init",
        help="Setup command to execute (default: init)"
    )
    
    args = parser.parse_args()
    
    # Handle help command
    if args.command == "help":
        show_help()
        return
    
    # Run the appropriate setup
    if args.command == "minimal":
        asyncio.run(run_minimal_setup())
    else:  # init or default
        asyncio.run(run_complete_setup())


if __name__ == "__main__":
    main()
