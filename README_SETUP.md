# Quick Setup Guide

## Complete Setup with Fake Data

To recreate the database with all fake data in a single command:

```bash
uv run python oppsetup.py
# or
uv run python oppsetup.py init
```

This will create:
- Database initialization
- Superuser: `admin@example.com` / `admin123`
- Test users: `test123` (for all test users)
- 5 sample clients and 10 projects
- 8 content templates
- 8 conversation folders with 3 sub-folders
- 12 sample conversations with realistic messages

## Minimal Setup (No Fake Data)

For a minimal setup without fake data:

```bash
uv run python oppsetup.py minimal
```

## What You Get

After running the complete setup, you can access:

- **Admin panel**: http://localhost:8000/admin/
- **Conversation browser**: http://localhost:8000/conversations
- **API docs**: http://localhost:8000/docs

## Start the Application

```bash
uv run uvicorn main:app --reload
```

## Help

```bash
uv run python oppsetup.py help
```

## Alternative: Individual Commands

If you prefer to run individual setup commands:

```bash
# Core setup
uv run python oppman.py init

# Add specific data
uv run python oppman.py clients_projects
uv run python oppman.py content_templates
uv run python scripts/fake_data/setup_conversation_data.py
```
