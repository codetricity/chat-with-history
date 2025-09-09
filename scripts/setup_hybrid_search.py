#!/usr/bin/env python3
"""
Setup script for hybrid search infrastructure
Creates FTS5 virtual tables, chunks existing conversations, and generates embeddings
"""

import asyncio
import sys
import os
import aiosqlite
import logging

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.hybrid_search_service import HybridSearchService
from models import Conversation, Document
from db import AsyncSessionLocal

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_fts5_tables():
    """Create FTS5 virtual tables for full-text search"""
    logger.info("Creating FTS5 virtual tables...")
    
    db_path = "test.db"
    
    async with aiosqlite.connect(db_path) as db:
        # Enable FTS5 extension
        await db.execute("PRAGMA compile_options;")
        
        # Create FTS5 virtual table for conversation chunks
        await db.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                content,
                chunk_type,
                content='chunks',
                content_rowid='rowid'
            );
        """)
        
        # Create FTS5 virtual table for document chunks
        await db.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS document_chunks_fts USING fts5(
                content,
                content='document_chunks',
                content_rowid='rowid'
            );
        """)
        
        # Create triggers to keep FTS5 tables in sync
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, content, chunk_type) 
                VALUES (new.rowid, new.content, new.chunk_type);
            END;
        """)
        
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content, chunk_type) 
                VALUES('delete', old.rowid, old.content, old.chunk_type);
            END;
        """)
        
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, content, chunk_type) 
                VALUES('delete', old.rowid, old.content, old.chunk_type);
                INSERT INTO chunks_fts(rowid, content, chunk_type) 
                VALUES (new.rowid, new.content, new.chunk_type);
            END;
        """)
        
        # Similar triggers for document chunks
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS document_chunks_ai AFTER INSERT ON document_chunks BEGIN
                INSERT INTO document_chunks_fts(rowid, content) 
                VALUES (new.rowid, new.content);
            END;
        """)
        
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS document_chunks_ad AFTER DELETE ON document_chunks BEGIN
                INSERT INTO document_chunks_fts(document_chunks_fts, rowid, content) 
                VALUES('delete', old.rowid, old.content);
            END;
        """)
        
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS document_chunks_au AFTER UPDATE ON document_chunks BEGIN
                INSERT INTO document_chunks_fts(document_chunks_fts, rowid, content) 
                VALUES('delete', old.rowid, old.content);
                INSERT INTO document_chunks_fts(rowid, content) 
                VALUES (new.rowid, new.content);
            END;
        """)
        
        await db.commit()
        logger.info("✅ FTS5 virtual tables and triggers created successfully")


async def chunk_existing_conversations():
    """Chunk all existing conversations"""
    logger.info("Chunking existing conversations...")
    
    chunking_service = ChunkingService()
    
    async with AsyncSessionLocal() as session:
        from sqlmodel import select
        statement = select(Conversation).where(Conversation.is_active)
        result = await session.execute(statement)
        conversations = result.scalars().all()
        
        total_chunks = 0
        for conversation in conversations:
            try:
                chunks = await chunking_service.chunk_conversation(conversation.id)
                total_chunks += len(chunks)
                logger.info("Chunked conversation '%s' - %d chunks", conversation.title, len(chunks))
            except Exception as e:
                logger.error(f"Error chunking conversation {conversation.id}: {e}")
        
        logger.info(f"✅ Chunked {len(conversations)} conversations, created {total_chunks} total chunks")
        return total_chunks


async def chunk_existing_documents():
    """Chunk all existing documents"""
    logger.info("Chunking existing documents...")
    
    chunking_service = ChunkingService()
    
    async with AsyncSessionLocal() as session:
        from sqlmodel import select
        statement = select(Document).where(Document.is_active)
        result = await session.execute(statement)
        documents = result.scalars().all()
        
        total_chunks = 0
        for document in documents:
            try:
                chunks = await chunking_service.chunk_document(document.id)
                total_chunks += len(chunks)
                logger.info("Chunked document '%s' - %d chunks", document.title, len(chunks))
            except Exception as e:
                logger.error(f"Error chunking document {document.id}: {e}")
        
        logger.info(f"✅ Chunked {len(documents)} documents, created {total_chunks} total chunks")
        return total_chunks


