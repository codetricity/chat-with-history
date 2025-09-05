"""
Chat History Service for managing conversation persistence and retrieval
"""
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple
from sqlmodel import select, and_
from models import Conversation, Message, User
from db import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)


class ChatHistoryService:
    """Service for managing chat conversation history"""

    @staticmethod
    async def create_conversation(
        user_id: Optional[uuid.UUID] = None,
        title: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation
        
        Args:
            user_id: Optional user ID for authenticated users
            title: Optional conversation title
            
        Returns:
            Conversation: The created conversation
        """
        async with AsyncSessionLocal() as session:
            conversation = Conversation(
                user_id=user_id,
                title=title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            logger.info(f"Created conversation {conversation.id} for user {user_id}")
            return conversation

    @staticmethod
    async def get_conversation(conversation_id: uuid.UUID) -> Optional[Conversation]:
        """
        Get a conversation by ID
        
        Args:
            conversation_id: The conversation UUID
            
        Returns:
            Conversation or None if not found
        """
        async with AsyncSessionLocal() as session:
            statement = select(Conversation).where(
                and_(
                    Conversation.id == conversation_id,
                    Conversation.is_active == True
                )
            )
            result = await session.execute(statement)
            conversation = result.scalar_one_or_none()
            return conversation

    @staticmethod
    async def get_user_conversations(
        user_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[Conversation]:
        """
        Get conversations for a specific user
        
        Args:
            user_id: The user UUID
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip
            
        Returns:
            List of conversations ordered by updated_at desc
        """
        async with AsyncSessionLocal() as session:
            statement = (
                select(Conversation)
                .where(
                    and_(
                        Conversation.user_id == user_id,
                        Conversation.is_active == True
                    )
                )
                .order_by(Conversation.updated_at.desc())
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(statement)
            conversations = result.scalars().all()
            return list(conversations)

    @staticmethod
    async def add_message(
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        raw_content: Optional[str] = None,
        model: Optional[str] = None,
        token_count: Optional[int] = None
    ) -> Message:
        """
        Add a message to a conversation
        
        Args:
            conversation_id: The conversation UUID
            role: Message role (user, assistant, system)
            content: The message content
            raw_content: Raw content before formatting
            model: LLM model used
            token_count: Token count for cost tracking
            
        Returns:
            Message: The created message
        """
        async with AsyncSessionLocal() as session:
            # Verify conversation exists and is active
            conversation = await ChatHistoryService.get_conversation(conversation_id)
            if not conversation:
                raise ValueError(f"Conversation {conversation_id} not found or inactive")
            
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                raw_content=raw_content,
                model=model,
                token_count=token_count
            )
            session.add(message)
            
            # Update conversation's updated_at timestamp
            conversation.updated_at = datetime.now(timezone.utc)
            session.add(conversation)
            
            await session.commit()
            await session.refresh(message)
            logger.info(f"Added {role} message to conversation {conversation_id}")
            return message

    @staticmethod
    async def get_conversation_messages(
        conversation_id: uuid.UUID,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Message]:
        """
        Get messages for a conversation
        
        Args:
            conversation_id: The conversation UUID
            limit: Maximum number of messages to return (None for all)
            offset: Number of messages to skip
            
        Returns:
            List of messages ordered by created_at asc
        """
        async with AsyncSessionLocal() as session:
            statement = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.asc())
            )
            
            if limit:
                statement = statement.offset(offset).limit(limit)
            elif offset:
                statement = statement.offset(offset)
            
            result = await session.execute(statement)
            messages = result.scalars().all()
            return list(messages)

    @staticmethod
    async def get_recent_messages(
        conversation_id: uuid.UUID,
        count: int = 10
    ) -> List[Message]:
        """
        Get the most recent messages from a conversation for context
        
        Args:
            conversation_id: The conversation UUID
            count: Number of recent messages to return
            
        Returns:
            List of recent messages ordered by created_at desc
        """
        async with AsyncSessionLocal() as session:
            statement = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(count)
            )
            result = await session.execute(statement)
            messages = result.scalars().all()
            # Return in chronological order (oldest first)
            return list(reversed(messages))

    @staticmethod
    async def get_conversation_context(
        conversation_id: uuid.UUID,
        max_messages: int = 20
    ) -> List[Dict[str, str]]:
        """
        Get conversation context formatted for LLM consumption
        
        Args:
            conversation_id: The conversation UUID
            max_messages: Maximum number of messages to include in context
            
        Returns:
            List of message dictionaries with 'role' and 'content' keys
        """
        messages = await ChatHistoryService.get_recent_messages(
            conversation_id, max_messages
        )
        
        context = []
        for message in messages:
            context.append({
                "role": message.role,
                "content": message.content
            })
        
        return context

    @staticmethod
    async def update_conversation_title(
        conversation_id: uuid.UUID,
        title: str
    ) -> bool:
        """
        Update conversation title
        
        Args:
            conversation_id: The conversation UUID
            title: New title
            
        Returns:
            bool: True if updated successfully
        """
        async with AsyncSessionLocal() as session:
            conversation = await ChatHistoryService.get_conversation(conversation_id)
            if not conversation:
                return False
            
            conversation.title = title
            conversation.updated_at = datetime.now(timezone.utc)
            session.add(conversation)
            await session.commit()
            logger.info(f"Updated conversation {conversation_id} title to: {title}")
            return True

    @staticmethod
    async def archive_conversation(conversation_id: uuid.UUID) -> bool:
        """
        Archive (soft delete) a conversation
        
        Args:
            conversation_id: The conversation UUID
            
        Returns:
            bool: True if archived successfully
        """
        async with AsyncSessionLocal() as session:
            conversation = await ChatHistoryService.get_conversation(conversation_id)
            if not conversation:
                return False
            
            conversation.is_active = False
            conversation.updated_at = datetime.now(timezone.utc)
            session.add(conversation)
            await session.commit()
            logger.info(f"Archived conversation {conversation_id}")
            return True

    @staticmethod
    async def get_conversation_stats(conversation_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get conversation statistics
        
        Args:
            conversation_id: The conversation UUID
            
        Returns:
            Dictionary with conversation statistics
        """
        async with AsyncSessionLocal() as session:
            # Get message count
            message_count_statement = select(Message).where(
                Message.conversation_id == conversation_id
            )
            result = await session.execute(message_count_statement)
            messages = result.scalars().all()
            message_count = len(messages)
            
            # Get total token count
            total_tokens = sum(msg.token_count or 0 for msg in messages)
            
            # Get conversation info
            conversation = await ChatHistoryService.get_conversation(conversation_id)
            if not conversation:
                return {}
            
            return {
                "conversation_id": str(conversation_id),
                "title": conversation.title,
                "message_count": message_count,
                "total_tokens": total_tokens,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "is_active": conversation.is_active
            }
