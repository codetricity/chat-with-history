"""
Page routes for the AI chat application
"""
import os
import markdown
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Home page with AI chat interface"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "AI Chat - FastOpp"
    })


@router.get("/conversation-browser", response_class=HTMLResponse)
async def conversation_browser(request: Request):
    """Conversation browser page with folder management"""
    return templates.TemplateResponse("conversation_browser.html", {
        "request": request,
        "title": "Conversation Browser - FastOpp"
    })


@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    """Dedicated search page with hybrid search capabilities"""
    return templates.TemplateResponse("search.html", {
        "request": request,
        "title": "Search - FastOpp"
    })


@router.get("/learning-goals", response_class=HTMLResponse)
async def learning_goals(request: Request):
    """Learning goals page with vector database and hybrid search documentation"""
    try:
        # Read the markdown file
        markdown_path = "docs/learning/docs/vector_db_hybrid_search.md"
        if not os.path.exists(markdown_path):
            return HTMLResponse(
                content="<h1>Learning Goals</h1><p>Documentation not found.</p>",
                status_code=404
            )

        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['fenced_code', 'codehilite', 'tables', 'nl2br', 'toc']
        )

        # Create a styled HTML page
        styled_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Learning Goals - Vector Databases & Hybrid Search</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                .markdown-content {{
                    max-width: 4xl;
                    margin: 0 auto;
                    padding: 2rem;
                }}
                .markdown-content h1 {{
                    font-size: 2.25rem;
                    font-weight: 700;
                    color: #111827;
                    margin-bottom: 1.5rem;
                    border-bottom: 1px solid #e5e7eb;
                    padding-bottom: 1rem;
                }}
                .markdown-content h2 {{
                    font-size: 1.875rem;
                    font-weight: 600;
                    color: #1f2937;
                    margin-bottom: 1rem;
                    margin-top: 2rem;
                }}
                .markdown-content h3 {{
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 0.75rem;
                    margin-top: 1.5rem;
                }}
                .markdown-content h4 {{
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 0.5rem;
                    margin-top: 1rem;
                }}
                .markdown-content p {{
                    color: #374151;
                    margin-bottom: 1rem;
                    line-height: 1.625;
                }}
                .markdown-content ul, .markdown-content ol {{
                    margin-bottom: 1rem;
                    padding-left: 1.5rem;
                }}
                .markdown-content li {{
                    color: #374151;
                    margin-bottom: 0.5rem;
                }}
                .markdown-content code {{
                    background-color: #f3f4f6;
                    color: #1f2937;
                    padding: 0.25rem 0.5rem;
                    border-radius: 0.25rem;
                    font-size: 0.875rem;
                    font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
                }}
                .markdown-content pre {{
                    background-color: #111827;
                    color: #f3f4f6;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    overflow-x: auto;
                    margin-bottom: 1rem;
                }}
                .markdown-content pre code {{
                    background-color: transparent;
                    color: #f3f4f6;
                    padding: 0;
                }}
                .markdown-content table {{
                    width: 100%;
                    border-collapse: collapse;
                    border: 1px solid #d1d5db;
                    margin-bottom: 1rem;
                }}
                .markdown-content th {{
                    background-color: #f3f4f6;
                    border: 1px solid #d1d5db;
                    padding: 0.5rem 1rem;
                    text-align: left;
                    font-weight: 600;
                }}
                .markdown-content td {{
                    border: 1px solid #d1d5db;
                    padding: 0.5rem 1rem;
                }}
                .markdown-content blockquote {{
                    border-left: 4px solid #3b82f6;
                    padding-left: 1rem;
                    font-style: italic;
                    color: #6b7280;
                    margin: 1rem 0;
                }}
                .markdown-content a {{
                    color: #2563eb;
                    text-decoration: underline;
                }}
                .markdown-content a:hover {{
                    color: #1d4ed8;
                }}
                .markdown-content strong {{
                    font-weight: 700;
                }}
                .markdown-content em {{
                    font-style: italic;
                }}
            </style>
        </head>
        <body class="bg-gray-50">
            <div class="min-h-screen">
                <!-- Header -->
                <div class="bg-white shadow-sm border-b">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <button onclick="window.close()"
                                        class="flex items-center text-gray-600 hover:text-gray-800">
                                    <i class="fas fa-arrow-left mr-2"></i>
                                    Close
                                </button>
                                <h1 class="text-xl font-semibold text-gray-900">
                                    <i class="fas fa-graduation-cap text-blue-600 mr-2"></i>
                                    Learning Goals: Vector Databases & Hybrid Search
                                </h1>
                            </div>
                            <div class="text-sm text-gray-500">
                                <i class="fas fa-book mr-1"></i>
                                Educational Content
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Content -->
                <div class="markdown-content">
                    {html_content}
                </div>
            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=styled_html)

    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error</h1><p>Failed to load learning goals: {str(e)}</p>",
            status_code=500
        )


