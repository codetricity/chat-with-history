"""
Service for managing content tags
"""
import uuid
from typing import List, Optional
from sqlmodel import select, Session
from models import ContentTag, ConversationTag, Conversation, ContentTagCreate, ContentTagUpdate


class ContentTagService:
    @staticmethod
    async def create_tag(session: Session, tag_data: ContentTagCreate) -> ContentTag:
        """Create a new content tag"""
        tag = ContentTag(**tag_data.dict())
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag

    @staticmethod
    async def get_tags(session: Session, skip: int = 0, limit: int = 100) -> List[ContentTag]:
        """Get all content tags"""
        query = select(ContentTag).where(ContentTag.is_active == True).offset(skip).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_tag(session: Session, tag_id: uuid.UUID) -> Optional[ContentTag]:
        """Get a specific tag by ID"""
        return await session.get(ContentTag, tag_id)

    @staticmethod
    async def update_tag(session: Session, tag_id: uuid.UUID, tag_data: ContentTagUpdate) -> Optional[ContentTag]:
        """Update a content tag"""
        tag = await session.get(ContentTag, tag_id)
        if not tag or not tag.is_active:
            return None
        
        update_data = tag_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(tag, key):
                setattr(tag, key, value)
        
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag

    @staticmethod
    async def delete_tag(session: Session, tag_id: uuid.UUID) -> bool:
        """Soft delete a content tag"""
        tag = await session.get(ContentTag, tag_id)
        if not tag or not tag.is_active:
            return False
        
        tag.is_active = False
        session.add(tag)
        await session.commit()
        return True

    @staticmethod
    async def add_tag_to_conversation(session: Session, conversation_id: uuid.UUID, tag_id: uuid.UUID) -> bool:
        """Add a tag to a conversation"""
        # Check if tag already exists for this conversation
        existing = await session.execute(
            select(ConversationTag).where(
                ConversationTag.conversation_id == conversation_id,
                ConversationTag.tag_id == tag_id
            )
        )
        if existing.scalar_one_or_none():
            return False  # Already exists
        
        conversation_tag = ConversationTag(
            conversation_id=conversation_id,
            tag_id=tag_id
        )
        session.add(conversation_tag)
        await session.commit()
        return True

    @staticmethod
    async def remove_tag_from_conversation(session: Session, conversation_id: uuid.UUID, tag_id: uuid.UUID) -> bool:
        """Remove a tag from a conversation"""
        result = await session.execute(
            select(ConversationTag).where(
                ConversationTag.conversation_id == conversation_id,
                ConversationTag.tag_id == tag_id
            )
        )
        conversation_tag = result.scalar_one_or_none()
        if not conversation_tag:
            return False
        
        await session.delete(conversation_tag)
        await session.commit()
        return True

    @staticmethod
    async def get_conversation_tags(session: Session, conversation_id: uuid.UUID) -> List[ContentTag]:
        """Get all tags for a conversation"""
        query = select(ContentTag).join(ConversationTag).where(
            ConversationTag.conversation_id == conversation_id,
            ContentTag.is_active == True
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_tags_legacy(active_only: bool = True) -> List[ContentTag]:
        """Get all content tags (legacy method)"""
        async with AsyncSessionLocal() as session:
            query = select(ContentTag)
            if active_only:
                query = query.where(ContentTag.is_active == True)
            
            result = await session.execute(query)
            tags = result.scalars().all()
            return list(tags)

    @staticmethod
    async def get_tag(tag_id: uuid.UUID) -> Optional[ContentTag]:
        """Get a specific tag by ID"""
        async with AsyncSessionLocal() as session:
            tag = await session.get(ContentTag, tag_id)
            return tag if tag and tag.is_active else None

    @staticmethod
    async def update_tag(tag_id: uuid.UUID, **kwargs) -> bool:
        """Update tag information"""
        async with AsyncSessionLocal() as session:
            tag = await session.get(ContentTag, tag_id)
            if not tag or not tag.is_active:
                return False
            
            for key, value in kwargs.items():
                if hasattr(tag, key) and value is not None:
                    setattr(tag, key, value)
            
            session.add(tag)
            await session.commit()
            return True

    @staticmethod
    async def delete_tag(tag_id: uuid.UUID) -> bool:
        """Soft delete a tag"""
        async with AsyncSessionLocal() as session:
            tag = await session.get(ContentTag, tag_id)
            if not tag or not tag.is_active:
                return False
            
            tag.is_active = False
            session.add(tag)
            await session.commit()
            return True

    @staticmethod
    async def add_tag_to_conversation(conversation_id: uuid.UUID, tag_id: uuid.UUID) -> bool:
        """Add a tag to a conversation"""
        async with AsyncSessionLocal() as session:
            # Check if tag already exists for this conversation
            existing_query = select(ConversationTag).where(
                ConversationTag.conversation_id == conversation_id,
                ConversationTag.tag_id == tag_id
            )
            result = await session.execute(existing_query)
            if result.scalar_one_or_none():
                return True  # Tag already exists
            
            conversation_tag = ConversationTag(
                conversation_id=conversation_id,
                tag_id=tag_id
            )
            session.add(conversation_tag)
            await session.commit()
            return True

    @staticmethod
    async def remove_tag_from_conversation(conversation_id: uuid.UUID, tag_id: uuid.UUID) -> bool:
        """Remove a tag from a conversation"""
        async with AsyncSessionLocal() as session:
            query = select(ConversationTag).where(
                ConversationTag.conversation_id == conversation_id,
                ConversationTag.tag_id == tag_id
            )
            result = await session.execute(query)
            conversation_tag = result.scalar_one_or_none()
            
            if conversation_tag:
                await session.delete(conversation_tag)
                await session.commit()
                return True
            return False

    @staticmethod
    async def get_conversation_tags(conversation_id: uuid.UUID) -> List[ContentTag]:
        """Get all tags for a conversation"""
        async with AsyncSessionLocal() as session:
            query = select(ContentTag).join(ConversationTag).where(
                ConversationTag.conversation_id == conversation_id,
                ContentTag.is_active == True
            )
            
            result = await session.execute(query)
            tags = result.scalars().all()
            return list(tags)

    @staticmethod
    async def get_conversations_by_tag(tag_id: uuid.UUID) -> List[Conversation]:
        """Get all conversations with a specific tag"""
        async with AsyncSessionLocal() as session:
            query = select(Conversation).join(ConversationTag).where(
                ConversationTag.tag_id == tag_id,
                Conversation.is_active == True
            )
            
            result = await session.execute(query)
            conversations = result.scalars().all()
            return list(conversations)

    @staticmethod
    async def get_tag_usage_stats() -> List[dict]:
        """Get usage statistics for all tags"""
        async with AsyncSessionLocal() as session:
            query = select(
                ContentTag.id,
                ContentTag.name,
                ContentTag.color,
                ContentTag.description,
                ConversationTag.id
            ).outerjoin(ConversationTag).where(ContentTag.is_active == True)
            
            result = await session.execute(query)
            rows = result.all()
            
            tag_stats = {}
            for row in rows:
                tag_id, name, color, description, conversation_tag_id = row
                if tag_id not in tag_stats:
                    tag_stats[tag_id] = {
                        "id": tag_id,
                        "name": name,
                        "color": color,
                        "description": description,
                        "usage_count": 0
                    }
                if conversation_tag_id:
                    tag_stats[tag_id]["usage_count"] += 1
            
            return list(tag_stats.values())
