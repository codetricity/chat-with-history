# =========================
# admin/views.py
# =========================
from typing import Any
from sqladmin import ModelView
from models import User, Conversation, Message


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