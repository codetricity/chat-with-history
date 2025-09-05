#!/usr/bin/env python3
"""
Script to add sample conversations for testing the conversation browser functionality
"""

import asyncio
import uuid
from datetime import datetime, timezone, timedelta
from db import AsyncSessionLocal
from models import Conversation, ConversationFolder, User
from sqlmodel import select


async def add_sample_conversations():
    """Add sample conversations to the database"""
    
    async with AsyncSessionLocal() as session:
        # Get some existing users and folders
        users_result = await session.execute(select(User).limit(3))
        users = users_result.scalars().all()
        
        folders_result = await session.execute(select(ConversationFolder).limit(5))
        folders = folders_result.scalars().all()
        
        if not users:
            print("❌ No users found. Please run add_test_users.py first.")
            return
        
        if not folders:
            print("❌ No folders found. Please run add_sample_conversation_folders.py first.")
            return
        
        # Sample conversations
        sample_conversations = [
            {
                "title": "Sony AI Developer Community Strategy for US Market",
                "user_id": users[0].id,
                "folder_id": folders[0].id if folders else None,
                "created_at": datetime.now(timezone.utc) - timedelta(days=5),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=2)
            },
            {
                "title": "Intel AI/ML Hardware Influencer Marketing Campaign",
                "user_id": users[0].id,
                "folder_id": folders[1].id if len(folders) > 1 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=3),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=1)
            },
            {
                "title": "AMD Developer Documentation Strategy & SDK Improvements",
                "user_id": users[1].id if len(users) > 1 else users[0].id,
                "folder_id": folders[5].id if len(folders) > 5 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=7),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=4)
            },
            {
                "title": "Rapidus 2nm Technology US Market Entry Plan",
                "user_id": users[1].id if len(users) > 1 else users[0].id,
                "folder_id": folders[0].id if folders else None,
                "created_at": datetime.now(timezone.utc) - timedelta(days=2),
                "updated_at": datetime.now(timezone.utc) - timedelta(hours=6)
            },
            {
                "title": "AI-Generated Technical Content for Healthcare Vertical",
                "user_id": users[0].id,
                "folder_id": folders[3].id if len(folders) > 3 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=10),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=8)
            },
            {
                "title": "Canon AI Imaging Solutions Developer Outreach",
                "user_id": users[2].id if len(users) > 2 else users[0].id,
                "folder_id": folders[4].id if len(folders) > 4 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=1),
                "updated_at": datetime.now(timezone.utc) - timedelta(hours=2)
            },
            {
                "title": "Ricoh B2B AI Solutions Event Strategy",
                "user_id": users[2].id if len(users) > 2 else users[0].id,
                "folder_id": folders[6].id if len(folders) > 6 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=4),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=3)
            },
            {
                "title": "US AI/ML Conference & Meetup Planning",
                "user_id": users[0].id,
                "folder_id": folders[6].id if len(folders) > 6 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=14),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=12)
            },
            {
                "title": "Financial Services AI Content Strategy",
                "user_id": users[0].id,
                "folder_id": folders[3].id if len(folders) > 3 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=6),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=5)
            },
            {
                "title": "Developer Influencer Partnership Strategy",
                "user_id": users[1].id if len(users) > 1 else users[0].id,
                "folder_id": folders[1].id if len(folders) > 1 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(hours=12),
                "updated_at": datetime.now(timezone.utc) - timedelta(hours=3)
            },
            {
                "title": "Automotive AI Applications US Market Analysis",
                "user_id": users[1].id if len(users) > 1 else users[0].id,
                "folder_id": folders[3].id if len(folders) > 3 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=8),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=6)
            },
            {
                "title": "Technical Documentation AI Content Generation",
                "user_id": users[2].id if len(users) > 2 else users[0].id,
                "folder_id": folders[2].id if len(folders) > 2 else folders[0].id,
                "created_at": datetime.now(timezone.utc) - timedelta(days=9),
                "updated_at": datetime.now(timezone.utc) - timedelta(days=7)
            },
            # Add some root conversations (no folder)
            {
                "title": "General AI Market Research & Trends",
                "user_id": users[0].id,
                "folder_id": None,  # Root conversation
                "created_at": datetime.now(timezone.utc) - timedelta(days=2),
                "updated_at": datetime.now(timezone.utc) - timedelta(hours=3)
            },
            {
                "title": "Client Onboarding Process Discussion",
                "user_id": users[1].id if len(users) > 1 else users[0].id,
                "folder_id": None,  # Root conversation
                "created_at": datetime.now(timezone.utc) - timedelta(days=1),
                "updated_at": datetime.now(timezone.utc) - timedelta(hours=1)
            },
            {
                "title": "Team Meeting Notes - Q4 Planning",
                "user_id": users[2].id if len(users) > 2 else users[0].id,
                "folder_id": None,  # Root conversation
                "created_at": datetime.now(timezone.utc) - timedelta(hours=6),
                "updated_at": datetime.now(timezone.utc) - timedelta(hours=2)
            }
        ]
        
        created_conversations = []
        
        for conv_data in sample_conversations:
            # Check if conversation already exists (by title and user)
            existing = await session.execute(
                select(Conversation).where(
                    Conversation.title == conv_data['title'],
                    Conversation.user_id == conv_data['user_id']
                )
            )
            if existing.scalar_one_or_none():
                print(f"Conversation '{conv_data['title']}' already exists, skipping...")
                continue
            
            conversation = Conversation(
                id=uuid.uuid4(),
                title=conv_data['title'],
                user_id=conv_data['user_id'],
                folder_id=conv_data['folder_id'],
                created_at=conv_data['created_at'],
                updated_at=conv_data['updated_at'],
                is_active=True
            )
            
            session.add(conversation)
            created_conversations.append(conversation)
            print(f"Added conversation: {conv_data['title']}")
        
        await session.commit()
        print(f"\n✅ Successfully added {len(created_conversations)} sample conversations!")
        
        # Show summary by folder
        print("\nConversations by folder:")
        for folder in folders:
            folder_conversations = [c for c in created_conversations if c.folder_id == folder.id]
            if folder_conversations:
                print(f"- {folder.name}: {len(folder_conversations)} conversations")


if __name__ == "__main__":
    asyncio.run(add_sample_conversations())
