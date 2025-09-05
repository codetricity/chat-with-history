#!/usr/bin/env python3
"""
Test script for the new LLM cache schema
"""
import asyncio
import uuid
import sys
import os
from datetime import datetime, timezone

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import create_tables, AsyncSessionLocal
from models import User, Conversation, Message, Chunk, ChunkEmbedding, Document, DocumentChunk
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.hybrid_search_service import HybridSearchService

async def test_schema():
    """Test the new schema with sample data"""
    print("🧪 Testing new LLM cache schema...")
    
    # Create tables
    await create_tables()
    print("✅ Database tables created")
    
    # Initialize services
    chunking_service = ChunkingService()
    embedding_service = EmbeddingService()
    search_service = HybridSearchService(embedding_service)
    
    async with AsyncSessionLocal() as session:
        # Create a test user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"✅ Created test user: {user.email}")
        
        # Create a test conversation
        conversation = Conversation(
            user_id=user.id,
            title="Test Conversation about AI and Machine Learning",
            is_active=True
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        print(f"✅ Created test conversation: {conversation.title}")
        
        # Create test messages
        messages = [
            Message(
                conversation_id=conversation.id,
                role="user",
                content="What is artificial intelligence and how does it work?",
                model="llama-3.3-70b"
            ),
            Message(
                conversation_id=conversation.id,
                role="assistant",
                content="Artificial Intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. AI systems can learn, reason, and make decisions similar to humans. There are several types of AI including machine learning, deep learning, and neural networks. Machine learning algorithms learn from data to make predictions or decisions without being explicitly programmed for every scenario.",
                model="llama-3.3-70b",
                token_count=150
            ),
            Message(
                conversation_id=conversation.id,
                role="user",
                content="Can you explain machine learning in more detail?",
                model="llama-3.3-70b"
            ),
            Message(
                conversation_id=conversation.id,
                role="assistant",
                content="Machine Learning (ML) is a subset of AI that focuses on algorithms that can learn and improve from experience. There are three main types: supervised learning (learning from labeled examples), unsupervised learning (finding patterns in data without labels), and reinforcement learning (learning through trial and error with rewards). Popular ML techniques include linear regression, decision trees, random forests, and neural networks. ML is used in applications like recommendation systems, image recognition, and natural language processing.",
                model="llama-3.3-70b",
                token_count=200
            )
        ]
        
        for message in messages:
            session.add(message)
        
        await session.commit()
        print(f"✅ Created {len(messages)} test messages")
        
        # Create a test document
        document = Document(
            user_id=user.id,
            title="AI Research Paper",
            content="This is a comprehensive research paper about artificial intelligence, machine learning, deep learning, neural networks, and their applications in various industries. The paper covers topics such as supervised learning, unsupervised learning, reinforcement learning, computer vision, natural language processing, and the future of AI technology.",
            file_type="pdf",
            is_active=True
        )
        session.add(document)
        await session.commit()
        await session.refresh(document)
        print(f"✅ Created test document: {document.title}")
    
    # Test chunking
    print("\n🔪 Testing chunking service...")
    chunks = await chunking_service.chunk_conversation(conversation.id)
    print(f"✅ Created {len(chunks)} chunks for conversation")
    
    doc_chunks = await chunking_service.chunk_document(document.id)
    print(f"✅ Created {len(doc_chunks)} chunks for document")
    
    # Test embedding generation (if API key is available)
    print("\n🧠 Testing embedding service...")
    try:
        embedding_test = await embedding_service.test_connection()
        print(f"✅ Embedding service test: {embedding_test}")
        
        if embedding_test["status"] == "success":
            # Generate embeddings for chunks
            for chunk in chunks[:2]:  # Test with first 2 chunks
                embedding = await embedding_service.generate_embedding(chunk.content)
                await embedding_service.store_chunk_embedding(chunk.id, embedding)
                print(f"✅ Generated and stored embedding for chunk {chunk.id}")
            
            # Test hybrid search
            print("\n🔍 Testing hybrid search...")
            
            # Setup FTS5 tables first
            print("📝 Setting up FTS5 virtual tables...")
            import subprocess
            result = subprocess.run(["uv", "run", "python", "scripts/setup_fts5.py"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ FTS5 tables created")
            else:
                print(f"⚠️  FTS5 setup warning: {result.stderr}")
            
            await search_service.build_faiss_index()
            
            # Test keyword search
            keyword_results = await search_service.keyword_search("machine learning", limit=5)
            print(f"✅ Keyword search found {len(keyword_results)} results")
            
            # Test semantic search
            semantic_results = await search_service.semantic_search("artificial intelligence", limit=5)
            print(f"✅ Semantic search found {len(semantic_results)} results")
            
            # Test hybrid search
            hybrid_results = await search_service.hybrid_search("AI and ML", limit=5)
            print(f"✅ Hybrid search found {len(hybrid_results)} results")
            
            if hybrid_results:
                print("\n📊 Sample hybrid search result:")
                result = hybrid_results[0]
                print(f"  Content: {result['content'][:100]}...")
                print(f"  Hybrid Score: {result['hybrid_score']:.4f}")
                print(f"  BM25 Score: {result['bm25_score']:.4f}")
                print(f"  Cosine Score: {result['cosine_score']:.4f}")
        else:
            print("⚠️  Embedding service not available (missing API key)")
    
    except Exception as e:
        print(f"⚠️  Embedding service test failed: {e}")
    
    print("\n🎉 Schema test completed successfully!")
    print("\n📋 Summary:")
    print(f"  - User: {user.email}")
    print(f"  - Conversation: {conversation.title}")
    print(f"  - Messages: {len(messages)}")
    print(f"  - Document: {document.title}")
    print(f"  - Conversation chunks: {len(chunks)}")
    print(f"  - Document chunks: {len(doc_chunks)}")
    print(f"  - FTS5 tables: chunks_fts, document_chunks_fts")
    print(f"  - FAISS index: {'Built' if search_service.faiss_index else 'Not built'}")

if __name__ == "__main__":
    asyncio.run(test_schema())
