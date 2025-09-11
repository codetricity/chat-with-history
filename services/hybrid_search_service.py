"""
Hybrid Search Service combining FTS5 (BM25) and FAISS (semantic search)
"""
import uuid
import faiss
import numpy as np
import aiosqlite
from typing import List, Dict, Any, Optional, Tuple
from models import Chunk, ChunkEmbedding, DocumentChunk, DocumentChunkEmbedding, Conversation
from db import AsyncSessionLocal
from services.embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

class HybridSearchService:
    """Service for hybrid search combining keyword and semantic search"""
    
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.faiss_index = None
        self.chunk_id_to_index = {}  # Maps chunk_id to FAISS index position
        self.index_to_chunk_id = {}  # Maps FAISS index position to chunk_id
        self.embedding_dimension = 1536
        
    async def build_faiss_index(self) -> None:
        """Build FAISS index from all stored embeddings"""
        # Get all chunk embeddings
        chunk_embeddings = await self.embedding_service.get_all_chunk_embeddings()
        doc_chunk_embeddings = await self.embedding_service.get_all_document_chunk_embeddings()
        
        all_embeddings = chunk_embeddings + doc_chunk_embeddings
        
        if not all_embeddings:
            logger.warning("No embeddings found to build FAISS index")
            return
        
        # Create FAISS index
        self.faiss_index = faiss.IndexFlatIP(self.embedding_dimension)  # Inner product for cosine similarity
        
        # Prepare embeddings array
        embeddings_array = np.array([emb for _, emb in all_embeddings], dtype=np.float32)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings_array)
        
        # Add embeddings to index
        self.faiss_index.add(embeddings_array)
        
        # Build mapping dictionaries
        self.chunk_id_to_index = {chunk_id: i for i, (chunk_id, _) in enumerate(all_embeddings)}
        self.index_to_chunk_id = {i: chunk_id for i, (chunk_id, _) in enumerate(all_embeddings)}
        
        logger.info(f"Built FAISS index with {len(all_embeddings)} embeddings")
    
    async def keyword_search(
        self, 
        query: str, 
        limit: int = 10,
        search_type: str = "conversation"  # "conversation" or "document"
    ) -> List[Dict[str, Any]]:
        """
        Perform keyword search using FTS5
        
        Args:
            query: Search query
            limit: Maximum number of results
            search_type: Type of content to search ("conversation" or "document")
            
        Returns:
            List of search results with BM25 scores
        """
        from db import DATABASE_URL
        import os
        
        # Extract database path from DATABASE_URL
        if DATABASE_URL.startswith("sqlite+aiosqlite:///"):
            db_path = DATABASE_URL.replace("sqlite+aiosqlite:///", "")
            if db_path.startswith("./"):
                db_path = db_path[2:]
            if not os.path.isabs(db_path):
                db_path = os.path.abspath(db_path)
        else:
            db_path = "test.db"
        
        results = []
        
        try:
            async with aiosqlite.connect(db_path) as db:
                if search_type == "conversation":
                    # Search conversation chunks
                    cursor = await db.execute("""
                        SELECT 
                            c.id as chunk_id,
                            c.content,
                            c.chunk_type,
                            c.conversation_id,
                            c.chunk_index,
                            conv.title as conversation_title,
                            f.name as folder_name,
                            bm25(chunks_fts) as bm25_score
                        FROM chunks_fts
                        JOIN chunks c ON chunks_fts.rowid = c.rowid
                        LEFT JOIN conversations conv ON c.conversation_id = conv.id
                        LEFT JOIN conversation_folders f ON conv.folder_id = f.id
                        WHERE chunks_fts MATCH ?
                        ORDER BY bm25_score DESC
                        LIMIT ?
                    """, (query, limit))
                else:
                    # Search document chunks
                    cursor = await db.execute("""
                        SELECT 
                            dc.id as chunk_id,
                            dc.content,
                            dc.document_id,
                            dc.chunk_index,
                            d.title as document_title,
                            f.name as folder_name,
                            d.file_type,
                            bm25(document_chunks_fts) as bm25_score
                        FROM document_chunks_fts
                        JOIN document_chunks dc ON document_chunks_fts.rowid = dc.rowid
                        LEFT JOIN documents d ON dc.document_id = d.id
                        LEFT JOIN conversation_folders f ON d.folder_id = f.id
                        WHERE document_chunks_fts MATCH ?
                        ORDER BY bm25_score DESC
                        LIMIT ?
                    """, (query, limit))
                
                rows = await cursor.fetchall()
                
                for row in rows:
                    result = {
                        "chunk_id": str(row[0]),
                        "content": row[1],
                        "bm25_score": row[-1],  # Last column is BM25 score
                        "search_type": search_type
                    }
                    
                    if search_type == "conversation":
                        result.update({
                            "conversation_title": row[2],
                            "folder_name": row[3],
                            "chunk_type": row[4],
                            "conversation_id": str(row[5]),
                            "chunk_index": row[6]
                        })
                    else:
                        result.update({
                            "document_title": row[2],
                            "folder_name": row[3],
                            "file_type": row[4],
                            "document_id": str(row[5]),
                            "chunk_index": row[6]
                        })
                    
                    results.append(result)
        except Exception as e:
            if "no such table: chunks_fts" in str(e) or "no such table: document_chunks_fts" in str(e):
                logger.warning("FTS5 tables not available, returning empty results for keyword search")
                return []
            else:
                logger.error(f"Error in keyword search: {e}")
                return []
        
        return results
    
    async def semantic_search(
        self, 
        query: str, 
        limit: int = 10,
        search_type: str = "conversation"
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search using FAISS
        
        Args:
            query: Search query
            limit: Maximum number of results
            search_type: Type of content to search ("conversation" or "document")
            
        Returns:
            List of search results with cosine similarity scores
        """
        try:
            if not self.faiss_index:
                await self.build_faiss_index()
            
            if not self.faiss_index:
                logger.warning("FAISS index not available, returning empty results")
                return []
            
            # Generate embedding for query
            query_embedding = await self.embedding_service.generate_embedding(query)
            query_vector = np.array([query_embedding], dtype=np.float32)
            faiss.normalize_L2(query_vector)
            
            # Search FAISS index
            scores, indices = self.faiss_index.search(query_vector, limit)
            
            results = []
            for score, index in zip(scores[0], indices[0]):
                if index == -1:  # No more results
                    break
                    
                chunk_id = self.index_to_chunk_id.get(index)
                if not chunk_id:
                    continue
                
                # Get chunk details from database
                chunk_details = await self._get_chunk_details(chunk_id, search_type)
                if chunk_details:
                    chunk_details.update({
                        "cosine_score": float(score),
                        "search_type": search_type
                    })
                    results.append(chunk_details)
            
            return results
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            # Return empty results if semantic search fails
            return []
    
    async def hybrid_search(
        self, 
        query: str, 
        limit: int = 10,
        search_type: str = "conversation",
        bm25_weight: float = 0.35,
        cosine_weight: float = 0.65
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining BM25 and cosine similarity
        
        Args:
            query: Search query
            limit: Maximum number of results
            search_type: Type of content to search ("conversation" or "document")
            bm25_weight: Weight for BM25 scores (default 0.35)
            cosine_weight: Weight for cosine scores (default 0.65)
            
        Returns:
            List of search results with hybrid scores
        """
        try:
            # Get results from both search methods
            bm25_results = await self.keyword_search(query, limit * 2, search_type)
            semantic_results = await self.semantic_search(query, limit * 2, search_type)
        except Exception as e:
            logger.error(f"Error in hybrid search: {e}")
            # Return empty results if search fails
            return []
        
        # Create score dictionaries for easy lookup
        bm25_scores = {result["chunk_id"]: result["bm25_score"] for result in bm25_results}
        cosine_scores = {result["chunk_id"]: result["cosine_score"] for result in semantic_results}
        
        # Get all unique chunk IDs
        all_chunk_ids = set(bm25_scores.keys()) | set(cosine_scores.keys())
        
        # Calculate hybrid scores
        hybrid_results = []
        for chunk_id in all_chunk_ids:
            bm25_score = bm25_scores.get(chunk_id, 0.0)
            cosine_score = cosine_scores.get(chunk_id, 0.0)
            
            # Normalize scores (simple min-max normalization)
            # This is a basic approach - you might want to use more sophisticated normalization
            hybrid_score = (bm25_weight * bm25_score) + (cosine_weight * cosine_score)
            
            # Get the result details (prefer semantic results as they have more metadata)
            result_details = next(
                (r for r in semantic_results if r["chunk_id"] == chunk_id), 
                next((r for r in bm25_results if r["chunk_id"] == chunk_id), {})
            )
            
            if result_details:
                result_details.update({
                    "hybrid_score": hybrid_score,
                    "bm25_score": bm25_score,
                    "cosine_score": cosine_score
                })
                hybrid_results.append(result_details)
        
        # Sort by hybrid score and return top results
        hybrid_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return hybrid_results[:limit]
    
    async def _get_chunk_details(self, chunk_id: uuid.UUID, search_type: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a chunk"""
        async with AsyncSessionLocal() as session:
            from sqlmodel import select
            
            if search_type == "conversation":
                statement = select(Chunk).where(Chunk.id == chunk_id)
                result = await session.execute(statement)
                chunk = result.scalar_one_or_none()
                
                if chunk:
                    # Get conversation and folder details
                    conv_statement = select(Conversation).where(Conversation.id == chunk.conversation_id)
                    conv_result = await session.execute(conv_statement)
                    conversation = conv_result.scalar_one_or_none()
                    
                    folder_name = "Root"
                    if conversation and conversation.folder_id:
                        from models import ConversationFolder
                        folder_statement = select(ConversationFolder).where(ConversationFolder.id == conversation.folder_id)
                        folder_result = await session.execute(folder_statement)
                        folder = folder_result.scalar_one_or_none()
                        if folder:
                            folder_name = folder.name
                    
                    return {
                        "chunk_id": str(chunk.id),
                        "content": chunk.content,
                        "conversation_id": str(chunk.conversation_id),
                        "chunk_index": chunk.chunk_index,
                        "chunk_type": chunk.chunk_type,
                        "conversation_title": conversation.title if conversation else "Unknown",
                        "folder_name": folder_name
                    }
            else:
                statement = select(DocumentChunk).where(DocumentChunk.id == chunk_id)
                result = await session.execute(statement)
                chunk = result.scalar_one_or_none()
                
                if chunk:
                    # Get document and folder details
                    from models import Document, ConversationFolder
                    doc_statement = select(Document).where(Document.id == chunk.document_id)
                    doc_result = await session.execute(doc_statement)
                    document = doc_result.scalar_one_or_none()
                    
                    folder_name = "Root"
                    if document and document.folder_id:
                        folder_statement = select(ConversationFolder).where(ConversationFolder.id == document.folder_id)
                        folder_result = await session.execute(folder_statement)
                        folder = folder_result.scalar_one_or_none()
                        if folder:
                            folder_name = folder.name
                    
                    return {
                        "chunk_id": str(chunk.id),
                        "content": chunk.content,
                        "document_id": str(chunk.document_id),
                        "chunk_index": chunk.chunk_index,
                        "document_title": document.title if document else "Unknown",
                        "folder_name": folder_name,
                        "file_type": document.file_type if document else None
                    }
        
        return None
    
    async def search_all(
        self, 
        query: str, 
        limit: int = 10,
        search_type: str = "both"  # "conversation", "document", or "both"
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search both conversations and documents
        
        Args:
            query: Search query
            limit: Maximum number of results per type
            search_type: What to search ("conversation", "document", or "both")
            
        Returns:
            Dictionary with search results by type
        """
        results = {}
        
        if search_type in ["conversation", "both"]:
            results["conversations"] = await self.hybrid_search(query, limit, "conversation")
        
        if search_type in ["document", "both"]:
            results["documents"] = await self.hybrid_search(query, limit, "document")
        
        return results
