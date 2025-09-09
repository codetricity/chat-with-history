"""
Service for managing conversation folders
"""
import uuid
from typing import List, Optional
from sqlmodel import select, func
from models import ConversationFolder, Conversation, Message
from db import AsyncSessionLocal


class FolderService:
    @staticmethod
    async def create_folder(name: str, description: Optional[str] = None, 
                          parent_folder_id: Optional[uuid.UUID] = None, 
                          user_id: Optional[uuid.UUID] = None,
                          project_id: Optional[uuid.UUID] = None) -> ConversationFolder:
        """Create a new conversation folder"""
        async with AsyncSessionLocal() as session:
            folder = ConversationFolder(
                name=name,
                description=description,
                parent_folder_id=parent_folder_id,
                user_id=user_id,
                project_id=project_id
            )
            session.add(folder)
            await session.commit()
            await session.refresh(folder)
            return folder

    @staticmethod
    async def get_folders(user_id: Optional[uuid.UUID] = None, 
                         parent_folder_id: Optional[uuid.UUID] = None,
                         project_id: Optional[uuid.UUID] = None) -> List[ConversationFolder]:
        """Get folders for a user, optionally filtered by parent folder or project"""
        async with AsyncSessionLocal() as session:
            query = select(ConversationFolder).where(ConversationFolder.is_active == True)
            
            if user_id is not None:
                query = query.where(ConversationFolder.user_id == user_id)
            
            if project_id is not None:
                query = query.where(ConversationFolder.project_id == project_id)
            
            if parent_folder_id is not None:
                query = query.where(ConversationFolder.parent_folder_id == parent_folder_id)
            else:
                # If no parent_folder_id specified, get root level folders
                query = query.where(ConversationFolder.parent_folder_id.is_(None))
            
            result = await session.execute(query)
            folders = result.scalars().all()
            return list(folders)

    @staticmethod
    async def get_folder(folder_id: uuid.UUID) -> Optional[ConversationFolder]:
        """Get a specific folder by ID"""
        async with AsyncSessionLocal() as session:
            folder = await session.get(ConversationFolder, folder_id)
            return folder if folder and folder.is_active else None

    @staticmethod
    async def update_folder(folder_id: uuid.UUID, name: Optional[str] = None, 
                          description: Optional[str] = None, project_id: Optional[uuid.UUID] = None) -> bool:
        """Update folder name, description, and/or project_id"""
        async with AsyncSessionLocal() as session:
            folder = await session.get(ConversationFolder, folder_id)
            if not folder or not folder.is_active:
                return False
            
            if name is not None:
                folder.name = name
            if description is not None:
                folder.description = description
            if project_id is not None:
                folder.project_id = project_id
            
            session.add(folder)
            await session.commit()
            return True

    @staticmethod
    async def delete_folder(folder_id: uuid.UUID) -> bool:
        """Soft delete a folder (and move its conversations to parent or root)"""
        async with AsyncSessionLocal() as session:
            folder = await session.get(ConversationFolder, folder_id)
            if not folder or not folder.is_active:
                return False
            
            # Move conversations in this folder to the parent folder or root
            conversations_query = select(Conversation).where(
                Conversation.folder_id == folder_id,
                Conversation.is_active == True
            )
            result = await session.execute(conversations_query)
            conversations = result.scalars().all()
            
            for conversation in conversations:
                conversation.folder_id = folder.parent_folder_id
                session.add(conversation)
            
            # Move sub-folders to the parent folder or root
            sub_folders_query = select(ConversationFolder).where(
                ConversationFolder.parent_folder_id == folder_id,
                ConversationFolder.is_active == True
            )
            result = await session.execute(sub_folders_query)
            sub_folders = result.scalars().all()
            
            for sub_folder in sub_folders:
                sub_folder.parent_folder_id = folder.parent_folder_id
                session.add(sub_folder)
            
            # Soft delete the folder
            folder.is_active = False
            session.add(folder)
            await session.commit()
            return True

    @staticmethod
    async def move_conversation_to_folder(conversation_id: uuid.UUID, 
                                        folder_id: Optional[uuid.UUID] = None) -> bool:
        """Move a conversation to a folder (or to root if folder_id is None)"""
        async with AsyncSessionLocal() as session:
            conversation = await session.get(Conversation, conversation_id)
            if not conversation or not conversation.is_active:
                return False
            
            # If folder_id is provided, verify the folder exists
            if folder_id is not None:
                folder = await session.get(ConversationFolder, folder_id)
                if not folder or not folder.is_active:
                    return False
            
            conversation.folder_id = folder_id
            session.add(conversation)
            await session.commit()
            return True

    @staticmethod
    async def get_conversations_in_folder(folder_id: Optional[uuid.UUID] = None, 
                                        user_id: Optional[uuid.UUID] = None) -> List[Conversation]:
        """Get conversations in a specific folder (or root if folder_id is None)"""
        async with AsyncSessionLocal() as session:
            query = select(Conversation).where(Conversation.is_active == True)
            
            if folder_id is not None:
                query = query.where(Conversation.folder_id == folder_id)
            else:
                # Get conversations not in any folder (root level)
                query = query.where(Conversation.folder_id.is_(None))
            
            if user_id is not None:
                query = query.where(Conversation.user_id == user_id)
            
            result = await session.execute(query)
            conversations = result.scalars().all()
            return list(conversations)

    @staticmethod
    async def get_folder_hierarchy(user_id: Optional[uuid.UUID] = None) -> List[dict]:
        """Get the complete folder hierarchy with conversations"""
        async with AsyncSessionLocal() as session:
            # Get all folders for the user
            folders_query = select(ConversationFolder).where(
                ConversationFolder.is_active == True
            )
            if user_id is not None:
                folders_query = folders_query.where(ConversationFolder.user_id == user_id)
            
            result = await session.execute(folders_query)
            folders = result.scalars().all()
            folder_dict = {folder.id: folder for folder in folders}
            
            # Get all conversations
            conversations_query = select(Conversation).where(Conversation.is_active == True)
            if user_id is not None:
                conversations_query = conversations_query.where(Conversation.user_id == user_id)
            
            result = await session.execute(conversations_query)
            conversations = result.scalars().all()
            
            # Build hierarchy
            hierarchy = []
            root_folders = [f for f in folders if f.parent_folder_id is None]
            root_conversations = [c for c in conversations if c.folder_id is None]
            
            # Add root conversations
            for conv in root_conversations:
                # Get message count for this conversation
                message_count_result = await session.execute(
                    select(func.count(Message.id))
                    .where(Message.conversation_id == conv.id)
                )
                message_count = message_count_result.scalar() or 0
                
                # Get client and project information
                from models import ContentStatus, Project, Client
                content_status_result = await session.execute(
                    select(ContentStatus, Project, Client)
                    .outerjoin(Project, ContentStatus.project_id == Project.id)
                    .outerjoin(Client, Project.client_id == Client.id)
                    .where(ContentStatus.conversation_id == conv.id)
                )
                content_status_data = content_status_result.first()
                
                hierarchy.append({
                    "type": "conversation",
                    "id": str(conv.id),
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat(),
                    "message_count": message_count,
                    "client_id": str(content_status_data[2].id) if content_status_data and content_status_data[2] else None,
                    "client_name": content_status_data[2].name if content_status_data and content_status_data[2] else None,
                    "project_id": str(content_status_data[1].id) if content_status_data and content_status_data[1] else None,
                    "project_name": content_status_data[1].name if content_status_data and content_status_data[1] else None,
                    "status": content_status_data[0].status if content_status_data and content_status_data[0] else None,
                    "content_type": content_status_data[0].content_type if content_status_data and content_status_data[0] else None
                })
            
            # Add root folders and their children
            for folder in root_folders:
                hierarchy.append(await FolderService._build_folder_tree(folder, folder_dict, conversations, session))
            
            return hierarchy

    @staticmethod
    async def _build_folder_tree(folder: ConversationFolder, 
                                folder_dict: dict, 
                                all_conversations: List[Conversation],
                                session) -> dict:
        """Recursively build folder tree structure"""
        # Get conversations in this folder
        folder_conversations = [c for c in all_conversations if c.folder_id == folder.id]
        
        # Get sub-folders
        sub_folders = [f for f in folder_dict.values() if f.parent_folder_id == folder.id]
        
        # Build conversations list
        conversations = []
        for conv in folder_conversations:
            # Get message count for this conversation
            message_count_result = await session.execute(
                select(func.count(Message.id))
                .where(Message.conversation_id == conv.id)
            )
            message_count = message_count_result.scalar() or 0
            
            # Get client and project information
            from models import ContentStatus, Project, Client
            content_status_result = await session.execute(
                select(ContentStatus, Project, Client)
                .outerjoin(Project, ContentStatus.project_id == Project.id)
                .outerjoin(Client, Project.client_id == Client.id)
                .where(ContentStatus.conversation_id == conv.id)
            )
            content_status_data = content_status_result.first()
            
            conversations.append({
                "type": "conversation",
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "message_count": message_count,
                "client_id": str(content_status_data[2].id) if content_status_data and content_status_data[2] else None,
                "client_name": content_status_data[2].name if content_status_data and content_status_data[2] else None,
                "project_id": str(content_status_data[1].id) if content_status_data and content_status_data[1] else None,
                "project_name": content_status_data[1].name if content_status_data and content_status_data[1] else None,
                "status": content_status_data[0].status if content_status_data and content_status_data[0] else None,
                "content_type": content_status_data[0].content_type if content_status_data and content_status_data[0] else None
            })
        
        # Build sub-folders list
        children = []
        for sub_folder in sub_folders:
            children.append(await FolderService._build_folder_tree(sub_folder, folder_dict, all_conversations, session))
        
        return {
            "type": "folder",
            "id": str(folder.id),
            "name": folder.name,
            "description": folder.description,
            "project_id": str(folder.project_id) if folder.project_id else None,
            "created_at": folder.created_at.isoformat(),
            "updated_at": folder.updated_at.isoformat(),
            "conversations": conversations,
            "children": children
        }