@router.get("/chat-learning-goals", response_class=HTMLResponse)
async def chat_learning_goals(request: Request):
    """Learning goals page for AI chat UI documentation"""
    try:
        # Read the markdown file
        markdown_path = "docs/learning/docs/ai_chat_ui.md"
        if not os.path.exists(markdown_path):
            return HTMLResponse(
                content="<h1>Learning Goals</h1><p>Documentation not found.</p>",
                status_code=404
            )

        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['fenced_code', 'codehilite', 'tables', 'nl2br', 'toc']
        )

        # Create a styled HTML page
        styled_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Learning Goals - AI Chat UI</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                .markdown-content {{
                    max-width: 4xl;
                    margin: 0 auto;
                    padding: 2rem;
                }}
                .markdown-content h1 {{
                    font-size: 2.25rem;
                    font-weight: 700;
                    color: #111827;
                    margin-bottom: 1.5rem;
                    border-bottom: 1px solid #e5e7eb;
                    padding-bottom: 1rem;
                }}
                .markdown-content h2 {{
                    font-size: 1.875rem;
                    font-weight: 600;
                    color: #1f2937;
                    margin-bottom: 1rem;
                    margin-top: 2rem;
                }}
                .markdown-content h3 {{
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 0.75rem;
                    margin-top: 1.5rem;
                }}
                .markdown-content h4 {{
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 0.5rem;
                    margin-top: 1rem;
                }}
                .markdown-content p {{
                    color: #374151;
                    margin-bottom: 1rem;
                    line-height: 1.625;
                }}
                .markdown-content ul, .markdown-content ol {{
                    margin-bottom: 1rem;
                    padding-left: 1.5rem;
                }}
                .markdown-content li {{
                    color: #374151;
                    margin-bottom: 0.5rem;
                }}
                .markdown-content code {{
                    background-color: #f3f4f6;
                    color: #1f2937;
                    padding: 0.25rem 0.5rem;
                    border-radius: 0.25rem;
                    font-size: 0.875rem;
                    font-family: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
                }}
                .markdown-content pre {{
                    background-color: #111827;
                    color: #f3f4f6;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    overflow-x: auto;
                    margin-bottom: 1rem;
                }}
                .markdown-content pre code {{
                    background-color: transparent;
                    color: #f3f4f6;
                    padding: 0;
                }}
                .markdown-content table {{
                    width: 100%;
                    border-collapse: collapse;
                    border: 1px solid #d1d5db;
                    margin-bottom: 1rem;
                }}
                .markdown-content th {{
                    background-color: #f3f4f6;
                    border: 1px solid #d1d5db;
                    padding: 0.5rem 1rem;
                    text-align: left;
                    font-weight: 600;
                }}
                .markdown-content td {{
                    border: 1px solid #d1d5db;
                    padding: 0.5rem 1rem;
                }}
                .markdown-content blockquote {{
                    border-left: 4px solid #3b82f6;
                    padding-left: 1rem;
                    font-style: italic;
                    color: #6b7280;
                    margin: 1rem 0;
                }}
                .markdown-content a {{
                    color: #2563eb;
                    text-decoration: underline;
                }}
                .markdown-content a:hover {{
                    color: #1d4ed8;
                }}
                .markdown-content strong {{
                    font-weight: 700;
                }}
                .markdown-content em {{
                    font-style: italic;
                }}
            </style>
        </head>
        <body class="bg-gray-50">
            <div class="min-h-screen">
                <!-- Header -->
                <div class="bg-white shadow-sm border-b">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <button onclick="window.close()"
                                        class="flex items-center text-gray-600 hover:text-gray-800">
                                    <i class="fas fa-arrow-left mr-2"></i>
                                    Close
                                </button>
                                <h1 class="text-xl font-semibold text-gray-900">
                                    <i class="fas fa-graduation-cap text-blue-600 mr-2"></i>
                                    Learning Goals: AI Chat UI
                                </h1>
                            </div>
                            <div class="text-sm text-gray-500">
                                <i class="fas fa-book mr-1"></i>
                                Educational Content
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Content -->
                <div class="markdown-content">
                    {html_content}
                </div>
            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=styled_html)

    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error</h1><p>Failed to load learning goals: {str(e)}</p>",
            status_code=500
        )


