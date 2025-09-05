"""
Chunking Service for breaking conversations and documents into searchable chunks
"""
import uuid
import re
from typing import List, Optional
from models import Chunk, Message, Conversation, Document, DocumentChunk
from db import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)

class ChunkingService:
    """Service for chunking conversations and documents"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                search_start = max(start + self.chunk_size - 100, start)
                sentence_end = text.rfind('.', search_start, end)
                if sentence_end > start:
                    end = sentence_end + 1
                else:
                    # Look for other natural break points
                    for break_char in ['\n', '!', '?', ';']:
                        break_point = text.rfind(break_char, search_start, end)
                        if break_point > start:
                            end = break_point + 1
                            break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        return chunks
    
    async def chunk_conversation(self, conversation_id: uuid.UUID) -> List[Chunk]:
        """
        Chunk all messages in a conversation
        
        Args:
            conversation_id: ID of the conversation to chunk
            
        Returns:
            List of created chunks
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            
            # Get all messages for the conversation
            statement = select(Message).where(Message.conversation_id == conversation_id)
            result = await session.execute(statement)
            messages = result.scalars().all()
            
            chunks = []
            chunk_index = 0
            
            for message in messages:
                # Split message content into chunks
                message_chunks = self.split_text(message.content)
                
                for i, chunk_content in enumerate(message_chunks):
                    chunk = Chunk(
                        conversation_id=conversation_id,
                        content=chunk_content,
                        chunk_index=chunk_index,
                        chunk_type=message.role,
                        message_id=message.id
                    )
                    session.add(chunk)
                    chunks.append(chunk)
                    chunk_index += 1
            
            await session.commit()
            
            # Refresh all chunks to get their IDs
            for chunk in chunks:
                await session.refresh(chunk)
            
            logger.info(f"Created {len(chunks)} chunks for conversation {conversation_id}")
            return chunks
    
    async def chunk_document(self, document_id: uuid.UUID) -> List[DocumentChunk]:
        """
        Chunk a document into searchable pieces
        
        Args:
            document_id: ID of the document to chunk
            
        Returns:
            List of created document chunks
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            
            # Get the document
            document = await session.get(Document, document_id)
            if not document:
                raise ValueError(f"Document {document_id} not found")
            
            # Split document content into chunks
            content_chunks = self.split_text(document.content)
            
            chunks = []
            for i, chunk_content in enumerate(content_chunks):
                chunk = DocumentChunk(
                    document_id=document_id,
                    content=chunk_content,
                    chunk_index=i
                )
                session.add(chunk)
                chunks.append(chunk)
            
            await session.commit()
            
            # Refresh all chunks to get their IDs
            for chunk in chunks:
                await session.refresh(chunk)
            
            logger.info(f"Created {len(chunks)} chunks for document {document_id}")
            return chunks
    
    async def re_chunk_conversation(self, conversation_id: uuid.UUID) -> List[Chunk]:
        """
        Re-chunk a conversation (delete existing chunks and create new ones)
        
        Args:
            conversation_id: ID of the conversation to re-chunk
            
        Returns:
            List of new chunks
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select, delete
            
            # Delete existing chunks
            delete_statement = delete(Chunk).where(Chunk.conversation_id == conversation_id)
            await session.execute(delete_statement)
            
            # Create new chunks
            await session.commit()
            return await self.chunk_conversation(conversation_id)
    
    async def re_chunk_document(self, document_id: uuid.UUID) -> List[DocumentChunk]:
        """
        Re-chunk a document (delete existing chunks and create new ones)
        
        Args:
            document_id: ID of the document to re-chunk
            
        Returns:
            List of new chunks
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import delete
            
            # Delete existing chunks
            delete_statement = delete(DocumentChunk).where(DocumentChunk.document_id == document_id)
            await session.execute(delete_statement)
            
            # Create new chunks
            await session.commit()
            return await self.chunk_document(document_id)
    
    async def get_conversation_chunks(self, conversation_id: uuid.UUID) -> List[Chunk]:
        """
        Get all chunks for a conversation
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            List of chunks ordered by chunk_index
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            statement = (
                select(Chunk)
                .where(Chunk.conversation_id == conversation_id)
                .order_by(Chunk.chunk_index)
            )
            result = await session.execute(statement)
            return list(result.scalars().all())
    
    async def get_document_chunks(self, document_id: uuid.UUID) -> List[DocumentChunk]:
        """
        Get all chunks for a document
        
        Args:
            document_id: ID of the document
            
        Returns:
            List of chunks ordered by chunk_index
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            statement = (
                select(DocumentChunk)
                .where(DocumentChunk.document_id == document_id)
                .order_by(DocumentChunk.chunk_index)
            )
            result = await session.execute(statement)
            return list(result.scalars().all())
    
    async def chunk_all_conversations(self) -> int:
        """
        Chunk all existing conversations
        
        Returns:
            Total number of chunks created
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            statement = select(Conversation).where(Conversation.is_active == True)
            result = await session.execute(statement)
            conversations = result.scalars().all()
            
            total_chunks = 0
            for conversation in conversations:
                chunks = await self.chunk_conversation(conversation.id)
                total_chunks += len(chunks)
            
            logger.info(f"Chunked {len(conversations)} conversations, created {total_chunks} total chunks")
            return total_chunks
    
    async def chunk_all_documents(self) -> int:
        """
        Chunk all existing documents
        
        Returns:
            Total number of chunks created
        """
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            statement = select(Document).where(Document.is_active == True)
            result = await session.execute(statement)
            documents = result.scalars().all()
            
            total_chunks = 0
            for document in documents:
                chunks = await self.chunk_document(document.id)
                total_chunks += len(chunks)
            
            logger.info(f"Chunked {len(documents)} documents, created {total_chunks} total chunks")
            return total_chunks
