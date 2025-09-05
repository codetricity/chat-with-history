"""
Service for managing clients and projects
"""
import uuid
from typing import List, Optional
from sqlmodel import select, Session
from models import Client, Project, ClientCreate, ClientUpdate, ProjectCreate, ProjectUpdate


class ClientService:
    @staticmethod
    async def create_client(session: Session, client_data: ClientCreate) -> Client:
        """Create a new client"""
        client = Client(**client_data.dict())
        session.add(client)
        await session.commit()
        await session.refresh(client)
        return client

    @staticmethod
    async def get_clients(session: Session, skip: int = 0, limit: int = 100) -> List[Client]:
        """Get all clients"""
        query = select(Client).where(Client.is_active == True).offset(skip).limit(limit)
        result = await session.execute(query)
        clients = result.scalars().all()
        return list(clients)

    @staticmethod
    async def get_client(session: Session, client_id: uuid.UUID) -> Optional[Client]:
        """Get a specific client by ID"""
        client = await session.get(Client, client_id)
        return client if client and client.is_active else None

    @staticmethod
    async def update_client(session: Session, client_id: uuid.UUID, client_data: ClientUpdate) -> Optional[Client]:
        """Update client information"""
        client = await session.get(Client, client_id)
        if not client or not client.is_active:
            return None
        
        update_data = client_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(client, key):
                setattr(client, key, value)
        
        session.add(client)
        await session.commit()
        await session.refresh(client)
        return client

    @staticmethod
    async def delete_client(session: Session, client_id: uuid.UUID) -> bool:
        """Soft delete a client"""
        client = await session.get(Client, client_id)
        if not client or not client.is_active:
            return False
        
        client.is_active = False
        session.add(client)
        await session.commit()
        return True

    @staticmethod
    async def create_project(session: Session, project_data: ProjectCreate) -> Project:
        """Create a new project for a client"""
        project = Project(**project_data.dict())
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

    @staticmethod
    async def get_projects(session: Session, client_id: Optional[uuid.UUID] = None, 
                          skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects, optionally filtered by client"""
        query = select(Project).where(Project.is_active == True).offset(skip).limit(limit)
        if client_id:
            query = query.where(Project.client_id == client_id)
        
        result = await session.execute(query)
        projects = result.scalars().all()
        return list(projects)

    @staticmethod
    async def get_project(session: Session, project_id: uuid.UUID) -> Optional[Project]:
        """Get a specific project by ID"""
        project = await session.get(Project, project_id)
        return project if project and project.is_active else None

    @staticmethod
    async def update_project(session: Session, project_id: uuid.UUID, project_data: ProjectUpdate) -> Optional[Project]:
        """Update project information"""
        project = await session.get(Project, project_id)
        if not project or not project.is_active:
            return None
        
        update_data = project_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(project, key):
                setattr(project, key, value)
        
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

    @staticmethod
    async def delete_project(session: Session, project_id: uuid.UUID) -> bool:
        """Soft delete a project"""
        project = await session.get(Project, project_id)
        if not project or not project.is_active:
            return False
        
        project.is_active = False
        session.add(project)
        await session.commit()
        return True
