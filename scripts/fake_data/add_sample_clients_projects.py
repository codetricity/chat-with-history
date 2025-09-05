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
            "name": "Sony Corporation",
            "company": "Sony Corporation",
            "email": "us-marketing@sony.com",
            "phone": "+1-212-833-6800",
            "industry": "Electronics & Entertainment",
            "notes": "Global electronics and entertainment company expanding AI and gaming technologies in the US market. Focus on developer community engagement and B2B influencer marketing for their AI/ML platforms."
        },
        {
            "name": "Intel Corporation",
            "company": "Intel Corporation",
            "email": "developer-relations@intel.com",
            "phone": "+1-408-765-8080",
            "industry": "Semiconductors & Computing",
            "notes": "Leading semiconductor company with strong developer ecosystem. Looking to expand AI/ML developer tools and hardware in the US market through technical influencer partnerships."
        },
        {
            "name": "AMD",
            "company": "Advanced Micro Devices",
            "email": "marketing@amd.com",
            "phone": "+1-408-749-4000",
            "industry": "Semiconductors & Computing",
            "notes": "Competitive semiconductor company focusing on AI/ML acceleration and gaming. Seeking to build developer community and technical influencer relationships for US market expansion."
        },
        {
            "name": "Rapidus Corporation",
            "company": "Rapidus Corporation",
            "email": "us-expansion@rapidus.com",
            "phone": "+81-3-1234-5678",
            "industry": "Semiconductors",
            "notes": "Japanese semiconductor startup with advanced 2nm technology. New to US market, needs comprehensive developer outreach and technical content strategy for AI/ML applications."
        },
        {
            "name": "Ricoh Company",
            "company": "Ricoh Company",
            "email": "us-business@ricoh.com",
            "phone": "+1-973-882-2000",
            "industry": "Office Equipment & Technology",
            "notes": "Japanese multinational focusing on digital workplace solutions and AI-powered business automation. Expanding B2B AI solutions in the US market through technical influencer marketing."
        },
        {
            "name": "Canon Inc.",
            "company": "Canon Inc.",
            "email": "us-marketing@canon.com",
            "phone": "+1-516-328-5000",
            "industry": "Imaging & Technology",
            "notes": "Global imaging and camera technology company expanding AI-powered imaging solutions and developer tools in the US market. Focus on technical content and developer community building."
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
                "client_id": client_ids[0],  # Sony Corporation
                "name": "US AI Developer Community Launch",
                "description": "Comprehensive influencer marketing campaign targeting AI/ML developers in the US market. Focus on Sony's AI platforms and developer tools through technical content and developer influencer partnerships.",
                "project_type": "influencer_marketing",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=30),
                "end_date": datetime.now() + timedelta(days=90),
                "budget": 150000.00
            },
            {
                "client_id": client_ids[0],  # Sony Corporation
                "name": "Gaming AI SDK Documentation Strategy",
                "description": "Technical documentation and developer resources for Sony's gaming AI SDK. Content generation for developer onboarding and API documentation with influencer validation.",
                "project_type": "content_creation",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=15),
                "end_date": datetime.now() + timedelta(days=120),
                "budget": 75000.00
            },
            {
                "client_id": client_ids[1],  # Intel Corporation
                "name": "AI/ML Hardware Developer Outreach",
                "description": "B2B influencer marketing campaign targeting AI/ML developers and data scientists. Focus on Intel's AI acceleration hardware and developer tools for the US market.",
                "project_type": "influencer_marketing",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=20),
                "end_date": datetime.now() + timedelta(days=100),
                "budget": 200000.00
            },
            {
                "client_id": client_ids[1],  # Intel Corporation
                "name": "Technical Content for US Market Entry",
                "description": "Strategic content generation for Intel's AI/ML developer tools and hardware. Focus on industry verticals like healthcare, finance, and automotive AI applications.",
                "project_type": "content_creation",
                "status": "review",
                "start_date": datetime.now() - timedelta(days=10),
                "end_date": datetime.now() + timedelta(days=150),
                "budget": 100000.00
            },
            {
                "client_id": client_ids[2],  # AMD
                "name": "Developer Community Building Campaign",
                "description": "Comprehensive developer outreach and influencer marketing for AMD's AI/ML acceleration products. Focus on competitive positioning against Intel in the US market.",
                "project_type": "influencer_marketing",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=25),
                "end_date": datetime.now() + timedelta(days=110),
                "budget": 180000.00
            },
            {
                "client_id": client_ids[2],  # AMD
                "name": "Technical Documentation & SDK Strategy",
                "description": "Developer documentation and SDK improvement strategy based on influencer feedback. Content generation for technical tutorials and API documentation.",
                "project_type": "content_creation",
                "status": "draft",
                "start_date": datetime.now() - timedelta(days=5),
                "end_date": datetime.now() + timedelta(days=180),
                "budget": 85000.00
            },
            {
                "client_id": client_ids[3],  # Rapidus Corporation
                "name": "US Market Entry Strategy",
                "description": "Comprehensive US market entry strategy for Rapidus's 2nm semiconductor technology. Focus on AI/ML applications and developer community building through technical influencer partnerships.",
                "project_type": "strategic_planning",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=40),
                "end_date": datetime.now() + timedelta(days=200),
                "budget": 300000.00
            },
            {
                "client_id": client_ids[3],  # Rapidus Corporation
                "name": "Technical Content & Event Strategy",
                "description": "Content generation and event strategy for Rapidus's US market introduction. Focus on AI/ML conferences, developer meetups, and technical content creation.",
                "project_type": "content_creation",
                "status": "review",
                "start_date": datetime.now() - timedelta(days=15),
                "end_date": datetime.now() + timedelta(days=160),
                "budget": 120000.00
            },
            {
                "client_id": client_ids[4],  # Ricoh Company
                "name": "B2B AI Solutions Marketing",
                "description": "B2B influencer marketing campaign for Ricoh's AI-powered business automation solutions in the US market. Focus on enterprise decision-makers and technical influencers.",
                "project_type": "influencer_marketing",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=35),
                "end_date": datetime.now() + timedelta(days=130),
                "budget": 160000.00
            },
            {
                "client_id": client_ids[4],  # Ricoh Company
                "name": "Industry Vertical Content Strategy",
                "description": "Content generation strategy for specific US industry verticals (healthcare, finance, legal) using Ricoh's AI solutions. Technical content validated by industry influencers.",
                "project_type": "content_creation",
                "status": "draft",
                "start_date": datetime.now() - timedelta(days=8),
                "end_date": datetime.now() + timedelta(days=140),
                "budget": 90000.00
            },
            {
                "client_id": client_ids[5],  # Canon Inc.
                "name": "AI Imaging Solutions Developer Campaign",
                "description": "Developer-focused influencer marketing campaign for Canon's AI-powered imaging solutions and developer tools in the US market.",
                "project_type": "influencer_marketing",
                "status": "active",
                "start_date": datetime.now() - timedelta(days=28),
                "end_date": datetime.now() + timedelta(days=95),
                "budget": 140000.00
            },
            {
                "client_id": client_ids[5],  # Canon Inc.
                "name": "Technical Documentation & SDK Enhancement",
                "description": "Strategic plan for Canon's AI imaging SDK improvements and technical documentation. Content generation for developer onboarding and API documentation.",
                "project_type": "content_creation",
                "status": "review",
                "start_date": datetime.now() - timedelta(days=12),
                "end_date": datetime.now() + timedelta(days=170),
                "budget": 95000.00
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