@router.get("/conversation-learning-goals", response_class=HTMLResponse)
async def conversation_learning_goals(request: Request):
    """Learning goals page for conversation organization documentation"""
    try:
        # Read the markdown file
        markdown_path = "docs/learning/docs/conversation_organization.md"
        if not os.path.exists(markdown_path):
            return HTMLResponse(
                content="<h1>Learning Goals</h1><p>Documentation not found.</p>",
                status_code=404
            )

        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['fenced_code', 'codehilite', 'tables', 'nl2br', 'toc']
        )

        # Create a styled HTML page
        styled_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Learning Goals - Conversation Organization</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                .markdown-content {{
                    max-width: 4xl;
                    margin: 0 auto;
                    padding: 2rem;
                }}
                .markdown-content h1 {{
                    font-size: 2.25rem;
                    font-weight: 700;
                    color: #111827;
                    margin-bottom: 1.5rem;
                    border-bottom: 1px solid #e5e7eb;
                    padding-bottom: 1rem;
                }}
                .markdown-content h2 {{
                    font-size: 1.875rem;
                    font-weight: 600;
                    color: #1f2937;
                    margin-bottom: 1rem;
                    margin-top: 2rem;
                }}
                .markdown-content h3 {{
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 0.75rem;
                    margin-top: 1.5rem;
                }}
                .markdown-content h4 {{
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 0.5rem;
                    margin-top: 1rem;
                }}
                .markdown-content p {{
                    color: #374151;
                    margin-bottom: 1rem;
                    line-height: 1.75;
                }}
                .markdown-content ul, .markdown-content ol {{
                    color: #374151;
                    margin-bottom: 1rem;
                    padding-left: 1.5rem;
                }}
                .markdown-content li {{
                    margin-bottom: 0.5rem;
                }}
                .markdown-content code {{
                    background-color: #f3f4f6;
                    color: #1f2937;
                    padding: 0.25rem 0.5rem;
                    border-radius: 0.375rem;
                    font-size: 0.875rem;
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                }}
                .markdown-content pre {{
                    background-color: #1f2937;
                    color: #f9fafb;
                    padding: 1.5rem;
                    border-radius: 0.5rem;
                    overflow-x: auto;
                    margin-bottom: 1.5rem;
                }}
                .markdown-content pre code {{
                    background-color: transparent;
                    color: inherit;
                    padding: 0;
                }}
                .markdown-content blockquote {{
                    border-left: 4px solid #3b82f6;
                    background-color: #f8fafc;
                    padding: 1rem 1.5rem;
                    margin: 1.5rem 0;
                    color: #374151;
                }}
                .markdown-content table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1.5rem 0;
                }}
                .markdown-content th, .markdown-content td {{
                    border: 1px solid #e5e7eb;
                    padding: 0.75rem;
                    text-align: left;
                }}
                .markdown-content th {{
                    background-color: #f9fafb;
                    font-weight: 600;
                    color: #374151;
                }}
                .markdown-content a {{
                    color: #3b82f6;
                    text-decoration: underline;
                }}
                .markdown-content a:hover {{
                    color: #1d4ed8;
                }}
                .close-btn {{
                    position: fixed;
                    top: 1.25rem;
                    right: 1.25rem;
                    background-color: #6b7280;
                    color: white;
                    border: none;
                    padding: 0.625rem 1.25rem;
                    border-radius: 0.375rem;
                    cursor: pointer;
                    font-size: 0.875rem;
                    z-index: 1000;
                    transition: background-color 0.2s;
                }}
                .close-btn:hover {{
                    background-color: #4b5563;
                }}
            </style>
        </head>
        <body class="bg-gray-50 min-h-screen">
            <button class="close-btn" onclick="window.close()">
                <i class="fas fa-times mr-2"></i>Close Window
            </button>
            <div class="markdown-content bg-white shadow-lg rounded-lg">
                {html_content}
            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=styled_html)

    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error</h1><p>Failed to load learning goals: {str(e)}</p>",
            status_code=500
        )


