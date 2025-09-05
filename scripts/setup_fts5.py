#!/usr/bin/env python3
"""
Setup FTS5 virtual table for keyword search
"""
import asyncio
import aiosqlite
from pathlib import Path

async def setup_fts5():
    """Create FTS5 virtual table for hybrid search"""
    db_path = Path("test.db")
    
    async with aiosqlite.connect(db_path) as db:
        # Create FTS5 virtual table for conversation chunks
        await db.execute("""
            CREATE VIRTUAL TABLE chunks_fts USING fts5(
                content,
                conversation_title,
                folder_name,
                chunk_type,
                content=chunks,
                content_rowid=rowid
            )
        """)
        
        # Create FTS5 virtual table for document chunks
        await db.execute("""
            CREATE VIRTUAL TABLE document_chunks_fts USING fts5(
                content,
                document_title,
                folder_name,
                file_type,
                content=document_chunks,
                content_rowid=rowid
            )
        """)
        
        # Create triggers to keep FTS5 tables in sync
        # For conversation chunks
        await db.execute("""
            CREATE TRIGGER chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(
                    rowid, content, conversation_title, folder_name, chunk_type
                ) VALUES (
                    new.rowid,
                    new.content,
                    (SELECT c.title FROM conversations c WHERE c.id = new.conversation_id),
                    (SELECT COALESCE(f.name, 'Root') FROM conversations c 
                     LEFT JOIN conversation_folders f ON c.folder_id = f.id 
                     WHERE c.id = new.conversation_id),
                    new.chunk_type
                );
            END
        """)
        
        await db.execute("""
            CREATE TRIGGER chunks_ad AFTER DELETE ON chunks BEGIN
                DELETE FROM chunks_fts WHERE rowid = old.rowid;
            END
        """)
        
        await db.execute("""
            CREATE TRIGGER chunks_au AFTER UPDATE ON chunks BEGIN
                DELETE FROM chunks_fts WHERE rowid = old.rowid;
                INSERT INTO chunks_fts(
                    rowid, content, conversation_title, folder_name, chunk_type
                ) VALUES (
                    new.rowid,
                    new.content,
                    (SELECT c.title FROM conversations c WHERE c.id = new.conversation_id),
                    (SELECT COALESCE(f.name, 'Root') FROM conversations c 
                     LEFT JOIN conversation_folders f ON c.folder_id = f.id 
                     WHERE c.id = new.conversation_id),
                    new.chunk_type
                );
            END
        """)
        
        # For document chunks
        await db.execute("""
            CREATE TRIGGER document_chunks_ai AFTER INSERT ON document_chunks BEGIN
                INSERT INTO document_chunks_fts(
                    rowid, content, document_title, folder_name, file_type
                ) VALUES (
                    new.rowid,
                    new.content,
                    (SELECT d.title FROM documents d WHERE d.id = new.document_id),
                    (SELECT COALESCE(f.name, 'Root') FROM documents d 
                     LEFT JOIN conversation_folders f ON d.folder_id = f.id 
                     WHERE d.id = new.document_id),
                    (SELECT d.file_type FROM documents d WHERE d.id = new.document_id)
                );
            END
        """)
        
        await db.execute("""
            CREATE TRIGGER document_chunks_ad AFTER DELETE ON document_chunks BEGIN
                DELETE FROM document_chunks_fts WHERE rowid = old.rowid;
            END
        """)
        
        await db.execute("""
            CREATE TRIGGER document_chunks_au AFTER UPDATE ON document_chunks BEGIN
                DELETE FROM document_chunks_fts WHERE rowid = old.rowid;
                INSERT INTO document_chunks_fts(
                    rowid, content, document_title, folder_name, file_type
                ) VALUES (
                    new.rowid,
                    new.content,
                    (SELECT d.title FROM documents d WHERE d.id = new.document_id),
                    (SELECT COALESCE(f.name, 'Root') FROM documents d 
                     LEFT JOIN conversation_folders f ON d.folder_id = f.id 
                     WHERE d.id = new.document_id),
                    (SELECT d.file_type FROM documents d WHERE d.id = new.document_id)
                );
            END
        """)
        
        await db.commit()
        print("✅ FTS5 virtual tables and triggers created successfully!")

if __name__ == "__main__":
    asyncio.run(setup_fts5())
