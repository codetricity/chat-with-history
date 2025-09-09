# =========================
# models.py
# =========================
import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)  # New field for staff permissions
    group: Optional[str] = Field(default=None)  # marketing, sales, support, etc.


class Product(SQLModel, table=True):
    __tablename__ = "products"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    price: float = Field(nullable=False)
    category: Optional[str] = Field(max_length=50, default=None, nullable=True)
    in_stock: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WebinarRegistrants(SQLModel, table=True):
    __tablename__ = "webinar_registrants"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    company: Optional[str] = Field(max_length=100, default=None, nullable=True)
    webinar_title: str = Field(max_length=200, nullable=False)
    webinar_date: datetime = Field(nullable=False)
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = Field(default="registered")  # registered, attended, cancelled, no_show
    assigned_sales_rep: Optional[str] = Field(default=None, nullable=True)
    group: Optional[str] = Field(default=None)  # marketing, sales, support
    is_public: bool = Field(default=True)  # Whether this registration is visible to all
    notes: Optional[str] = Field(default=None, nullable=True)
    photo_url: Optional[str] = Field(default=None, nullable=True)  # Path to uploaded photo
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConversationFolder(SQLModel, table=True):
    __tablename__ = "conversation_folders"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(foreign_key="users.id", nullable=True)  # Nullable for shared folders
    project_id: Optional[uuid.UUID] = Field(foreign_key="projects.id", nullable=True)  # Nullable for general folders
    name: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=500, nullable=True)
    parent_folder_id: Optional[uuid.UUID] = Field(foreign_key="conversation_folders.id", nullable=True)  # For sub-folders
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)  # For soft deletion


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(foreign_key="users.id", nullable=True)  # Nullable for anonymous chats
    folder_id: Optional[uuid.UUID] = Field(foreign_key="conversation_folders.id", nullable=True)  # Folder assignment
    title: Optional[str] = Field(default=None, max_length=200, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)  # For soft deletion


class Message(SQLModel, table=True):
    __tablename__ = "messages"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", nullable=False)
    role: str = Field(max_length=20, nullable=False)  # user, assistant, system
    content: str = Field(nullable=False)  # The actual message content
    raw_content: Optional[str] = Field(default=None, nullable=True)  # Raw content before formatting
    model: Optional[str] = Field(default=None, max_length=100, nullable=True)  # LLM model used
    token_count: Optional[int] = Field(default=None, nullable=True)  # Token count for cost tracking
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Chunk(SQLModel, table=True):
    __tablename__ = "chunks"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", nullable=False)
    content: str = Field(nullable=False)  # The actual chunk content
    chunk_index: int = Field(nullable=False)  # Order within conversation
    chunk_type: str = Field(default="message", max_length=20, nullable=False)  # message, response, system
    message_id: Optional[uuid.UUID] = Field(foreign_key="messages.id", nullable=True)  # Reference to original message
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChunkEmbedding(SQLModel, table=True):
    __tablename__ = "chunk_embeddings"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    chunk_id: uuid.UUID = Field(foreign_key="chunks.id", nullable=False)
    embedding: bytes = Field(nullable=False)  # float32 array as BLOB
    model_name: str = Field(max_length=100, nullable=False)  # e.g., "text-embedding-3-small"
    embedding_dimension: int = Field(nullable=False)  # e.g., 1536 for text-embedding-3-small
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Document(SQLModel, table=True):
    __tablename__ = "documents"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(foreign_key="users.id", nullable=True)
    folder_id: Optional[uuid.UUID] = Field(foreign_key="conversation_folders.id", nullable=True)
    title: str = Field(max_length=200, nullable=False)
    content: str = Field(nullable=False)  # Full document content
    file_type: Optional[str] = Field(max_length=50, nullable=True)  # pdf, txt, md, etc.
    file_path: Optional[str] = Field(max_length=500, nullable=True)  # Path to original file
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)


