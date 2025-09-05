"""
Marketing firm API routes for client management, projects, content templates, and status tracking
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime, timezone

from db import get_session
from models import (
    Client, Project, ContentTemplate, ContentStatus, ContentTag, ConversationTag,
    ClientCreate, ClientUpdate, ProjectCreate, ProjectUpdate, 
    ContentTemplateCreate, ContentTemplateUpdate, ContentStatusCreate, ContentStatusUpdate,
    ContentTagCreate, ContentTagUpdate
)
from services.client_service import ClientService
from services.content_template_service import ContentTemplateService
from services.content_status_service import ContentStatusService
from services.content_tag_service import ContentTagService

router = APIRouter(prefix="/api", tags=["marketing"])

# Initialize services
client_service = ClientService()
template_service = ContentTemplateService()
status_service = ContentStatusService()
tag_service = ContentTagService()


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
async def get_conversations(session: Session = Depends(get_session)):
    """Get all conversations"""
    try:
        # For now, return empty list since we don't have conversations yet
        # In a real implementation, this would query the database
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversations: {str(e)}")

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
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Search conversations with advanced filters"""
    try:
        from sqlmodel import select, and_, or_
        from models import Conversation, ContentStatus
        from datetime import datetime
        
        # Build the base query
        query = select(Conversation)
        
        # Apply filters
        conditions = []
        
        # For now, let's keep it simple and only support basic text search and date filters
        # More complex joins can be added later when we have proper relationships
        
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date)
                conditions.append(Conversation.created_at >= start_dt)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date)
                conditions.append(Conversation.created_at <= end_dt)
            except ValueError:
                pass
        
        # Apply text search if query provided
        if q:
            search_conditions = [
                Conversation.title.contains(q)
            ]
            conditions.append(or_(*search_conditions))
        
        # Apply all conditions
        if conditions:
            query = query.where(and_(*conditions))
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await session.execute(query)
        conversations = result.scalars().all()
        
        return list(conversations)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
