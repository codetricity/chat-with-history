"""
Embedding Service for generating and managing embeddings using OpenAI API
"""
import os
import uuid
import numpy as np
from typing import List, Optional, Tuple
from openai import AsyncOpenAI
from models import Chunk, ChunkEmbedding, DocumentChunk, DocumentChunkEmbedding
from db import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating and managing embeddings"""
    
    def __init__(self):
        # Use OpenAI API for embeddings
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model_name = "text-embedding-3-small"  # 1536 dimensions
        self.embedding_dimension = 1536
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using OpenAI API
        
        Args:
            text: Text to embed
            
        Returns:
            List of float values representing the embedding
        """
        try:
            response = await self.client.embeddings.create(
                model=self.model_name,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch using OpenAI API
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        try:
            response = await self.client.embeddings.create(
                model=self.model_name,
                input=texts
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise
    
    def float32_to_bytes(self, embedding: List[float]) -> bytes:
        """Convert float32 list to bytes for storage"""
        return np.array(embedding, dtype=np.float32).tobytes()
    
    def bytes_to_float32(self, embedding_bytes: bytes) -> List[float]:
        """Convert bytes back to float32 list"""
        return np.frombuffer(embedding_bytes, dtype=np.float32).tolist()
    
    async def store_chunk_embedding(
        self, 
        chunk_id: uuid.UUID, 
        embedding: List[float]
    ) -> ChunkEmbedding:
        """
        Store embedding for a conversation chunk
        
        Args:
            chunk_id: ID of the chunk
            embedding: Embedding vector
            
        Returns:
            ChunkEmbedding object
        """
        async with AsyncSessionLocal() as session:
            chunk_embedding = ChunkEmbedding(
                chunk_id=chunk_id,
                embedding=self.float32_to_bytes(embedding),
                model_name=self.model_name,
                embedding_dimension=self.embedding_dimension
            )
            session.add(chunk_embedding)
            await session.commit()
            await session.refresh(chunk_embedding)
            return chunk_embedding
    
    async def store_document_chunk_embedding(
        self, 
        chunk_id: uuid.UUID, 
        embedding: List[float]
    ) -> DocumentChunkEmbedding:
        """
        Store embedding for a document chunk
        
        Args:
            chunk_id: ID of the document chunk
            embedding: Embedding vector
            
        Returns:
            DocumentChunkEmbedding object
        """
        async with AsyncSessionLocal() as session:
            chunk_embedding = DocumentChunkEmbedding(
                chunk_id=chunk_id,
                embedding=self.float32_to_bytes(embedding),
                model_name=self.model_name,
                embedding_dimension=self.embedding_dimension
            )
            session.add(chunk_embedding)
            await session.commit()
            await session.refresh(chunk_embedding)
            return chunk_embedding
    
    async def get_chunk_embedding(self, chunk_id: uuid.UUID) -> Optional[List[float]]:
        """
        Retrieve embedding for a chunk
        
        Args:
            chunk_id: ID of the chunk
            
        Returns:
            Embedding vector or None if not found
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            statement = select(ChunkEmbedding).where(ChunkEmbedding.chunk_id == chunk_id)
            result = await session.execute(statement)
            chunk_embedding = result.scalar_one_or_none()
            
            if chunk_embedding:
                return self.bytes_to_float32(chunk_embedding.embedding)
            return None
    
    async def get_document_chunk_embedding(self, chunk_id: uuid.UUID) -> Optional[List[float]]:
        """
        Retrieve embedding for a document chunk
        
        Args:
            chunk_id: ID of the document chunk
            
        Returns:
            Embedding vector or None if not found
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            statement = select(DocumentChunkEmbedding).where(DocumentChunkEmbedding.chunk_id == chunk_id)
            result = await session.execute(statement)
            chunk_embedding = result.scalar_one_or_none()
            
            if chunk_embedding:
                return self.bytes_to_float32(chunk_embedding.embedding)
            return None
    
    async def get_all_chunk_embeddings(self) -> List[Tuple[uuid.UUID, List[float]]]:
        """
        Get all chunk embeddings for building FAISS index
        
        Returns:
            List of (chunk_id, embedding) tuples
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            statement = select(ChunkEmbedding)
            result = await session.execute(statement)
            chunk_embeddings = result.scalars().all()
            
            return [
                (ce.chunk_id, self.bytes_to_float32(ce.embedding))
                for ce in chunk_embeddings
            ]
    
    async def get_all_document_chunk_embeddings(self) -> List[Tuple[uuid.UUID, List[float]]]:
        """
        Get all document chunk embeddings for building FAISS index
        
        Returns:
            List of (chunk_id, embedding) tuples
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            statement = select(DocumentChunkEmbedding)
            result = await session.execute(statement)
            chunk_embeddings = result.scalars().all()
            
            return [
                (ce.chunk_id, self.bytes_to_float32(ce.embedding))
                for ce in chunk_embeddings
            ]
    
    async def test_connection(self) -> dict:
        """
        Test the embedding service connection
        
        Returns:
            Dictionary with test results
        """
        try:
            test_embedding = await self.generate_embedding("test")
            return {
                "status": "success",
                "model": self.model_name,
                "dimension": self.embedding_dimension,
                "test_embedding_length": len(test_embedding)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
