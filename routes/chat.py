"""
Chat routes for AI chat functionality
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from services.chat_service import ChatService
from services.chat_history_service import ChatHistoryService
from services.folder_service import FolderService
from services.web_search_service import WebSearchService
import json
import uuid
from typing import Optional

router = APIRouter()


@router.get("/api/chat/test")
async def test_chat_connection():
    """Test endpoint to check OpenRouter API connection"""
    try:
        result = await ChatService.test_connection()
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Test failed: {str(e)}"}
        )


@router.get("/api/chat/web-search/test")
async def test_web_search_connection():
    """Test endpoint to check Tavily API connection"""
    try:
        web_search_service = WebSearchService()
        result = await web_search_service.test_connection()
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Web search test failed: {str(e)}"}
        )


@router.post("/api/chat/web-search")
async def test_web_search(request: Request):
    """Test endpoint to perform a web search"""
    try:
        body = await request.json()
        query = body.get("query", "")
        
        if not query:
            return JSONResponse(
                status_code=400,
                content={"error": "Query is required"}
            )
        
        web_search_service = WebSearchService()
        result = await web_search_service.search(query)
        return JSONResponse(content=result)
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Web search failed: {str(e)}"}
        )


@router.post("/api/chat")
async def chat_with_llama(request: Request):
    """Chat endpoint using OpenRouter API with Llama 3.3 70B (non-streaming)"""
    try:
        # Get the request body
        body = await request.json()
        user_message = body.get("message", "")
        conversation_id = body.get("conversation_id")
        user_id = body.get("user_id")
        
        if not user_message:
            return JSONResponse(
                status_code=400,
                content={"error": "Message is required"}
            )
        
        # Parse conversation_id if provided
        parsed_conversation_id = None
        if conversation_id:
            try:
                parsed_conversation_id = uuid.UUID(conversation_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid conversation_id format"}
                )
        
        # Parse user_id if provided
        parsed_user_id = None
        if user_id:
            try:
                parsed_user_id = uuid.UUID(user_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid user_id format"}
                )
        
        # Use service to handle chat with conversation context
        response = await ChatService.chat_with_llama(
            user_message, 
            conversation_id=parsed_conversation_id,
            user_id=parsed_user_id
        )
        return JSONResponse(content=response)
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.post("/api/chat/stream")
async def chat_with_llama_stream(request: Request):
    """Streaming chat endpoint using OpenRouter API with Llama 3.3 70B"""
    try:
        # Get the request body
        body = await request.json()
        user_message = body.get("message", "")
        conversation_id = body.get("conversation_id")
        user_id = body.get("user_id")
        
        if not user_message:
            return JSONResponse(
                status_code=400,
                content={"error": "Message is required"}
            )
        
        # Parse conversation_id if provided
        parsed_conversation_id = None
        if conversation_id:
            try:
                parsed_conversation_id = uuid.UUID(conversation_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid conversation_id format"}
                )
        
        # Parse user_id if provided
        parsed_user_id = None
        if user_id:
            try:
                parsed_user_id = uuid.UUID(user_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid user_id format"}
                )
        
        # Create SSE response
        async def event_generator():
            try:
                async for chunk in ChatService.chat_with_llama_stream(
                    user_message,
                    conversation_id=parsed_conversation_id,
                    user_id=parsed_user_id
                ):
                    yield {
                        "event": "message",
                        "data": json.dumps(chunk)
                    }
                # Send completion event
                yield {
                    "event": "complete",
                    "data": json.dumps({"status": "completed"})
                }
            except Exception as e:
                yield {
                    "event": "error",
                    "data": json.dumps({"error": str(e)})
                }
        
        return EventSourceResponse(event_generator())
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.get("/api/chat/conversations")
async def get_conversations(user_id: Optional[str] = None, limit: int = 50, offset: int = 0):
    """Get conversations for a user"""
    try:
        parsed_user_id = None
        if user_id:
            try:
                parsed_user_id = uuid.UUID(user_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid user_id format"}
                )
        
        conversations = await ChatHistoryService.get_user_conversations(
            parsed_user_id, limit=limit, offset=offset
        )
        
        return JSONResponse(content={
            "conversations": [
                {
                    "id": str(conv.id),
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat(),
                    "is_active": conv.is_active
                }
                for conv in conversations
            ]
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.get("/api/chat/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation with its messages"""
    try:
        parsed_conversation_id = uuid.UUID(conversation_id)
        conversation = await ChatHistoryService.get_conversation(parsed_conversation_id)
        
        if not conversation:
            return JSONResponse(
                status_code=404,
                content={"error": "Conversation not found"}
            )
        
        messages = await ChatHistoryService.get_conversation_messages(parsed_conversation_id)
        
        # Process messages to convert markdown to HTML for display
        import markdown
        processed_messages = []
        for msg in messages:
            # For assistant messages, convert markdown to HTML
            if msg.role == "assistant":
                formatted_content = markdown.markdown(
                    msg.content,
                    extensions=['fenced_code', 'codehilite', 'tables', 'nl2br']
                )
            else:
                # For user messages, keep as-is (they're usually plain text)
                formatted_content = msg.content
                
            processed_messages.append({
                "id": str(msg.id),
                "role": msg.role,
                "content": formatted_content,
                "created_at": msg.created_at.isoformat(),
                "model": msg.model
            })
        
        return JSONResponse(content={
            "conversation": {
                "id": str(conversation.id),
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "is_active": conversation.is_active
            },
            "messages": processed_messages
        })
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid conversation_id format"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.put("/api/chat/conversations/{conversation_id}/title")
async def update_conversation_title(conversation_id: str, request: Request):
    """Update conversation title"""
    try:
        parsed_conversation_id = uuid.UUID(conversation_id)
        body = await request.json()
        title = body.get("title", "")
        
        if not title:
            return JSONResponse(
                status_code=400,
                content={"error": "Title is required"}
            )
        
        success = await ChatHistoryService.update_conversation_title(
            parsed_conversation_id, title
        )
        
        if not success:
            return JSONResponse(
                status_code=404,
                content={"error": "Conversation not found"}
            )
        
        return JSONResponse(content={"message": "Title updated successfully"})
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid conversation_id format"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.delete("/api/chat/conversations/{conversation_id}")
async def archive_conversation(conversation_id: str):
    """Archive a conversation (soft delete)"""
    try:
        parsed_conversation_id = uuid.UUID(conversation_id)
        success = await ChatHistoryService.archive_conversation(parsed_conversation_id)
        
        if not success:
            return JSONResponse(
                status_code=404,
                content={"error": "Conversation not found"}
            )
        
        return JSONResponse(content={"message": "Conversation archived successfully"})
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid conversation_id format"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


