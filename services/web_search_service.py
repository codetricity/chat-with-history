"""
Web search service using Tavily API for AI chat functionality
"""
import os
import logging
from typing import Dict, Any, List, Optional
from tavily import TavilyClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSearchService:
    """Service for web search operations using Tavily API"""

    def __init__(self):
        """Initialize the Tavily client with API key from environment"""
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            logger.warning("TAVILY_API_KEY not found in environment variables")
            self.client = None
        else:
            self.client = TavilyClient(api_key=self.api_key)
            logger.info("Tavily client initialized successfully")

    async def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Perform a web search using Tavily API
        
        Args:
            query: The search query
            max_results: Maximum number of results to return (default: 5)
            
        Returns:
            dict: Search results with sources and content
        """
        if not self.client:
            return {
                "success": False,
                "error": "Tavily API key not configured",
                "results": []
            }
        
        try:
            logger.info(f"Performing web search for query: {query}")
            
            # Perform the search
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=max_results,
                include_answer=True,
                include_raw_content=False,
                include_images=False
            )
            
            # Extract and format results
            results = []
            if "results" in response:
                for result in response["results"]:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", ""),
                        "score": result.get("score", 0.0)
                    })
            
            # Get the answer if available
            answer = response.get("answer", "")
            
            logger.info(f"Search completed. Found {len(results)} results")
            
            return {
                "success": True,
                "query": query,
                "answer": answer,
                "results": results,
                "total_results": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }

    def should_search(self, user_message: str) -> bool:
        """
        Determine if a user message requires web search
        
        Args:
            user_message: The user's message
            
        Returns:
            bool: True if web search should be performed
        """
        # Keywords that suggest the user wants current information
        search_keywords = [
            "current", "latest", "recent", "today", "now", "2024", "2025",
            "news", "update", "happening", "trending", "what's new",
            "price", "cost", "rate", "stock", "market", "weather",
            "search for", "find", "look up", "research", "information about"
        ]
        
        # Questions that typically need current information
        question_words = ["what", "when", "where", "who", "how", "why"]
        
        message_lower = user_message.lower()
        
        # Check for search keywords
        for keyword in search_keywords:
            if keyword in message_lower:
                return True
        
        # Check for questions about current events or specific information
        if any(word in message_lower for word in question_words):
            # Additional context clues for current information needs
            current_info_clues = [
                "happening", "going on", "latest", "recent", "current",
                "now", "today", "this week", "this month", "this year"
            ]
            if any(clue in message_lower for clue in current_info_clues):
                return True
        
        return False

    def format_search_results_for_llm(self, search_data: Dict[str, Any]) -> str:
        """
        Format search results for inclusion in LLM context
        
        Args:
            search_data: The search results from Tavily API
            
        Returns:
            str: Formatted search results for LLM context
        """
        if not search_data.get("success") or not search_data.get("results"):
            return ""
        
        formatted_results = []
        
        # Add the answer if available
        if search_data.get("answer"):
            formatted_results.append(f"**Search Answer:** {search_data['answer']}\n")
        
        # Add individual results
        formatted_results.append("**Search Results:**")
        for i, result in enumerate(search_data["results"], 1):
            formatted_results.append(
                f"{i}. **{result['title']}**\n"
                f"   URL: {result['url']}\n"
                f"   Content: {result['content'][:300]}{'...' if len(result['content']) > 300 else ''}\n"
            )
        
        return "\n".join(formatted_results)

    async def test_connection(self) -> Dict[str, Any]:
        """
        Test the Tavily API connection
        
        Returns:
            dict: Connection test result
        """
        if not self.client:
            return {
                "status": "error",
                "message": "Tavily API key not configured"
            }
        
        try:
            # Perform a simple test search
            test_result = await self.search("test search", max_results=1)
            
            if test_result["success"]:
                return {
                    "status": "success",
                    "message": "Tavily API connection successful",
                    "test_results": test_result
                }
            else:
                return {
                    "status": "error",
                    "message": f"Tavily API test failed: {test_result.get('error', 'Unknown error')}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Tavily API test exception: {str(e)}"
            }
