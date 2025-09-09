#!/usr/bin/env python3
"""
Script to add ContentStatus records to associate conversations with clients, projects, content types, and statuses
This makes the conversation browser filters work properly
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from db import AsyncSessionLocal
from models import Conversation, Client, Project, ContentStatus
from sqlmodel import select


async def add_content_status_data():
    """Add ContentStatus records to associate conversations with clients, projects, content types, and statuses"""
    print("🔄 Adding ContentStatus data to make conversation filters work...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Get all conversations
            conversations_result = await session.execute(select(Conversation))
            conversations = conversations_result.scalars().all()
            
            # Get all clients
            clients_result = await session.execute(select(Client))
            clients = clients_result.scalars().all()
            
            # Get all projects
            projects_result = await session.execute(select(Project))
            projects = projects_result.scalars().all()
            
            if not conversations:
                print("❌ No conversations found. Please run the conversation setup first.")
                return
            
            if not clients:
                print("❌ No clients found. Please run the client setup first.")
                return
                
            if not projects:
                print("❌ No projects found. Please run the project setup first.")
                return
            
            # Content types and statuses to use
            content_types = [
                "blog_post", "social_media", "email_campaign", "ad_copy", 
                "press_release", "whitepaper", "case_study", "newsletter"
            ]
            
            statuses = ["draft", "review", "approved", "rejected", "published"]
            
            # Create ContentStatus records for conversations
            content_status_records = []
            
            for i, conversation in enumerate(conversations):
                # Assign a random client and project
                client = clients[i % len(clients)]
                project = projects[i % len(projects)]
                
                # Assign a random content type and status
                content_type = content_types[i % len(content_types)]
                status = statuses[i % len(statuses)]
                
                # Create ContentStatus record
                content_status = ContentStatus(
                    conversation_id=conversation.id,
                    project_id=project.id,
                    status=status,
                    content_type=content_type,
                    assigned_to=None,  # Could be assigned to a user if needed
                    review_notes=f"Auto-generated content status for {conversation.title}",
                    due_date=datetime.now() + timedelta(days=7 + (i % 30)),  # Random due date
                    published_at=datetime.now() + timedelta(days=1) if status == "published" else None
                )
                
                content_status_records.append(content_status)
            
            # Add all ContentStatus records to the session
            for record in content_status_records:
                session.add(record)
            
            await session.commit()
            
            print(f"✅ Created {len(content_status_records)} ContentStatus records")
            print(f"   - Associated conversations with {len(clients)} clients")
            print(f"   - Associated conversations with {len(projects)} projects")
            print(f"   - Used {len(content_types)} different content types")
            print(f"   - Used {len(statuses)} different statuses")
            
        except Exception as e:
            print(f"❌ Error adding ContentStatus data: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(add_content_status_data())
