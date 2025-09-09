"""
Marketing firm API routes for client management, projects, content templates, and status tracking
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
import uuid
import logging

from db import get_session
from models import (
    Client, Project, ContentTemplate, ContentStatus, ContentTag, ConversationTag, Message,
    ClientCreate, ClientUpdate, ProjectCreate, ProjectUpdate, 
    ContentTemplateCreate, ContentTemplateUpdate, ContentStatusCreate, ContentStatusUpdate,
    ContentTagCreate, ContentTagUpdate
)
from services.client_service import ClientService
from services.content_template_service import ContentTemplateService
from services.content_status_service import ContentStatusService
from services.content_tag_service import ContentTagService
from services.hybrid_search_service import HybridSearchService
from services.embedding_service import EmbeddingService

router = APIRouter(prefix="/api", tags=["marketing"])

# Initialize services
client_service = ClientService()
template_service = ContentTemplateService()
status_service = ContentStatusService()
tag_service = ContentTagService()

# Set up logging
logger = logging.getLogger(__name__)


# =========================
# Client Management Endpoints
# =========================

@router.get("/clients", response_model=List[Client])
async def get_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get all active clients"""
    return await client_service.get_clients(session, skip=skip, limit=limit)


@router.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: UUID, session: Session = Depends(get_session)):
    """Get a specific client by ID"""
    client = await client_service.get_client(session, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/clients", response_model=Client)
async def create_client(client_data: ClientCreate, session: Session = Depends(get_session)):
    """Create a new client"""
    return await client_service.create_client(session, client_data)


@router.put("/clients/{client_id}", response_model=Client)
async def update_client(
    client_id: UUID, 
    client_data: ClientUpdate, 
    session: Session = Depends(get_session)
):
    """Update an existing client"""
    client = await client_service.update_client(session, client_id, client_data)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.delete("/clients/{client_id}")
async def delete_client(client_id: UUID, session: Session = Depends(get_session)):
    """Delete a client (soft delete)"""
    success = await client_service.delete_client(session, client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}


# =========================
# Project Management Endpoints
# =========================

@router.get("/projects", response_model=List[Project])
async def get_projects(
    client_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get all active projects, optionally filtered by client"""
    return await client_service.get_projects(session, client_id=client_id, skip=skip, limit=limit)


@router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: UUID, session: Session = Depends(get_session)):
    """Get a specific project by ID"""
    project = await client_service.get_project(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/projects", response_model=Project)
async def create_project(project_data: ProjectCreate, session: Session = Depends(get_session)):
    """Create a new project"""
    return await client_service.create_project(session, project_data)


@router.put("/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: UUID, 
    project_data: ProjectUpdate, 
    session: Session = Depends(get_session)
):
    """Update an existing project"""
    project = await client_service.update_project(session, project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/projects/{project_id}")
async def delete_project(project_id: UUID, session: Session = Depends(get_session)):
    """Delete a project (soft delete)"""
    success = await client_service.delete_project(session, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


# =========================
# Content Template Endpoints
# =========================

@router.get("/content-templates", response_model=List[ContentTemplate])
async def get_content_templates(
    content_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get all active content templates, optionally filtered by type"""
    return await template_service.get_templates(session, content_type=content_type, skip=skip, limit=limit)


@router.get("/content-templates/{template_id}", response_model=ContentTemplate)
async def get_content_template(template_id: UUID, session: Session = Depends(get_session)):
    """Get a specific content template by ID"""
    template = await template_service.get_template(session, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Content template not found")
    return template


@router.post("/content-templates", response_model=ContentTemplate)
async def create_content_template(
    template_data: ContentTemplateCreate, 
    session: Session = Depends(get_session)
):
    """Create a new content template"""
    return await template_service.create_template(session, template_data)


@router.put("/content-templates/{template_id}", response_model=ContentTemplate)
async def update_content_template(
    template_id: UUID, 
    template_data: ContentTemplateUpdate, 
    session: Session = Depends(get_session)
):
    """Update an existing content template"""
    template = await template_service.update_template(session, template_id, template_data)
    if not template:
        raise HTTPException(status_code=404, detail="Content template not found")
    return template


@router.delete("/content-templates/{template_id}")
async def delete_content_template(template_id: UUID, session: Session = Depends(get_session)):
    """Delete a content template (soft delete)"""
    success = await template_service.delete_template(session, template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content template not found")
    return {"message": "Content template deleted successfully"}


# =========================
# Content Status Endpoints
# =========================

@router.get("/content-status", response_model=List[ContentStatus])
async def get_content_statuses(
    conversation_id: Optional[UUID] = Query(None),
    project_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get content statuses with optional filters"""
    return await status_service.get_statuses(
        session, 
        conversation_id=conversation_id,
        project_id=project_id,
        status=status,
        skip=skip, 
        limit=limit
    )


@router.get("/content-status/summary")
async def get_content_status_summary(session: Session = Depends(get_session)):
    """Get summary of content statuses for dashboard"""
    return await status_service.get_status_summary(session)


@router.get("/content-status/{status_id}", response_model=ContentStatus)
async def get_content_status(status_id: UUID, session: Session = Depends(get_session)):
    """Get a specific content status by ID"""
    status = await status_service.get_status(session, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Content status not found")
    return status


@router.post("/content-status", response_model=ContentStatus)
async def create_content_status(
    status_data: ContentStatusCreate, 
    session: Session = Depends(get_session)
):
    """Create a new content status"""
    return await status_service.create_status(session, status_data)


@router.put("/content-status/{status_id}", response_model=ContentStatus)
async def update_content_status(
    status_id: UUID, 
    status_data: ContentStatusUpdate, 
    session: Session = Depends(get_session)
):
    """Update an existing content status"""
    status = await status_service.update_status(session, status_id, status_data)
    if not status:
        raise HTTPException(status_code=404, detail="Content status not found")
    return status


@router.delete("/content-status/{status_id}")
async def delete_content_status(status_id: UUID, session: Session = Depends(get_session)):
    """Delete a content status"""
    success = await status_service.delete_status(session, status_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content status not found")
    return {"message": "Content status deleted successfully"}


# =========================
# Content Tag Endpoints
# =========================

@router.get("/content-tags", response_model=List[ContentTag])
async def get_content_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get all active content tags"""
    return await tag_service.get_tags(session, skip=skip, limit=limit)


@router.get("/content-tags/{tag_id}", response_model=ContentTag)
async def get_content_tag(tag_id: UUID, session: Session = Depends(get_session)):
    """Get a specific content tag by ID"""
    tag = await tag_service.get_tag(session, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Content tag not found")
    return tag


@router.post("/content-tags", response_model=ContentTag)
async def create_content_tag(
    tag_data: ContentTagCreate, 
    session: Session = Depends(get_session)
):
    """Create a new content tag"""
    return await tag_service.create_tag(session, tag_data)


@router.put("/content-tags/{tag_id}", response_model=ContentTag)
async def update_content_tag(
    tag_id: UUID, 
    tag_data: ContentTagUpdate, 
    session: Session = Depends(get_session)
):
    """Update an existing content tag"""
    tag = await tag_service.update_tag(session, tag_id, tag_data)
    if not tag:
        raise HTTPException(status_code=404, detail="Content tag not found")
    return tag


@router.delete("/content-tags/{tag_id}")
async def delete_content_tag(tag_id: UUID, session: Session = Depends(get_session)):
    """Delete a content tag (soft delete)"""
    success = await tag_service.delete_tag(session, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content tag not found")
    return {"message": "Content tag deleted successfully"}


# =========================
# Conversation Tag Management
# =========================

@router.post("/conversations/{conversation_id}/tags/{tag_id}")
async def add_tag_to_conversation(
    conversation_id: UUID, 
    tag_id: UUID, 
    session: Session = Depends(get_session)
):
    """Add a tag to a conversation"""
    success = await tag_service.add_tag_to_conversation(session, conversation_id, tag_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add tag to conversation")
    return {"message": "Tag added to conversation successfully"}


@router.delete("/conversations/{conversation_id}/tags/{tag_id}")
async def remove_tag_from_conversation(
    conversation_id: UUID, 
    tag_id: UUID, 
    session: Session = Depends(get_session)
):
    """Remove a tag from a conversation"""
    success = await tag_service.remove_tag_from_conversation(session, conversation_id, tag_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to remove tag from conversation")
    return {"message": "Tag removed from conversation successfully"}


@router.get("/conversations/{conversation_id}/tags", response_model=List[ContentTag])
async def get_conversation_tags(
    conversation_id: UUID, 
    session: Session = Depends(get_session)
):
    """Get all tags for a conversation"""
    return await tag_service.get_conversation_tags(session, conversation_id)


# =========================
# Conversation Endpoints
# =========================

@router.get("/conversations")
async def get_conversations(session: AsyncSession = Depends(get_session)):
    """Get all conversations"""
    try:
        from sqlmodel import select
        from models import Conversation, ConversationFolder, User
        
        # Get all conversations with their folders and users
        result = await session.execute(
            select(Conversation, ConversationFolder, User)
            .join(ConversationFolder, Conversation.folder_id == ConversationFolder.id, isouter=True)
            .join(User, Conversation.user_id == User.id, isouter=True)
            .where(Conversation.is_active)
            .order_by(Conversation.updated_at.desc())
        )
        
        conversations = []
        for conv, folder, user in result:
            conversations.append({
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "folder": {
                    "id": str(folder.id) if folder else None,
                    "name": folder.name if folder else None
                } if folder else None,
                "user": {
                    "id": str(user.id) if user else None,
                    "email": user.email if user else None
                } if user else None
            })
        
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversations: {str(e)}")

@router.get("/folders")
async def get_folders(session: AsyncSession = Depends(get_session)):
    """Get all conversation folders"""
    try:
        from sqlmodel import select
        from models import ConversationFolder, User
        
        # Get all folders with their users
        result = await session.execute(
            select(ConversationFolder, User)
            .join(User, ConversationFolder.user_id == User.id, isouter=True)
            .where(ConversationFolder.is_active == True)
            .order_by(ConversationFolder.name)
        )
        
        folders = []
        for folder, user in result:
            folders.append({
                "id": str(folder.id),
                "name": folder.name,
                "description": folder.description,
                "parent_folder_id": str(folder.parent_folder_id) if folder.parent_folder_id else None,
                "created_at": folder.created_at.isoformat(),
                "updated_at": folder.updated_at.isoformat(),
                "user": {
                    "id": str(user.id) if user else None,
                    "email": user.email if user else None
                } if user else None
            })
        
        return folders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch folders: {str(e)}")

@router.get("/folders/hierarchy")
async def get_folder_hierarchy_marketing(session: AsyncSession = Depends(get_session)):
    """Get the complete folder hierarchy with conversations"""
    try:
        from sqlmodel import select
        from models import ConversationFolder, User, Conversation
        
        # Get all folders with their users
        folders_result = await session.execute(
            select(ConversationFolder, User)
            .join(User, ConversationFolder.user_id == User.id, isouter=True)
            .where(ConversationFolder.is_active == True)
            .order_by(ConversationFolder.name)
        )
        
        # Get all conversations with their folders
        conversations_result = await session.execute(
            select(Conversation, ConversationFolder)
            .join(ConversationFolder, Conversation.folder_id == ConversationFolder.id, isouter=True)
            .where(Conversation.is_active)
            .order_by(Conversation.updated_at.desc())
        )
        
        # Build folder hierarchy
        folders = {}
        root_folders = []
        
        for folder, user in folders_result:
            folder_data = {
                "id": str(folder.id),
                "name": folder.name,
                "description": folder.description,
                "parent_folder_id": str(folder.parent_folder_id) if folder.parent_folder_id else None,
                "created_at": folder.created_at.isoformat(),
                "updated_at": folder.updated_at.isoformat(),
                "user": {
                    "id": str(user.id) if user else None,
                    "email": user.email if user else None
                } if user else None,
                "conversations": [],
                "sub_folders": []
            }
            folders[str(folder.id)] = folder_data
            
            if folder.parent_folder_id:
                parent_id = str(folder.parent_folder_id)
                if parent_id in folders:
                    folders[parent_id]["sub_folders"].append(folder_data)
            else:
                root_folders.append(folder_data)
        
        # Add conversations to folders
        for conversation, folder in conversations_result:
            # Get message count for this conversation
            message_count_result = await session.execute(
                select(func.count(Message.id))
                .where(Message.conversation_id == conversation.id)
            )
            message_count = message_count_result.scalar() or 0
            
            conv_data = {
                "id": str(conversation.id),
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "message_count": message_count
            }
            
            if folder:
                folder_id = str(folder.id)
                if folder_id in folders:
                    folders[folder_id]["conversations"].append(conv_data)
            else:
                # Root level conversations (no folder)
                if "root_conversations" not in locals():
                    root_conversations = []
                root_conversations.append(conv_data)
        
        # Build final hierarchy - return the data directly, not wrapped
        return {
            "folders": root_folders,
            "root_conversations": root_conversations if "root_conversations" in locals() else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch folder hierarchy: {str(e)}")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, session: AsyncSession = Depends(get_session)):
    """Delete a conversation"""
    try:
        from sqlmodel import select
        from models import Conversation
        import uuid
        
        # Parse conversation ID
        try:
            conv_id = uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")
        
        # Find the conversation
        result = await session.execute(
            select(Conversation).where(Conversation.id == conv_id)
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Soft delete by setting is_active to False
        conversation.is_active = False
        await session.commit()
        
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")

# =========================
# Search Endpoints
# =========================

@router.get("/search/conversations")
async def search_conversations(
    q: Optional[str] = Query(None, description="Search query"),
    client_id: Optional[uuid.UUID] = Query(None, description="Filter by client ID"),
    project_id: Optional[uuid.UUID] = Query(None, description="Filter by project ID"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    start_date: Optional[str] = Query(None, description="Filter by start date"),
    end_date: Optional[str] = Query(None, description="Filter by end date"),
    search_method: str = Query("hybrid", description="Search method: hybrid, keyword, semantic, or basic"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Search conversations with advanced filters"""
    try:
        from sqlmodel import select, and_, or_, func
        from models import Conversation, ContentStatus, Project, Client, ConversationFolder, Message
        from datetime import datetime
        
        # Build the base query with joins
        query = select(Conversation).distinct()
        
        # Join with ContentStatus for project and status filtering
        query = query.outerjoin(ContentStatus, Conversation.id == ContentStatus.conversation_id)
        
        # Join with Project for client filtering
        query = query.outerjoin(Project, ContentStatus.project_id == Project.id)
        
        # Join with Client for client filtering
        query = query.outerjoin(Client, Project.client_id == Client.id)
        
        # Join with ConversationFolder for folder information
        query = query.outerjoin(ConversationFolder, Conversation.folder_id == ConversationFolder.id)
        
        # Apply filters
        conditions = [Conversation.is_active == True]  # Only active conversations
        
        # Date filters
        if start_date:
            try:
                # Handle both YYYY-MM-DD and ISO format
                if len(start_date) == 10:  # YYYY-MM-DD format
                    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                else:  # ISO format
                    start_dt = datetime.fromisoformat(start_date)
                conditions.append(Conversation.created_at >= start_dt)
            except ValueError:
                pass
        
        if end_date:
            try:
                # Handle both YYYY-MM-DD and ISO format
                if len(end_date) == 10:  # YYYY-MM-DD format
                    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                    # Add time to end of day for end_date
                    end_dt = end_dt.replace(hour=23, minute=59, second=59, microsecond=999999)
                else:  # ISO format
                    end_dt = datetime.fromisoformat(end_date)
                conditions.append(Conversation.created_at <= end_dt)
            except ValueError:
                pass
        
        # Client filter
        if client_id:
            conditions.append(Client.id == client_id)
        
        # Project filter
        if project_id:
            conditions.append(Project.id == project_id)
        
        # Content type filter
        if content_type:
            conditions.append(ContentStatus.content_type == content_type)
        
        # Status filter
        if status:
            conditions.append(ContentStatus.status == status)
        
        # Text search - use hybrid search if query provided and method is not basic
        if q and search_method != "basic":
            try:
                # Use hybrid search for content search
                embedding_service = EmbeddingService()
                hybrid_service = HybridSearchService(embedding_service)
                
                if search_method == "hybrid":
                    search_results = await hybrid_service.hybrid_search(
                        query=q,
                        limit=limit * 2,  # Get more results to filter
                        search_type="conversation"
                    )
                elif search_method == "keyword":
                    search_results = await hybrid_service.keyword_search(
                        query=q,
                        limit=limit * 2,
                        search_type="conversation"
                    )
                elif search_method == "semantic":
                    search_results = await hybrid_service.semantic_search(
                        query=q,
                        limit=limit * 2,
                        search_type="conversation"
                    )
                else:
                    raise HTTPException(status_code=400, detail="Invalid search_method")
                
                # Extract conversation IDs from search results
                conversation_ids = [result["conversation_id"] for result in search_results if "conversation_id" in result]
                
                if conversation_ids:
                    conditions.append(Conversation.id.in_(conversation_ids))
                else:
                    # No results found, return empty list
                    return []
                    
            except Exception as e:
                # Fall back to basic search if hybrid search fails
                logger.warning(f"Hybrid search failed, falling back to basic search: {e}")
                search_conditions = [
                    Conversation.title.contains(q),
                    ConversationFolder.name.contains(q),
                    Client.name.contains(q),
                    Project.name.contains(q)
                ]
                conditions.append(or_(*search_conditions))
        elif q:
            # Basic search fallback
            search_conditions = [
                Conversation.title.contains(q),
                ConversationFolder.name.contains(q),
                Client.name.contains(q),
                Project.name.contains(q)
            ]
            conditions.append(or_(*search_conditions))
        
        # Apply all conditions
        if conditions:
            query = query.where(and_(*conditions))
        
        # Order by updated_at desc
        query = query.order_by(Conversation.updated_at.desc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await session.execute(query)
        conversations = result.scalars().all()
        
        # Format the response with additional data
        formatted_conversations = []
        for conv in conversations:
            # Get additional data for this conversation
            content_status_result = await session.execute(
                select(ContentStatus, Project, Client)
                .outerjoin(Project, ContentStatus.project_id == Project.id)
                .outerjoin(Client, Project.client_id == Client.id)
                .where(ContentStatus.conversation_id == conv.id)
            )
            
            content_status_data = content_status_result.first()
            
            # Get folder data
            folder_result = await session.execute(
                select(ConversationFolder)
                .where(ConversationFolder.id == conv.folder_id)
            )
            folder = folder_result.scalar_one_or_none()
            
            # Get tags
            from sqlmodel import select
            tags_result = await session.execute(
                select(ContentTag)
                .join(ConversationTag, ContentTag.id == ConversationTag.tag_id)
                .where(ConversationTag.conversation_id == conv.id)
            )
            tags = tags_result.scalars().all()
            
            # Get message count for this conversation
            message_count_result = await session.execute(
                select(func.count(Message.id))
                .where(Message.conversation_id == conv.id)
            )
            message_count = message_count_result.scalar() or 0
            
            formatted_conv = {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "folder_id": str(conv.folder_id) if conv.folder_id else None,
                "folder_name": folder.name if folder else None,
                "client_id": (str(content_status_data[2].id) 
                             if content_status_data and content_status_data[2] else None),
                "client_name": (content_status_data[2].name 
                               if content_status_data and content_status_data[2] else None),
                "project_id": (str(content_status_data[1].id) 
                              if content_status_data and content_status_data[1] else None),
                "project_name": (content_status_data[1].name 
                                if content_status_data and content_status_data[1] else None),
                "status": (content_status_data[0].status 
                          if content_status_data and content_status_data[0] else None),
                "content_type": (content_status_data[0].content_type 
                                if content_status_data and content_status_data[0] else None),
                "message_count": message_count,
                "tags": [{"id": str(tag.id), "name": tag.name} for tag in tags]
            }
            formatted_conversations.append(formatted_conv)
        
        return formatted_conversations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


# =========================
# Hybrid Search Endpoints
# =========================

@router.get("/search/hybrid")
async def hybrid_search(
    q: str = Query(..., description="Search query"),
    search_type: str = Query("conversation", description="Search type: conversation or document"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    bm25_weight: float = Query(0.35, ge=0.0, le=1.0, description="Weight for BM25 scores"),
    cosine_weight: float = Query(0.65, ge=0.0, le=1.0, description="Weight for cosine similarity scores")
):
    """Perform hybrid search combining keyword and semantic search"""
    try:
        embedding_service = EmbeddingService()
        hybrid_service = HybridSearchService(embedding_service)
        
        results = await hybrid_service.hybrid_search(
            query=q,
            limit=limit,
            search_type=search_type,
            bm25_weight=bm25_weight,
            cosine_weight=cosine_weight
        )
        
        return {
            "query": q,
            "search_type": search_type,
            "results": results,
            "total_results": len(results),
            "weights": {
                "bm25": bm25_weight,
                "cosine": cosine_weight
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hybrid search failed: {str(e)}")


@router.get("/search/keyword")
async def keyword_search(
    q: str = Query(..., description="Search query"),
    search_type: str = Query("conversation", description="Search type: conversation or document"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results")
):
    """Perform keyword search using FTS5 with BM25 scoring"""
    try:
        embedding_service = EmbeddingService()
        hybrid_service = HybridSearchService(embedding_service)
        
        results = await hybrid_service.keyword_search(
            query=q,
            limit=limit,
            search_type=search_type
        )
        
        return {
            "query": q,
            "search_type": search_type,
            "search_method": "keyword",
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword search failed: {str(e)}")


@router.get("/search/semantic")
async def semantic_search(
    q: str = Query(..., description="Search query"),
    search_type: str = Query("conversation", description="Search type: conversation or document"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results")
):
    """Perform semantic search using FAISS with cosine similarity"""
    try:
        embedding_service = EmbeddingService()
        hybrid_service = HybridSearchService(embedding_service)
        
        results = await hybrid_service.semantic_search(
            query=q,
            limit=limit,
            search_type=search_type
        )
        
        return {
            "query": q,
            "search_type": search_type,
            "search_method": "semantic",
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {str(e)}")


@router.get("/search/documents")
async def search_documents(
    q: str = Query(..., description="Search query"),
    search_method: str = Query("hybrid", description="Search method: hybrid, keyword, or semantic"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results")
):
    """Search documents using the specified method"""
    try:
        embedding_service = EmbeddingService()
        hybrid_service = HybridSearchService(embedding_service)
        
        if search_method == "hybrid":
            results = await hybrid_service.hybrid_search(
                query=q,
                limit=limit,
                search_type="document"
            )
        elif search_method == "keyword":
            results = await hybrid_service.keyword_search(
                query=q,
                limit=limit,
                search_type="document"
            )
        elif search_method == "semantic":
            results = await hybrid_service.semantic_search(
                query=q,
                limit=limit,
                search_type="document"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid search_method. Must be 'hybrid', 'keyword', or 'semantic'")
        
        return {
            "query": q,
            "search_method": search_method,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document search failed: {str(e)}")


@router.post("/search/rebuild-index")
async def rebuild_search_index():
    """Rebuild the FAISS search index from all embeddings"""
    try:
        embedding_service = EmbeddingService()
        hybrid_service = HybridSearchService(embedding_service)
        
        await hybrid_service.build_faiss_index()
        
        return {
            "message": "Search index rebuilt successfully",
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Index rebuild failed: {str(e)}")