async def generate_embeddings():
    """Generate embeddings for all chunks"""
    logger.info("Generating embeddings for all chunks...")
    
    embedding_service = EmbeddingService()
    
    # Generate embeddings for conversation chunks
    async with AsyncSessionLocal() as session:
        from sqlmodel import select
        from models import Chunk, ChunkEmbedding
        
        # Get all chunks without embeddings
        statement = (
            select(Chunk)
            .outerjoin(ChunkEmbedding, Chunk.id == ChunkEmbedding.chunk_id)
            .where(ChunkEmbedding.chunk_id.is_(None))
        )
        result = await session.execute(statement)
        chunks = result.scalars().all()
        
        logger.info(f"Generating embeddings for {len(chunks)} conversation chunks...")
        
        for i, chunk in enumerate(chunks):
            try:
                # Generate embedding
                embedding = await embedding_service.generate_embedding(chunk.content)
                
                # Store embedding
                await embedding_service.store_chunk_embedding(chunk.id, embedding)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Generated embeddings for {i + 1}/{len(chunks)} chunks")
                    
            except Exception as e:
                logger.error(f"Error generating embedding for chunk {chunk.id}: {e}")
        
        logger.info(f"✅ Generated embeddings for {len(chunks)} conversation chunks")
    
    # Generate embeddings for document chunks
    async with AsyncSessionLocal() as session:
        from sqlmodel import select
        from models import DocumentChunk, DocumentChunkEmbedding
        
        # Get all document chunks without embeddings
        statement = (
            select(DocumentChunk)
            .outerjoin(DocumentChunkEmbedding, DocumentChunk.id == DocumentChunkEmbedding.chunk_id)
            .where(DocumentChunkEmbedding.chunk_id.is_(None))
        )
        result = await session.execute(statement)
        doc_chunks = result.scalars().all()
        
        logger.info(f"Generating embeddings for {len(doc_chunks)} document chunks...")
        
        for i, chunk in enumerate(doc_chunks):
            try:
                # Generate embedding
                embedding = await embedding_service.generate_embedding(chunk.content)
                
                # Store embedding
                await embedding_service.store_document_chunk_embedding(chunk.id, embedding)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Generated embeddings for {i + 1}/{len(doc_chunks)} chunks")
                    
            except Exception as e:
                logger.error(f"Error generating embedding for document chunk {chunk.id}: {e}")
        
        logger.info(f"✅ Generated embeddings for {len(doc_chunks)} document chunks")


async def build_faiss_index():
    """Build FAISS index from all embeddings"""
    logger.info("Building FAISS index...")
    
    embedding_service = EmbeddingService()
    hybrid_service = HybridSearchService(embedding_service)
    
    await hybrid_service.build_faiss_index()
    logger.info("✅ FAISS index built successfully")


async def test_hybrid_search():
    """Test the hybrid search functionality"""
    logger.info("Testing hybrid search functionality...")
    
    embedding_service = EmbeddingService()
    hybrid_service = HybridSearchService(embedding_service)
    
    # Test queries
    test_queries = [
        "marketing strategy",
        "social media",
        "client meeting",
        "project timeline"
    ]
    
    for query in test_queries:
        logger.info(f"\nTesting query: '{query}'")
        
        try:
            # Test keyword search
            keyword_results = await hybrid_service.keyword_search(query, limit=3)
            logger.info(f"Keyword search found {len(keyword_results)} results")
            
            # Test semantic search
            semantic_results = await hybrid_service.semantic_search(query, limit=3)
            logger.info(f"Semantic search found {len(semantic_results)} results")
            
            # Test hybrid search
            hybrid_results = await hybrid_service.hybrid_search(query, limit=3)
            logger.info(f"Hybrid search found {len(hybrid_results)} results")
            
        except Exception as e:
            logger.error(f"Error testing query '{query}': {e}")
    
    logger.info("✅ Hybrid search testing completed")


async def setup_hybrid_search():
    """Complete setup for hybrid search infrastructure"""
    logger.info("🚀 Setting up hybrid search infrastructure...")
    logger.info("=" * 60)
    
    try:
        # Step 1: Create FTS5 virtual tables
        logger.info("\n📊 Step 1: Creating FTS5 virtual tables...")
        await create_fts5_tables()
        
        # Step 2: Chunk existing conversations
        logger.info("\n📝 Step 2: Chunking existing conversations...")
        conv_chunks = await chunk_existing_conversations()
        
        # Step 3: Chunk existing documents
        logger.info("\n📄 Step 3: Chunking existing documents...")
        doc_chunks = await chunk_existing_documents()
        
        # Step 4: Generate embeddings
        logger.info("\n🧠 Step 4: Generating embeddings...")
        await generate_embeddings()
        
        # Step 5: Build FAISS index
        logger.info("\n🔍 Step 5: Building FAISS index...")
        await build_faiss_index()
        
        # Step 6: Test hybrid search
        logger.info("\n🧪 Step 6: Testing hybrid search...")
        await test_hybrid_search()
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Hybrid search infrastructure setup complete!")
        logger.info(f"\n📊 Summary:")
        logger.info(f"  - FTS5 virtual tables created")
        logger.info(f"  - {conv_chunks} conversation chunks created")
        logger.info(f"  - {doc_chunks} document chunks created")
        logger.info(f"  - Embeddings generated for all chunks")
        logger.info(f"  - FAISS index built and ready")
        logger.info(f"\n🔍 Hybrid search is now ready to use!")
        
    except Exception as e:
        logger.error(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(setup_hybrid_search())
