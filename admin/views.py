# =========================
# admin/views.py
# =========================
from typing import Any
from sqladmin import ModelView
from models import User, Conversation, Message, ContentStatus, Project, Client


class UserAdmin(ModelView, model=User):
    column_list = ["email", "is_active", "is_superuser", "is_staff", "group"]
    
    def is_accessible(self, request: Any) -> bool:
        """Only superusers can manage users"""
        return request.session.get("is_superuser", False)
    
    def is_visible(self, request: Any) -> bool:
        """Only show user management to superusers"""
        return request.session.get("is_superuser", False)


class ConversationAdmin(ModelView, model=Conversation):
    column_list = ["title", "user_id", "created_at", "updated_at", "is_active"]
    column_searchable_list = ["title"]
    column_sortable_list = ["created_at", "updated_at", "title"]
    
    def is_accessible(self, request: Any) -> bool:
        """Staff and superusers can manage conversations"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)
    
    def can_create(self, request: Any) -> bool:
        """Only superusers can create conversations"""
        return request.session.get("is_superuser", False)
    
    def can_delete(self, request: Any) -> bool:
        """Only superusers can delete conversations"""
        return request.session.get("is_superuser", False)


class MessageAdmin(ModelView, model=Message):
    column_list = ["conversation_id", "role", "content", "model", "token_count", "created_at"]
    column_searchable_list = ["content", "role"]
    column_sortable_list = ["created_at", "role"]
    can_create = False  # Messages are created through the chat interface
    can_edit = False    # Messages should not be edited
    can_delete = False  # Messages should not be deleted
    
    def is_accessible(self, request: Any) -> bool:
        """Staff and superusers can view messages"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)
    
    def is_visible(self, request: Any) -> bool:
        """Only show messages to staff and superusers"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)


class ContentStatusAdmin(ModelView, model=ContentStatus):
    column_list = ["conversation_id", "project_id", "status", "content_type", "assigned_to", "due_date", "created_at"]
    column_searchable_list = ["status", "content_type", "review_notes"]
    column_sortable_list = ["created_at", "updated_at", "status", "due_date"]
    column_details_list = [
        "id", "conversation_id", "project_id", "status", "content_type",
        "assigned_to", "review_notes", "due_date", "published_at",
        "created_at", "updated_at"
    ]

    # Form configuration
    form_columns = [
        "conversation_id", "project_id", "status", "content_type",
        "assigned_to", "review_notes", "due_date", "published_at"
    ]
    
    # Status choices for dropdown
    column_formatters = {
        "status": lambda m, a: m.status.title() if m.status else "Draft"
    }
    
    def is_accessible(self, request: Any) -> bool:
        """Staff and superusers can manage content status"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)
    
    def can_create(self, request: Any) -> bool:
        """Staff and superusers can create content status"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)
    
    def can_edit(self, request: Any) -> bool:
        """Staff and superusers can edit content status"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)
    
    def can_delete(self, request: Any) -> bool:
        """Only superusers can delete content status"""
        return request.session.get("is_superuser", False)


class ProjectAdmin(ModelView, model=Project):
    column_list = ["name", "client_id", "project_type", "status", "start_date", "end_date", "is_active"]
    column_searchable_list = ["name", "description", "project_type"]
    column_sortable_list = ["created_at", "updated_at", "name", "status"]
    
    def is_accessible(self, request: Any) -> bool:
        """Staff and superusers can manage projects"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)


class ClientAdmin(ModelView, model=Client):
    column_list = ["name", "company", "email", "industry", "is_active", "created_at"]
    column_searchable_list = ["name", "company", "email", "industry"]
    column_sortable_list = ["created_at", "updated_at", "name"]
    
    def is_accessible(self, request: Any) -> bool:
        """Staff and superusers can manage clients"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)