@router.get("/search-learning-goals", response_class=HTMLResponse)
async def search_learning_goals(request: Request):
    """Learning goals page for search functionality documentation"""
    try:
        # Read the markdown file
        markdown_path = "docs/learning/docs/vector_db_hybrid_search.md"
        if not os.path.exists(markdown_path):
            return HTMLResponse(
                content="<h1>Learning Goals</h1><p>Documentation not found.</p>",
                status_code=404
            )

        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['fenced_code', 'codehilite', 'tables', 'nl2br', 'toc']
        )

        # Create a styled HTML page
        styled_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Learning Goals - Search & Hybrid Search</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                .markdown-content {{
                    max-width: 4xl;
                    margin: 0 auto;
                    padding: 2rem;
                }}
                .markdown-content h1 {{
                    font-size: 2.25rem;
                    font-weight: 700;
                    color: #111827;
                    margin-bottom: 1.5rem;
                    border-bottom: 1px solid #e5e7eb;
                    padding-bottom: 1rem;
                }}
                .markdown-content h2 {{
                    font-size: 1.875rem;
                    font-weight: 600;
                    color: #1f2937;
                    margin-bottom: 1rem;
                    margin-top: 2rem;
                }}
                .markdown-content h3 {{
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 0.75rem;
                    margin-top: 1.5rem;
                }}
                .markdown-content h4 {{
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: #374151;
                    margin-bottom: 0.5rem;
                    margin-top: 1rem;
                }}
                .markdown-content p {{
                    color: #374151;
                    margin-bottom: 1rem;
                    line-height: 1.75;
                }}
                .markdown-content ul, .markdown-content ol {{
                    color: #374151;
                    margin-bottom: 1rem;
                    padding-left: 1.5rem;
                }}
                .markdown-content li {{
                    margin-bottom: 0.5rem;
                }}
                .markdown-content code {{
                    background-color: #f3f4f6;
                    color: #1f2937;
                    padding: 0.25rem 0.5rem;
                    border-radius: 0.375rem;
                    font-size: 0.875rem;
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                }}
                .markdown-content pre {{
                    background-color: #1f2937;
                    color: #f9fafb;
                    padding: 1.5rem;
                    border-radius: 0.5rem;
                    overflow-x: auto;
                    margin-bottom: 1.5rem;
                }}
                .markdown-content pre code {{
                    background-color: transparent;
                    color: inherit;
                    padding: 0;
                }}
                .markdown-content blockquote {{
                    border-left: 4px solid #3b82f6;
                    background-color: #f8fafc;
                    padding: 1rem 1.5rem;
                    margin: 1.5rem 0;
                    color: #374151;
                }}
                .markdown-content table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1.5rem 0;
                }}
                .markdown-content th, .markdown-content td {{
                    border: 1px solid #e5e7eb;
                    padding: 0.75rem;
                    text-align: left;
                }}
                .markdown-content th {{
                    background-color: #f9fafb;
                    font-weight: 600;
                    color: #374151;
                }}
                .markdown-content a {{
                    color: #3b82f6;
                    text-decoration: underline;
                }}
                .markdown-content a:hover {{
                    color: #1d4ed8;
                }}
                .close-btn {{
                    position: fixed;
                    top: 1.25rem;
                    right: 1.25rem;
                    background-color: #6b7280;
                    color: white;
                    border: none;
                    padding: 0.625rem 1.25rem;
                    border-radius: 0.375rem;
                    cursor: pointer;
                    font-size: 0.875rem;
                    z-index: 1000;
                    transition: background-color 0.2s;
                }}
                .close-btn:hover {{
                    background-color: #4b5563;
                }}
            </style>
        </head>
        <body class="bg-gray-50 min-h-screen">
            <button class="close-btn" onclick="window.close()">
                <i class="fas fa-times mr-2"></i>Close Window
            </button>
            <div class="markdown-content bg-white shadow-lg rounded-lg">
                {html_content}
            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=styled_html)

    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error</h1><p>Failed to load learning goals: {str(e)}</p>",
            status_code=500
        )