# =========================
# Folder Management Endpoints
# =========================

@router.post("/api/folders")
async def create_folder(request: Request):
    """Create a new conversation folder"""
    try:
        body = await request.json()
        name = body.get("name", "").strip()
        description = body.get("description", "").strip() or None
        parent_folder_id = body.get("parent_folder_id")
        user_id = body.get("user_id")
        
        if not name:
            return JSONResponse(
                status_code=400,
                content={"error": "Folder name is required"}
            )
        
        # Parse UUIDs if provided
        parsed_parent_folder_id = None
        if parent_folder_id:
            try:
                parsed_parent_folder_id = uuid.UUID(parent_folder_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid parent_folder_id format"}
                )
        
        parsed_user_id = None
        if user_id:
            try:
                parsed_user_id = uuid.UUID(user_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid user_id format"}
                )
        
        folder = await FolderService.create_folder(
            name=name,
            description=description,
            parent_folder_id=parsed_parent_folder_id,
            user_id=parsed_user_id
        )
        
        return JSONResponse(content={
            "id": str(folder.id),
            "name": folder.name,
            "description": folder.description,
            "parent_folder_id": str(folder.parent_folder_id) if folder.parent_folder_id else None,
            "created_at": folder.created_at.isoformat(),
            "updated_at": folder.updated_at.isoformat()
        })
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.get("/api/folders")
async def get_folders(user_id: Optional[str] = None, parent_folder_id: Optional[str] = None):
    """Get folders for a user"""
    try:
        parsed_user_id = None
        if user_id:
            try:
                parsed_user_id = uuid.UUID(user_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid user_id format"}
                )
        
        parsed_parent_folder_id = None
        if parent_folder_id:
            try:
                parsed_parent_folder_id = uuid.UUID(parent_folder_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid parent_folder_id format"}
                )
        
        folders = await FolderService.get_folders(
            user_id=parsed_user_id,
            parent_folder_id=parsed_parent_folder_id
        )
        
        return JSONResponse(content={
            "folders": [
                {
                    "id": str(folder.id),
                    "name": folder.name,
                    "description": folder.description,
                    "parent_folder_id": str(folder.parent_folder_id) if folder.parent_folder_id else None,
                    "created_at": folder.created_at.isoformat(),
                    "updated_at": folder.updated_at.isoformat()
                }
                for folder in folders
            ]
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.get("/api/folders/hierarchy")
async def get_folder_hierarchy(user_id: Optional[str] = None):
    """Get the complete folder hierarchy with conversations"""
    try:
        parsed_user_id = None
        if user_id:
            try:
                parsed_user_id = uuid.UUID(user_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid user_id format"}
                )
        
        hierarchy = await FolderService.get_folder_hierarchy(user_id=parsed_user_id)
        
        # Transform the hierarchy to match frontend expectations
        folders = []
        root_conversations = []
        
        for item in hierarchy:
            if item.get("type") == "folder":
                folders.append(item)
            elif item.get("type") == "conversation":
                root_conversations.append(item)
        
        return JSONResponse(content={
            "folders": folders,
            "root_conversations": root_conversations
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.get("/api/folders/{folder_id}")
async def get_folder(folder_id: str):
    """Get a specific folder by ID"""
    try:
        parsed_folder_id = uuid.UUID(folder_id)
        folder = await FolderService.get_folder(parsed_folder_id)
        
        if not folder:
            return JSONResponse(
                status_code=404,
                content={"error": "Folder not found"}
            )
        
        return JSONResponse(content={
            "id": str(folder.id),
            "name": folder.name,
            "description": folder.description,
            "parent_folder_id": str(folder.parent_folder_id) if folder.parent_folder_id else None,
            "created_at": folder.created_at.isoformat(),
            "updated_at": folder.updated_at.isoformat()
        })
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid folder_id format"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.put("/api/folders/{folder_id}")
async def update_folder(folder_id: str, request: Request):
    """Update folder name and/or description"""
    try:
        parsed_folder_id = uuid.UUID(folder_id)
        body = await request.json()
        name = body.get("name", "").strip() or None
        description = body.get("description", "").strip() or None
        
        if name is None and description is None:
            return JSONResponse(
                status_code=400,
                content={"error": "At least one field (name or description) must be provided"}
            )
        
        success = await FolderService.update_folder(
            folder_id=parsed_folder_id,
            name=name,
            description=description
        )
        
        if not success:
            return JSONResponse(
                status_code=404,
                content={"error": "Folder not found"}
            )
        
        return JSONResponse(content={"message": "Folder updated successfully"})
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid folder_id format"}
        )
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.delete("/api/folders/{folder_id}")
async def delete_folder(folder_id: str):
    """Delete a folder (soft delete)"""
    try:
        parsed_folder_id = uuid.UUID(folder_id)
        success = await FolderService.delete_folder(parsed_folder_id)
        
        if not success:
            return JSONResponse(
                status_code=404,
                content={"error": "Folder not found"}
            )
        
        return JSONResponse(content={"message": "Folder deleted successfully"})
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid folder_id format"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.post("/api/conversations/{conversation_id}/move")
async def move_conversation(conversation_id: str, request: Request):
    """Move a conversation to a folder or to root"""
    try:
        parsed_conversation_id = uuid.UUID(conversation_id)
        body = await request.json()
        folder_id = body.get("folder_id")
        
        parsed_folder_id = None
        if folder_id:
            try:
                parsed_folder_id = uuid.UUID(folder_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid folder_id format"}
                )
        
        success = await FolderService.move_conversation_to_folder(
            conversation_id=parsed_conversation_id,
            folder_id=parsed_folder_id
        )
        
        if not success:
            return JSONResponse(
                status_code=404,
                content={"error": "Conversation not found"}
            )
        
        return JSONResponse(content={"message": "Conversation moved successfully"})
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid conversation_id format"}
        )
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.get("/api/folders/{folder_id}/conversations")
async def get_conversations_in_folder(folder_id: str, user_id: Optional[str] = None):
    """Get conversations in a specific folder"""
    try:
        parsed_folder_id = uuid.UUID(folder_id)
        parsed_user_id = None
        if user_id:
            try:
                parsed_user_id = uuid.UUID(user_id)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid user_id format"}
                )
        
        conversations = await FolderService.get_conversations_in_folder(
            folder_id=parsed_folder_id,
            user_id=parsed_user_id
        )
        
        return JSONResponse(content={
            "conversations": [
                {
                    "id": str(conv.id),
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat(),
                    "is_active": conv.is_active
                }
                for conv in conversations
            ]
        })
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid folder_id format"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )
