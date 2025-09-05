"""
Chat routes for AI chat functionality
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from services.chat_service import ChatService
from services.chat_history_service import ChatHistoryService
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
