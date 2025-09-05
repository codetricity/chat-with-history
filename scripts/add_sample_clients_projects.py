#!/usr/bin/env python3
"""
Script to add sample clients and projects for the marketing firm system.
"""

import asyncio
import sys
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# Add the parent directory to the path so we can import from the project
sys.path.append(str(Path(__file__).parent.parent))

from db import AsyncSessionLocal
from models import Client, Project
from sqlmodel import select


async def add_sample_data():
    """Add sample clients and projects to the database."""
    
    sample_clients = [
        {
            "name": "TechStart Inc.",
            "company": "TechStart Inc.",
            "email": "contact@techstart.com",
            "phone": "+1-555-0123",
            "industry": "Technology",
            "notes": "Fast-growing startup focused on AI solutions. High priority client with aggressive growth targets."
        },
        {
            "name": "Sarah Johnson",
            "company": "EcoFriendly Products",
            "email": "sarah@ecofriendly.com",
            "phone": "+1-555-0456",
            "industry": "Sustainability",
            "notes": "Eco-conscious brand looking to expand their digital presence. Values authentic, environmentally-focused messaging."
        },
        {
            "name": "Mike Chen",
            "company": "Local Restaurant Group",
            "email": "mike@localrestaurants.com",
            "phone": "+1-555-0789",
            "industry": "Food & Beverage",
            "notes": "Family-owned restaurant chain with 5 locations. Needs help with local SEO and social media marketing."
        },
        {
            "name": "Jennifer Martinez",
            "company": "Fitness First",
            "email": "jennifer@fitnessfirst.com",
            "phone": "+1-555-0321",
            "industry": "Health & Fitness",
            "notes": "Personal training studio expanding to online coaching. Requires content for both in-person and virtual services."
        },
        {
            "name": "David Wilson",
            "company": "Wilson Legal Services",
            "email": "david@wilsonlegal.com",
            "phone": "+1-555-0654",
            "industry": "Legal Services",
            "notes": "Small law firm specializing in business law. Conservative approach, needs professional and trustworthy content."
        }
    ]
    
    async with AsyncSessionLocal() as session:
        # Check if clients already exist
        existing_clients = await session.execute(select(Client))
        existing_count = len(existing_clients.scalars().all())
        
        if existing_count > 0:
            print(f"Found {existing_count} existing clients. Skipping sample data creation.")
            return
        
        print("Adding sample clients...")
        client_ids = []
        
        for client_data in sample_clients:
            client = Client(**client_data)
            session.add(client)
            await session.flush()  # Get the ID
            client_ids.append(client.id)
            print(f"Added client: {client_data['name']}")
        
        await session.commit()
        
        # Now add projects for these clients
        print("Adding sample projects...")
        
        sample_projects = [
            {
                "client_id": client_ids[0],  # TechStart Inc.
                "name": "AI Product Launch Campaign",
                "description": "Comprehensive marketing campaign for new AI-powered analytics platform",
                "project_type": "content_creation",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=30),
                "end_date": datetime.now() + timedelta(days=60),
                "budget": 50000.00
            },
            {
                "client_id": client_ids[0],  # TechStart Inc.
                "name": "Thought Leadership Content",
                "description": "Monthly blog posts and LinkedIn articles to establish CEO as industry thought leader",
                "project_type": "content_creation",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=15),
                "end_date": datetime.now() + timedelta(days=90),
                "budget": 15000.00
            },
            {
                "client_id": client_ids[1],  # EcoFriendly Products
                "name": "Earth Day Campaign",
                "description": "Social media and email campaign for Earth Day product promotion",
                "project_type": "social_media",
                "status": "review",
                "start_date": datetime.now() - timedelta(days=10),
                "end_date": datetime.now() + timedelta(days=20),
                "budget": 8000.00
            },
            {
                "client_id": client_ids[1],  # EcoFriendly Products
                "name": "Sustainability Blog Series",
                "description": "12-part blog series about sustainable living and eco-friendly practices",
                "project_type": "content_creation",
                "status": "draft",
                "start_date": datetime.now() - timedelta(days=5),
                "end_date": datetime.now() + timedelta(days=120),
                "budget": 12000.00
            },
            {
                "client_id": client_ids[2],  # Local Restaurant Group
                "name": "Local SEO Optimization",
                "description": "Google My Business optimization and local search content creation",
                "project_type": "seo",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=20),
                "end_date": datetime.now() + timedelta(days=45),
                "budget": 6000.00
            },
            {
                "client_id": client_ids[2],  # Local Restaurant Group
                "name": "Social Media Management",
                "description": "Daily social media posts and community engagement for all 5 locations",
                "project_type": "social_media",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=45),
                "end_date": datetime.now() + timedelta(days=90),
                "budget": 10000.00
            },
            {
                "client_id": client_ids[3],  # Fitness First
                "name": "Online Course Content",
                "description": "Video scripts and course materials for virtual fitness programs",
                "project_type": "content_creation",
                "status": "approved",
                "start_date": datetime.now() - timedelta(days=60),
                "end_date": datetime.now() + timedelta(days=30),
                "budget": 18000.00
            },
            {
                "client_id": client_ids[3],  # Fitness First
                "name": "Instagram Reels Campaign",
                "description": "Weekly fitness reels and workout content for Instagram",
                "project_type": "social_media",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=30),
                "end_date": datetime.now() + timedelta(days=60),
                "budget": 7500.00
            },
            {
                "client_id": client_ids[4],  # Wilson Legal Services
                "name": "Website Content Refresh",
                "description": "Update website copy and add new practice area pages",
                "project_type": "content_creation",
                "status": "draft",
                "start_date": datetime.now() - timedelta(days=7),
                "end_date": datetime.now() + timedelta(days=30),
                "budget": 5000.00
            },
            {
                "client_id": client_ids[4],  # Wilson Legal Services
                "name": "LinkedIn Thought Leadership",
                "description": "Monthly articles and posts to establish expertise in business law",
                "project_type": "content_creation",
                "status": "review",
                "start_date": datetime.now() - timedelta(days=20),
                "end_date": datetime.now() + timedelta(days=100),
                "budget": 8000.00
            }
        ]
        
        for project_data in sample_projects:
            project = Project(**project_data)
            session.add(project)
            print(f"Added project: {project_data['name']} for {project_data['client_id']}")
        
        await session.commit()
        print(f"Successfully added {len(sample_clients)} clients and {len(sample_projects)} projects!")


async def main():
    """Main function to run the script."""
    try:
        await add_sample_data()
    except Exception as e:
        print(f"Error adding sample data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
