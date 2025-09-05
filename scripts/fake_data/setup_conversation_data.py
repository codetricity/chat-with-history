#!/usr/bin/env python3
"""
Master script to set up all conversation-related sample data
Runs the scripts in the correct order to create a complete conversation browser dataset
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.fake_data.add_sample_conversation_folders import add_sample_conversation_folders
from scripts.fake_data.add_sample_conversations import add_sample_conversations
from scripts.fake_data.add_sample_messages import add_sample_messages


async def setup_conversation_data():
    """Set up all conversation-related sample data"""
    
    print("🚀 Setting up conversation browser sample data...")
    print("=" * 60)
    
    try:
        # Step 1: Create conversation folders
        print("\n📁 Step 1: Creating conversation folders...")
        await add_sample_conversation_folders()
        
        # Step 2: Create conversations
        print("\n💬 Step 2: Creating conversations...")
        await add_sample_conversations()
        
        # Step 3: Add messages to conversations
        print("\n📝 Step 3: Adding messages to conversations...")
        await add_sample_messages()
        
        print("\n" + "=" * 60)
        print("✅ Conversation browser sample data setup complete!")
        print("\nYou can now:")
        print("- Browse conversations by folder")
        print("- View conversation history")
        print("- Test the conversation browser interface")
        print("- Search and filter conversations")
        
    except Exception as e:
        print(f"\n❌ Error setting up conversation data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(setup_conversation_data())
