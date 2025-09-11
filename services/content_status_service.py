"""
Service for managing content approval workflow
"""
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlmodel import select, Session
from models import ContentStatus, Conversation, Project, User, ContentStatusCreate, ContentStatusUpdate
from db import AsyncSessionLocal


class ContentStatusService:
    @staticmethod
    async def create_status(session: Session, status_data: ContentStatusCreate) -> ContentStatus:
        """Create a new content status entry or update existing one"""
        # Check if a ContentStatus already exists for this conversation
        existing_status = await session.execute(
            select(ContentStatus).where(ContentStatus.conversation_id == status_data.conversation_id)
        )
        existing_status = existing_status.scalar_one_or_none()
        
        if existing_status:
            # Update existing status instead of creating a new one
            update_data = status_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                if hasattr(existing_status, key):
                    setattr(existing_status, key, value)
            
            session.add(existing_status)
            await session.commit()
            await session.refresh(existing_status)
            return existing_status
        else:
            # Create new status
            content_status = ContentStatus(**status_data.dict())
            session.add(content_status)
            await session.commit()
            await session.refresh(content_status)
            return content_status

    @staticmethod
    async def get_statuses(session: Session, conversation_id: Optional[uuid.UUID] = None,
                          project_id: Optional[uuid.UUID] = None, status: Optional[str] = None,
                          skip: int = 0, limit: int = 100) -> List[ContentStatus]:
        """Get content statuses with optional filters"""
        query = select(ContentStatus).offset(skip).limit(limit)
        if conversation_id:
            query = query.where(ContentStatus.conversation_id == conversation_id)
        if project_id:
            query = query.where(ContentStatus.project_id == project_id)
        if status:
            query = query.where(ContentStatus.status == status)
        
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_status(session: Session, status_id: uuid.UUID) -> Optional[ContentStatus]:
        """Get a specific content status by ID"""
        return await session.get(ContentStatus, status_id)

    @staticmethod
    async def update_status(session: Session, status_id: uuid.UUID, status_data: ContentStatusUpdate) -> Optional[ContentStatus]:
        """Update content status"""
        content_status = await session.get(ContentStatus, status_id)
        if not content_status:
            return None
        
        update_data = status_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(content_status, key):
                setattr(content_status, key, value)
        
        session.add(content_status)
        await session.commit()
        await session.refresh(content_status)
        return content_status

    @staticmethod
    async def delete_status(session: Session, status_id: uuid.UUID) -> bool:
        """Delete a content status"""
        content_status = await session.get(ContentStatus, status_id)
        if not content_status:
            return False
        
        await session.delete(content_status)
        await session.commit()
        return True

    @staticmethod
    async def get_status_summary(session: Session) -> Dict[str, int]:
        """Get summary of content statuses for dashboard"""
        from sqlalchemy import func
        
        query = select(ContentStatus.status, func.count(ContentStatus.id).label('count')).group_by(ContentStatus.status)
        result = await session.execute(query)
        status_counts = {row[0]: row[1] for row in result.fetchall()}
        
        # Ensure all statuses are present with 0 count
        all_statuses = ['draft', 'review', 'approved', 'rejected', 'published']
        return {status: status_counts.get(status, 0) for status in all_statuses}

    @staticmethod
    async def create_content_status(conversation_id: uuid.UUID, content_type: str,
                                  project_id: Optional[uuid.UUID] = None,
                                  assigned_to: Optional[uuid.UUID] = None,
                                  due_date: Optional[datetime] = None) -> ContentStatus:
        """Create a new content status entry"""
        async with AsyncSessionLocal() as session:
            content_status = ContentStatus(
                conversation_id=conversation_id,
                project_id=project_id,
                content_type=content_type,
                assigned_to=assigned_to,
                due_date=due_date,
                status="draft"
            )
            session.add(content_status)
            await session.commit()
            await session.refresh(content_status)
            return content_status

    @staticmethod
    async def get_content_status(conversation_id: uuid.UUID, session: Optional[Session] = None) -> Optional[ContentStatus]:
        """Get content status for a conversation"""
        if session:
            query = select(ContentStatus).where(ContentStatus.conversation_id == conversation_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        else:
            async with AsyncSessionLocal() as new_session:
                query = select(ContentStatus).where(ContentStatus.conversation_id == conversation_id)
                result = await new_session.execute(query)
                return result.scalar_one_or_none()

    @staticmethod
    async def update_status_by_conversation(conversation_id: uuid.UUID, status: str,
                          review_notes: Optional[str] = None,
                          assigned_to: Optional[uuid.UUID] = None) -> bool:
        """Update content status by conversation ID"""
        async with AsyncSessionLocal() as session:
            content_status = await ContentStatusService.get_content_status(conversation_id, session)
            if not content_status:
                return False
            
            content_status.status = status
            if review_notes is not None:
                content_status.review_notes = review_notes
            if assigned_to is not None:
                content_status.assigned_to = assigned_to
            
            if status == "published":
                content_status.published_at = datetime.now(timezone.utc)
            
            session.add(content_status)
            await session.commit()
            return True

    @staticmethod
    async def get_content_by_status(status: str, project_id: Optional[uuid.UUID] = None,
                                  assigned_to: Optional[uuid.UUID] = None) -> List[Dict[str, Any]]:
        """Get content filtered by status, project, or assignee"""
        async with AsyncSessionLocal() as session:
            query = select(ContentStatus, Conversation, Project, User).join(
                Conversation, ContentStatus.conversation_id == Conversation.id
            ).outerjoin(Project, ContentStatus.project_id == Project.id).outerjoin(
                User, ContentStatus.assigned_to == User.id
            ).where(ContentStatus.status == status)
            
            if project_id:
                query = query.where(ContentStatus.project_id == project_id)
            if assigned_to:
                query = query.where(ContentStatus.assigned_to == assigned_to)
            
            result = await session.execute(query)
            rows = result.all()
            
            content_list = []
            for row in rows:
                content_status, conversation, project, user = row
                content_list.append({
                    "content_status": content_status,
                    "conversation": conversation,
                    "project": project,
                    "assigned_user": user
                })
            
            return content_list

    @staticmethod
    async def get_content_by_project(project_id: uuid.UUID) -> List[Dict[str, Any]]:
        """Get all content for a specific project"""
        async with AsyncSessionLocal() as session:
            query = select(ContentStatus, Conversation, User).join(
                Conversation, ContentStatus.conversation_id == Conversation.id
            ).outerjoin(User, ContentStatus.assigned_to == User.id).where(
                ContentStatus.project_id == project_id
            )
            
            result = await session.execute(query)
            rows = result.all()
            
            content_list = []
            for row in rows:
                content_status, conversation, user = row
                content_list.append({
                    "content_status": content_status,
                    "conversation": conversation,
                    "assigned_user": user
                })
            
            return content_list

    @staticmethod
    async def get_overdue_content() -> List[Dict[str, Any]]:
        """Get content that is overdue"""
        async with AsyncSessionLocal() as session:
            now = datetime.now(timezone.utc)
            query = select(ContentStatus, Conversation, Project, User).join(
                Conversation, ContentStatus.conversation_id == Conversation.id
            ).outerjoin(Project, ContentStatus.project_id == Project.id).outerjoin(
                User, ContentStatus.assigned_to == User.id
            ).where(
                ContentStatus.due_date < now,
                ContentStatus.status.in_(["draft", "review"])
            )
            
            result = await session.execute(query)
            rows = result.all()
            
            content_list = []
            for row in rows:
                content_status, conversation, project, user = row
                content_list.append({
                    "content_status": content_status,
                    "conversation": conversation,
                    "project": project,
                    "assigned_user": user
                })
            
            return content_list

