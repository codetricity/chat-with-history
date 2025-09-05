#!/usr/bin/env python3
"""
Check available OpenRouter models
"""
import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import os

async def check_models():
    """Check available OpenRouter models"""
    print("🔍 Checking available OpenRouter models...")
    
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return
    
    print(f"✅ Found API key: {api_key[:20]}...")
    
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                print(f"✅ Status: {response.status}")
                
                if response.status == 200:
                    response_json = await response.json()
                    print(f"✅ Found {len(response_json.get('data', []))} models")
                    
                    # Look for embedding models
                    embedding_models = []
                    for model in response_json.get('data', []):
                        model_id = model.get('id', '')
                        if 'embedding' in model_id.lower() or 'embed' in model_id.lower():
                            embedding_models.append(model)
                    
                    print(f"\n🎯 Found {len(embedding_models)} embedding models:")
                    for model in embedding_models:
                        print(f"  - {model.get('id')} ({model.get('context_length', 'N/A')} context)")
                        print(f"    Pricing: {model.get('pricing', {}).get('prompt', 'N/A')} per token")
                        print(f"    Description: {model.get('description', 'N/A')}")
                        print()
                    
                    if not embedding_models:
                        print("❌ No embedding models found")
                        print("\n📋 All available models:")
                        for model in response_json.get('data', [])[:10]:  # Show first 10
                            print(f"  - {model.get('id')}")
                        if len(response_json.get('data', [])) > 10:
                            print(f"  ... and {len(response_json.get('data', [])) - 10} more")
                else:
                    response_text = await response.text()
                    print(f"❌ Error: {response_text}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_models())