class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunks"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="documents.id", nullable=False)
    content: str = Field(nullable=False)
    chunk_index: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DocumentChunkEmbedding(SQLModel, table=True):
    __tablename__ = "document_chunk_embeddings"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    chunk_id: uuid.UUID = Field(foreign_key="document_chunks.id", nullable=False)
    embedding: bytes = Field(nullable=False)  # float32 array as BLOB
    model_name: str = Field(max_length=100, nullable=False)
    embedding_dimension: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SearchQuery(SQLModel, table=True):
    __tablename__ = "search_queries"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(foreign_key="users.id", nullable=True)
    query_text: str = Field(nullable=False)
    search_type: str = Field(max_length=20, nullable=False)  # keyword, semantic, hybrid
    results_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    action: str = Field(max_length=50)  # create, update, delete, view
    model_name: str = Field(max_length=50)  # products, webinar_registrants, users
    record_id: str = Field(max_length=50)
    changes: Optional[str] = Field(default=None, nullable=True)  # JSON of changes
    ip_address: Optional[str] = Field(default=None, nullable=True)
    user_agent: Optional[str] = Field(default=None, nullable=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# =========================
# Marketing Firm Models
# =========================

class Client(SQLModel, table=True):
    __tablename__ = "clients"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=200, nullable=False)
    company: Optional[str] = Field(max_length=200, nullable=True)
    email: Optional[str] = Field(max_length=255, nullable=True)
    phone: Optional[str] = Field(max_length=50, nullable=True)
    industry: Optional[str] = Field(max_length=100, nullable=True)
    notes: Optional[str] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Project(SQLModel, table=True):
    __tablename__ = "projects"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    client_id: uuid.UUID = Field(foreign_key="clients.id")
    name: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    project_type: str = Field(max_length=50, nullable=False)  # content_creation, research, strategy, etc.
    status: str = Field(max_length=20, default="active")  # active, completed, on_hold, cancelled
    start_date: Optional[datetime] = Field(default=None, nullable=True)
    end_date: Optional[datetime] = Field(default=None, nullable=True)
    budget: Optional[float] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContentTemplate(SQLModel, table=True):
    __tablename__ = "content_templates"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    content_type: str = Field(max_length=50, nullable=False)  # blog_post, social_media, email, ad_copy, etc.
    template_prompt: str = Field(nullable=False)  # The actual prompt template
    variables: Optional[str] = Field(default=None, nullable=True)  # JSON list of variable names
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContentStatus(SQLModel, table=True):
    __tablename__ = "content_status"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    project_id: Optional[uuid.UUID] = Field(foreign_key="projects.id", nullable=True)
    status: str = Field(max_length=20, default="draft")  # draft, review, approved, rejected, published
    content_type: str = Field(max_length=50, nullable=False)  # blog_post, social_media, email, etc.
    assigned_to: Optional[uuid.UUID] = Field(foreign_key="users.id", nullable=True)
    review_notes: Optional[str] = Field(default=None, nullable=True)
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    published_at: Optional[datetime] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContentTag(SQLModel, table=True):
    __tablename__ = "content_tags"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=100, nullable=False, unique=True)
    color: Optional[str] = Field(max_length=7, default="#3B82F6", nullable=True)  # Hex color
    description: Optional[str] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConversationTag(SQLModel, table=True):
    __tablename__ = "conversation_tags"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    tag_id: uuid.UUID = Field(foreign_key="content_tags.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# =========================
# Pydantic Models for API Requests/Responses
# =========================

# Client API Models
class ClientCreate(SQLModel):
    name: str = Field(max_length=200, nullable=False)
    company: Optional[str] = Field(max_length=200, nullable=True)
    email: Optional[str] = Field(max_length=255, nullable=True)
    phone: Optional[str] = Field(max_length=50, nullable=True)
    industry: Optional[str] = Field(max_length=100, nullable=True)
    notes: Optional[str] = Field(default=None, nullable=True)


class ClientUpdate(SQLModel):
    name: Optional[str] = Field(max_length=200, nullable=True)
    company: Optional[str] = Field(max_length=200, nullable=True)
    email: Optional[str] = Field(max_length=255, nullable=True)
    phone: Optional[str] = Field(max_length=50, nullable=True)
    industry: Optional[str] = Field(max_length=100, nullable=True)
    notes: Optional[str] = Field(default=None, nullable=True)
    is_active: Optional[bool] = None


# Project API Models
class ProjectCreate(SQLModel):
    client_id: uuid.UUID
    name: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    project_type: str = Field(max_length=50, nullable=False)
    status: Optional[str] = Field(max_length=20, default="active")
    start_date: Optional[datetime] = Field(default=None, nullable=True)
    end_date: Optional[datetime] = Field(default=None, nullable=True)
    budget: Optional[float] = Field(default=None, nullable=True)


class ProjectUpdate(SQLModel):
    name: Optional[str] = Field(max_length=200, nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)
    project_type: Optional[str] = Field(max_length=50, nullable=True)
    status: Optional[str] = Field(max_length=20, nullable=True)
    start_date: Optional[datetime] = Field(default=None, nullable=True)
    end_date: Optional[datetime] = Field(default=None, nullable=True)
    budget: Optional[float] = Field(default=None, nullable=True)
    is_active: Optional[bool] = None


# Content Template API Models
class ContentTemplateCreate(SQLModel):
    name: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    content_type: str = Field(max_length=50, nullable=False)
    template_prompt: str = Field(nullable=False)
    variables: Optional[str] = Field(default=None, nullable=True)


class ContentTemplateUpdate(SQLModel):
    name: Optional[str] = Field(max_length=200, nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)
    content_type: Optional[str] = Field(max_length=50, nullable=True)
    template_prompt: Optional[str] = Field(nullable=True)
    variables: Optional[str] = Field(default=None, nullable=True)
    is_active: Optional[bool] = None


# Content Status API Models
class ContentStatusCreate(SQLModel):
    conversation_id: uuid.UUID
    project_id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    status: str = Field(max_length=20, default="draft")
    content_type: str = Field(max_length=50, nullable=False)
    assigned_to: Optional[uuid.UUID] = Field(default=None, nullable=True)
    review_notes: Optional[str] = Field(default=None, nullable=True)
    due_date: Optional[datetime] = Field(default=None, nullable=True)


class ContentStatusUpdate(SQLModel):
    project_id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    status: Optional[str] = Field(max_length=20, nullable=True)
    content_type: Optional[str] = Field(max_length=50, nullable=True)
    assigned_to: Optional[uuid.UUID] = Field(default=None, nullable=True)
    review_notes: Optional[str] = Field(default=None, nullable=True)
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    published_at: Optional[datetime] = Field(default=None, nullable=True)


# Content Tag API Models
class ContentTagCreate(SQLModel):
    name: str = Field(max_length=100, nullable=False)
    color: Optional[str] = Field(max_length=7, default="#3B82F6", nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)


class ContentTagUpdate(SQLModel):
    name: Optional[str] = Field(max_length=100, nullable=True)
    color: Optional[str] = Field(max_length=7, nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)
    is_active: Optional[bool] = None

