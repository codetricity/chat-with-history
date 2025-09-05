# Fake Data Scripts

This folder contains sample data generation scripts specifically for the conversation browser application.

## Scripts

### Core Conversation Data

- **`add_sample_conversation_folders.py`** - Creates sample conversation folders with hierarchical structure
- **`add_sample_conversations.py`** - Creates sample conversations and assigns them to folders
- **`add_sample_messages.py`** - Adds realistic conversation messages with user/assistant exchanges

### Application Entities

- **`add_sample_clients_projects.py`** - Creates sample clients and projects for the marketing firm system
- **`add_sample_content_templates.py`** - Creates sample content templates for content generation

### Master Setup Script

- **`setup_conversation_data.py`** - Runs all conversation data scripts in the correct order

## Usage

### Individual Scripts

Run each script individually:

```bash
# Create application entities first
uv run python scripts/fake_data/add_sample_clients_projects.py
uv run python scripts/fake_data/add_sample_content_templates.py

# Then create conversation data
uv run python scripts/fake_data/add_sample_conversation_folders.py
uv run python scripts/fake_data/add_sample_conversations.py
uv run python scripts/fake_data/add_sample_messages.py
```

### Master Setup

Run all scripts at once:

```bash
uv run python scripts/fake_data/setup_conversation_data.py
```

## Prerequisites

Make sure you have:

1. **Users in the database** - Run `uv run python scripts/add_test_users.py` first
2. **Database initialized** - Run `uv run python scripts/init_db.py` if needed

## Sample Data Created

The scripts create:

### Application Entities
- **5 sample clients** (TechStart Inc., EcoFriendly Products, Local Restaurant Group, etc.)
- **10 sample projects** assigned to clients with budgets, timelines, and statuses
- **8 content templates** (Blog Post Outline, Social Media Post, Email Newsletter, etc.)

### Conversation Data
- **8 main conversation folders** (Work Projects, Personal Learning, Client Communications, etc.)
- **3 sub-folders** under Work Projects (Active, Completed, On Hold)
- **12 sample conversations** with realistic titles and timestamps
- **15+ sample messages** with detailed technical conversations about:
  - FastAPI authentication implementation
  - Database migration strategies
  - Client API requirements
  - Performance optimization
  - Python async programming

## Data Structure

```
Conversation Folders
├── Work Projects
│   ├── Active Projects
│   ├── Completed Projects
│   └── On Hold
├── Personal Learning
├── Client Communications
├── Technical Discussions
├── Q1 2024 Projects
├── Q2 2024 Projects
├── Bug Reports
└── Feature Requests
```

Each conversation contains realistic user/assistant message exchanges with proper timestamps, token counts, and model information.
