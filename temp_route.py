@router.get("/conversation-learning-goals", response_class=HTMLResponse)
async def conversation_learning_goals(request: Request):
    """Learning goals page for conversation organization documentation"""
    try:
        # Read the markdown file
        markdown_path = "docs/learning/conversation_organization.md"
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
            <title>Conversation Organization Learning Goals</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8fafc;
                }}
                .container {{
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 40px;
                }}
                h1 {{
                    color: #1e40af;
                    border-bottom: 3px solid #3b82f6;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #1e40af;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #374151;
                }}
                code {{
                    background-color: #f1f5f9;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                }}
                pre {{
                    background-color: #1e293b;
                    color: #e2e8f0;
                    padding: 20px;
                    border-radius: 8px;
                    overflow-x: auto;
                }}
                pre code {{
                    background-color: transparent;
                    color: inherit;
                }}
                .close-btn {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #ef4444;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;
                    z-index: 1000;
                }}
                .close-btn:hover {{
                    background: #dc2626;
                }}
                blockquote {{
                    border-left: 4px solid #3b82f6;
                    margin: 20px 0;
                    padding: 10px 20px;
                    background-color: #f8fafc;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #e5e7eb;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f3f4f6;
                    font-weight: 600;
                }}
            </style>
        </head>
        <body>
            <button class="close-btn" onclick="window.close()">Close Window</button>
            <div class="container">
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
