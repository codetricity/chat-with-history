#!/usr/bin/env python3
"""
Test script for embedding service with raw HTTP request
"""
import asyncio
import os
import aiohttp
import json
from dotenv import load_dotenv

async def test_embedding_raw():
    """Test embedding generation with raw HTTP request to OpenRouter"""
    print("🧪 Testing OpenRouter embedding API with raw HTTP...")
    
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return
    
    print(f"✅ Found API key: {api_key[:20]}...")
    
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": "test text"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                print(f"✅ Status: {response.status}")
                print(f"✅ Headers: {dict(response.headers)}")
                
                response_text = await response.text()
                print(f"✅ Response text: {response_text}")
                
                if response.status == 200:
                    try:
                        response_json = await response.json()
                        print(f"✅ Response JSON: {json.dumps(response_json, indent=2)}")
                        
                        if 'data' in response_json and response_json['data']:
                            embedding = response_json['data'][0]['embedding']
                            print(f"✅ Embedding length: {len(embedding)}")
                            print(f"✅ First 5 values: {embedding[:5]}")
                    except Exception as e:
                        print(f"❌ JSON parse error: {e}")
                else:
                    print(f"❌ HTTP error: {response.status}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_embedding_raw())
