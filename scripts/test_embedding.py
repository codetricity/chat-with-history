#!/usr/bin/env python3
"""
Test script for embedding service debugging
"""
import asyncio
import os
from openai import AsyncOpenAI

async def test_embedding():
    """Test embedding generation with OpenRouter"""
    print("🧪 Testing OpenRouter embedding API...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return
    
    print(f"✅ Found API key: {api_key[:20]}...")
    
    # Set the environment variable for OpenAI client
    os.environ["OPENAI_API_KEY"] = api_key
    
    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        print("📡 Making API call...")
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input="test text"
        )
        
        print(f"✅ Response type: {type(response)}")
        print(f"✅ Response: {response}")
        print(f"✅ Response attributes: {dir(response)}")
        
        # Try to access as dict first
        if isinstance(response, dict):
            print(f"✅ Response as dict keys: {response.keys()}")
            if 'data' in response:
                print(f"✅ Response['data'] type: {type(response['data'])}")
                print(f"✅ Response['data'] length: {len(response['data'])}")
                if response['data']:
                    print(f"✅ First item: {response['data'][0]}")
                    if 'embedding' in response['data'][0]:
                        print(f"✅ Embedding length: {len(response['data'][0]['embedding'])}")
                        print(f"✅ First 5 embedding values: {response['data'][0]['embedding'][:5]}")
        else:
            print("❌ Response is not a dict")
            
        if hasattr(response, 'data'):
            print(f"✅ Response.data type: {type(response.data)}")
            print(f"✅ Response.data length: {len(response.data)}")
            if response.data:
                print(f"✅ First item type: {type(response.data[0])}")
                print(f"✅ First item attributes: {dir(response.data[0])}")
                if hasattr(response.data[0], 'embedding'):
                    print(f"✅ Embedding length: {len(response.data[0].embedding)}")
                    print(f"✅ First 5 embedding values: {response.data[0].embedding[:5]}")
                else:
                    print("❌ No embedding attribute found")
        else:
            print("❌ No data attribute found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_embedding())
