#!/usr/bin/env python3
"""
Script to add sample conversation folders for testing the conversation browser functionality
"""

import asyncio
import uuid
from datetime import datetime, timezone
from db import AsyncSessionLocal
from models import ConversationFolder, User
from sqlmodel import select


async def add_sample_conversation_folders():
    """Add sample conversation folders to the database"""
    
    async with AsyncSessionLocal() as session:
        # Get some existing users to assign folders to
        result = await session.execute(select(User).limit(3))
        users = result.scalars().all()
        
        if not users:
            print("❌ No users found. Please run add_test_users.py first.")
            return
        
        # Sample conversation folders
        sample_folders = [
            {
                "name": "US Market Entry Strategy",
                "description": "Strategic conversations about entering the US market with AI/ML technologies and developer tools",
                "user_id": users[0].id if users else None,
                "parent_folder_id": None
            },
            {
                "name": "Influencer Marketing Campaigns",
                "description": "Conversations about B2B influencer marketing strategies and developer community outreach",
                "user_id": users[0].id if users else None,
                "parent_folder_id": None
            },
            {
                "name": "Technical Content Generation",
                "description": "AI-generated content strategies for technical documentation, tutorials, and developer resources",
                "user_id": users[1].id if len(users) > 1 else users[0].id,
                "parent_folder_id": None
            },
            {
                "name": "Industry Vertical Strategies",
                "description": "Conversations about targeting specific US industry verticals (healthcare, finance, automotive, etc.)",
                "user_id": users[1].id if len(users) > 1 else users[0].id,
                "parent_folder_id": None
            },
            {
                "name": "Developer Community Building",
                "description": "Strategies for building and engaging developer communities in the US market",
                "user_id": users[0].id if users else None,
                "parent_folder_id": None  # Will be updated after creating the parent
            },
            {
                "name": "SDK & Documentation Strategy", 
                "description": "Technical documentation and SDK improvement strategies based on influencer feedback",
                "user_id": users[0].id if users else None,
                "parent_folder_id": None  # Will be updated after creating the parent
            },
            {
                "name": "Event & Conference Planning",
                "description": "Conversations about US market events, conferences, and developer meetups",
                "user_id": users[2].id if len(users) > 2 else users[0].id,
                "parent_folder_id": None
            },
            {
                "name": "Client-Specific Projects",
                "description": "Conversations specific to individual client projects and requirements",
                "user_id": users[2].id if len(users) > 2 else users[0].id,
                "parent_folder_id": None
            }
        ]
        
        created_folders = []
        
        for folder_data in sample_folders:
            # Check if folder already exists
            existing = await session.execute(
                select(ConversationFolder).where(
                    ConversationFolder.name == folder_data['name'],
                    ConversationFolder.user_id == folder_data['user_id']
                )
            )
            if existing.scalar_one_or_none():
                print(f"Folder '{folder_data['name']}' already exists, skipping...")
                continue
            
            folder = ConversationFolder(
                id=uuid.uuid4(),
                name=folder_data['name'],
                description=folder_data['description'],
                user_id=folder_data['user_id'],
                parent_folder_id=folder_data['parent_folder_id'],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                is_active=True
            )
            
            session.add(folder)
            created_folders.append(folder)
            print(f"Added folder: {folder_data['name']}")
        
        await session.commit()
        
        # Now create some sub-folders
        if created_folders:
            # Find the "US Market Entry Strategy" folder to add sub-folders
            us_market_folder = None
            for folder in created_folders:
                if folder.name == "US Market Entry Strategy":
                    us_market_folder = folder
                    break
            
            if us_market_folder:
                sub_folders = [
                    {
                        "name": "Market Research & Analysis",
                        "description": "US market research, competitive analysis, and market entry strategies",
                        "user_id": us_market_folder.user_id,
                        "parent_folder_id": us_market_folder.id
                    },
                    {
                        "name": "Regulatory & Compliance",
                        "description": "US regulatory requirements, compliance strategies, and legal considerations",
                        "user_id": us_market_folder.user_id,
                        "parent_folder_id": us_market_folder.id
                    },
                    {
                        "name": "Partnership & Channel Strategy",
                        "description": "US partnership strategies, channel development, and go-to-market planning",
                        "user_id": us_market_folder.user_id,
                        "parent_folder_id": us_market_folder.id
                    }
                ]
                
                for sub_folder_data in sub_folders:
                    # Check if sub-folder already exists
                    existing = await session.execute(
                        select(ConversationFolder).where(
                            ConversationFolder.name == sub_folder_data['name'],
                            ConversationFolder.parent_folder_id == sub_folder_data['parent_folder_id']
                        )
                    )
                    if existing.scalar_one_or_none():
                        print(f"Sub-folder '{sub_folder_data['name']}' already exists, skipping...")
                        continue
                    
                    sub_folder = ConversationFolder(
                        id=uuid.uuid4(),
                        name=sub_folder_data['name'],
                        description=sub_folder_data['description'],
                        user_id=sub_folder_data['user_id'],
                        parent_folder_id=sub_folder_data['parent_folder_id'],
                        created_at=datetime.now(timezone.utc),
                        updated_at=datetime.now(timezone.utc),
                        is_active=True
                    )
                    
                    session.add(sub_folder)
                    print(f"Added sub-folder: {sub_folder_data['name']} (under {us_market_folder.name})")
        
        await session.commit()
        print("\n✅ Successfully added conversation folders!")
        print(f"Created {len(created_folders)} main folders and 3 sub-folders")


if __name__ == "__main__":
    asyncio.run(add_sample_conversation_folders())
