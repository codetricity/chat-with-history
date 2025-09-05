"""
Title Generation Service for creating meaningful conversation titles
"""
import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TitleGenerationService:
    """Service for generating conversation titles from AI responses"""

    @staticmethod
    def generate_title_from_response(ai_response: str, user_message: str = None) -> str:
        """
        Generate a meaningful title from AI response or user message
        
        Args:
            ai_response: The AI's response content
            user_message: The user's original message (optional)
            
        Returns:
            str: A generated title (max 50 characters)
        """
        try:
            # Clean the response text
            clean_response = TitleGenerationService._clean_text(ai_response)
            
            # Try to extract title from AI response first
            title = TitleGenerationService._extract_title_from_response(clean_response)
            
            # If no good title from AI response, try user message
            if not title and user_message:
                title = TitleGenerationService._extract_title_from_user_message(user_message)
            
            # If still no title, create a generic one
            if not title:
                title = "New Conversation"
            
            # Ensure title is not too long
            if len(title) > 50:
                title = title[:47] + "..."
            
            logger.info(f"Generated title: '{title}' from response length: {len(ai_response)}")
            return title
            
        except Exception as e:
            logger.error(f"Error generating title: {e}")
            return "New Conversation"

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing markdown and extra whitespace"""
        if not text:
            return ""
        
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'`(.*?)`', r'\1', text)        # Inline code
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # Code blocks
        text = re.sub(r'#{1,6}\s*', '', text)         # Headers
        text = re.sub(r'^\s*[-*+]\s*', '', text, flags=re.MULTILINE)  # List items
        text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)  # Numbered lists
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    @staticmethod
    def _extract_title_from_response(response: str) -> Optional[str]:
        """Extract a title from the AI response"""
        if not response:
            return None
        
        # Look for the first sentence or phrase that could be a title
        sentences = re.split(r'[.!?]+', response)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Too short
                continue
            if len(sentence) > 50:  # Too long, take first part
                sentence = sentence[:47] + "..."
            
            # Skip common AI response patterns
            skip_patterns = [
                r'^(hello|hi|hey)',
                r'^(i\'m|i am)',
                r'^(thank you|thanks)',
                r'^(you\'re welcome|no problem)',
                r'^(i can help|i\'d be happy)',
                r'^(let me|i\'ll)',
                r'^(sure|of course|absolutely)',
                r'^(i understand|i see)',
                r'^(here\'s|here is)',
                r'^(that\'s|that is)',
                r'^(this is|this)',
                r'^(the|a|an)\s+\w+\s+is',
            ]
            
            if any(re.match(pattern, sentence.lower()) for pattern in skip_patterns):
                continue
            
            # Check if it looks like a meaningful title
            if TitleGenerationService._is_good_title(sentence):
                return sentence
        
        return None

    @staticmethod
    def _extract_title_from_user_message(user_message: str) -> Optional[str]:
        """Extract a title from the user's message"""
        if not user_message:
            return None
        
        clean_message = TitleGenerationService._clean_text(user_message)
        
        # Take first sentence or first 50 characters
        sentences = re.split(r'[.!?]+', clean_message)
        first_sentence = sentences[0].strip()
        
        if len(first_sentence) > 50:
            first_sentence = first_sentence[:47] + "..."
        
        if len(first_sentence) >= 10 and TitleGenerationService._is_good_title(first_sentence):
            return first_sentence
        
        return None

    @staticmethod
    def _is_good_title(text: str) -> bool:
        """Check if text would make a good title"""
        if not text or len(text) < 5:
            return False
        
        # Check for common question words that might make good titles
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'who']
        if any(text.lower().startswith(word) for word in question_words):
            return True
        
        # Check for action words
        action_words = ['create', 'build', 'make', 'write', 'explain', 'describe', 'show', 'help']
        if any(word in text.lower() for word in action_words):
            return True
        
        # Check for topic indicators
        topic_indicators = ['about', 'regarding', 'concerning', 'on the topic of']
        if any(indicator in text.lower() for indicator in topic_indicators):
            return True
        
        # If it's a reasonable length and doesn't start with common AI patterns, it's probably good
        return len(text) >= 10 and not text.lower().startswith(('i ', 'you ', 'we ', 'they '))
