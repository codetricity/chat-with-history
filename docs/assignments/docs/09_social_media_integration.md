---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Social Media Integration Assignment**
## Real-Time API Data Collection

**Connect to Reddit, YouTube, Twitter, and other social platforms**

---

# Assignment Overview

## What You'll Build

A comprehensive social media integration system that:
- **Connects to multiple APIs** - Reddit, YouTube, Twitter, LinkedIn, GitHub
- **Collects real-time data** - Posts, comments, videos, user profiles
- **Processes and normalizes data** - Standardize different data formats
- **Implements rate limiting** - Respect API limits and terms of service
- **Stores data efficiently** - Optimize for search and analysis
- **Provides real-time updates** - Live data streaming and processing

---

# Problem Statement

## Social Media Data Challenges

Real-world applications need social media data for:
- **Market research** - Understand customer sentiment and trends
- **Content discovery** - Find relevant discussions and influencers
- **Competitive analysis** - Monitor competitor mentions and activities
- **Lead generation** - Identify potential customers and partners
- **Brand monitoring** - Track mentions and reputation
- **Trend analysis** - Identify emerging topics and patterns

---

# Your Solution

## Multi-Platform Integration

Create a social media integration system that addresses these challenges:

1. **Unified API Interface** - Consistent interface across platforms
2. **Real-time Data Collection** - Live streaming and batch processing
3. **Data Normalization** - Standardize different data formats
4. **Rate Limiting & Caching** - Efficient API usage and data storage
5. **Error Handling & Recovery** - Robust error handling and retry logic
6. **Data Quality Assurance** - Validate and clean collected data

---

# Technical Requirements

## Tech Stack

- **Python 3.8+** with asyncio support
- **PRAW** - Reddit API wrapper
- **Google API Client** - YouTube Data API
- **Tweepy** - Twitter API wrapper
- **LinkedIn API** - Professional network data
- **GitHub API** - Developer community data
- **Redis** - Caching and rate limiting
- **Celery** - Background task processing
- **FastAPI** - API endpoints for data access

---

# Project Structure

## Recommended Architecture

```
social_media_integration/
├── src/
│   ├── connectors/
│   │   ├── base.py
│   │   ├── reddit.py
│   │   ├── youtube.py
│   │   ├── twitter.py
│   │   └── linkedin.py
│   ├── models/
│   │   ├── post.py
│   │   ├── user.py
│   │   ├── comment.py
│   │   └── video.py
│   ├── services/
│   │   ├── rate_limiter.py
│   │   ├── data_processor.py
│   │   ├── cache_manager.py
│   │   └── error_handler.py
│   ├── workers/
│   │   ├── collector.py
│   │   ├── processor.py
│   │   └── scheduler.py
│   └── api/
│       ├── endpoints.py
│       └── middleware.py
├── config/
│   ├── api_keys.yaml
│   └── settings.py
├── tests/
│   ├── test_connectors.py
│   └── test_services.py
└── requirements.txt
```

---

# Core Components

## 1. Base Connector Class

```python
# src/connectors/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncGenerator
import asyncio
import aiohttp
from datetime import datetime, timedelta
import logging

class BaseConnector(ABC):
    def __init__(self, api_key: str, rate_limit: int = 100):
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.requests_made = 0
        self.rate_limit_reset = datetime.now()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the API"""
        pass
    
    @abstractmethod
    async def search_posts(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search for posts matching the query"""
        pass
    
    @abstractmethod
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile information"""
        pass
    
    @abstractmethod
    async def get_comments(self, post_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get comments for a specific post"""
        pass
    
    async def rate_limit_check(self):
        """Check and enforce rate limits"""
        if datetime.now() < self.rate_limit_reset:
            await asyncio.sleep(1)
            return
        
        if self.requests_made >= self.rate_limit:
            sleep_time = (self.rate_limit_reset - datetime.now()).total_seconds()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            self.requests_made = 0
            self.rate_limit_reset = datetime.now() + timedelta(hours=1)
    
    async def make_request(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make an authenticated API request"""
        await self.rate_limit_check()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    self.requests_made += 1
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"API request failed: {response.status}")
                        return {}
        except Exception as e:
            self.logger.error(f"Request error: {str(e)}")
            return {}
```

---

# Core Components

## 2. Reddit Connector

```python
# src/connectors/reddit.py
import praw
from typing import Dict, Any, List
from .base import BaseConnector

class RedditConnector(BaseConnector):
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        super().__init__(client_id, rate_limit=100)
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.reddit = None
    
    async def authenticate(self) -> bool:
        """Authenticate with Reddit API"""
        try:
            self.reddit = praw.Reddit(
                client_id=self.api_key,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
            # Test authentication
            self.reddit.user.me()
            return True
        except Exception as e:
            self.logger.error(f"Reddit authentication failed: {str(e)}")
            return False
    
    async def search_posts(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search for Reddit posts"""
        if not self.reddit:
            await self.authenticate()
        
        posts = []
        try:
            subreddit = self.reddit.subreddit("all")
            for post in subreddit.search(query, limit=limit):
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'content': post.selftext,
                    'author': str(post.author) if post.author else 'deleted',
                    'subreddit': str(post.subreddit),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'created_utc': post.created_utc,
                    'url': post.url,
                    'permalink': post.permalink,
                    'is_self': post.is_self,
                    'over_18': post.over_18,
                    'stickied': post.stickied,
                    'awards': post.total_awards_received,
                    'flair': post.link_flair_text,
                    'platform': 'reddit'
                }
                posts.append(post_data)
        except Exception as e:
            self.logger.error(f"Reddit search failed: {str(e)}")
        
        return posts
    
    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get Reddit user profile"""
        if not self.reddit:
            await self.authenticate()
        
        try:
            user = self.reddit.redditor(username)
            return {
                'id': str(user),
                'username': str(user),
                'created_utc': user.created_utc,
                'karma': user.comment_karma + user.link_karma,
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'is_employee': user.is_employee,
                'is_mod': user.is_mod,
                'is_gold': user.is_gold,
                'is_verified': user.verified,
                'platform': 'reddit'
            }
        except Exception as e:
            self.logger.error(f"Failed to get Reddit user profile: {str(e)}")
            return {}
    
    async def get_comments(self, post_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get Reddit post comments"""
        if not self.reddit:
            await self.authenticate()
        
        comments = []
        try:
            post = self.reddit.submission(id=post_id)
            post.comments.replace_more(limit=0)
            for comment in post.comments.list()[:limit]:
                comment_data = {
                    'id': comment.id,
                    'post_id': post_id,
                    'author': str(comment.author) if comment.author else 'deleted',
                    'body': comment.body,
                    'score': comment.score,
                    'created_utc': comment.created_utc,
                    'is_submitter': comment.is_submitter,
                    'stickied': comment.stickied,
                    'awards': comment.total_awards_received,
                    'platform': 'reddit'
                }
                comments.append(comment_data)
        except Exception as e:
            self.logger.error(f"Failed to get Reddit comments: {str(e)}")
        
        return comments
```

---

# Core Components

## 3. YouTube Connector

```python
# src/connectors/youtube.py
from googleapiclient.discovery import build
from typing import Dict, Any, List
from .base import BaseConnector

class YouTubeConnector(BaseConnector):
    def __init__(self, api_key: str):
        super().__init__(api_key, rate_limit=10000)
        self.youtube = None
    
    async def authenticate(self) -> bool:
        """Authenticate with YouTube API"""
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
            # Test authentication with a simple request
            request = self.youtube.channels().list(part='snippet', mine=True)
            request.execute()
            return True
        except Exception as e:
            self.logger.error(f"YouTube authentication failed: {str(e)}")
            return False
    
    async def search_videos(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search for YouTube videos"""
        if not self.youtube:
            await self.authenticate()
        
        videos = []
        try:
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=min(limit, 50),  # YouTube API limit
                type='video',
                order='relevance'
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            
            # Get detailed video information
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            for video in video_response['items']:
                video_data = {
                    'id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'channel_id': video['snippet']['channelId'],
                    'channel_title': video['snippet']['channelTitle'],
                    'published_at': video['snippet']['publishedAt'],
                    'duration': video['contentDetails']['duration'],
                    'views': int(video['statistics'].get('viewCount', 0)),
                    'likes': int(video['statistics'].get('likeCount', 0)),
                    'dislikes': int(video['statistics'].get('dislikeCount', 0)),
                    'comments': int(video['statistics'].get('commentCount', 0)),
                    'tags': video['snippet'].get('tags', []),
                    'category_id': video['snippet']['categoryId'],
                    'thumbnail_url': video['snippet']['thumbnails']['high']['url'],
                    'platform': 'youtube'
                }
                videos.append(video_data)
        except Exception as e:
            self.logger.error(f"YouTube search failed: {str(e)}")
        
        return videos
    
    async def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """Get YouTube channel information"""
        if not self.youtube:
            await self.authenticate()
        
        try:
            channel_response = self.youtube.channels().list(
                part='snippet,statistics,contentDetails',
                id=channel_id
            ).execute()
            
            if channel_response['items']:
                channel = channel_response['items'][0]
                return {
                    'id': channel['id'],
                    'title': channel['snippet']['title'],
                    'description': channel['snippet']['description'],
                    'subscriber_count': int(channel['statistics'].get('subscriberCount', 0)),
                    'video_count': int(channel['statistics'].get('videoCount', 0)),
                    'view_count': int(channel['statistics'].get('viewCount', 0)),
                    'created_at': channel['snippet']['publishedAt'],
                    'country': channel['snippet'].get('country'),
                    'thumbnail_url': channel['snippet']['thumbnails']['high']['url'],
                    'platform': 'youtube'
                }
        except Exception as e:
            self.logger.error(f"Failed to get YouTube channel info: {str(e)}")
        
        return {}
    
    async def get_video_comments(self, video_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get YouTube video comments"""
        if not self.youtube:
            await self.authenticate()
        
        comments = []
        try:
            comments_response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(limit, 100),  # YouTube API limit
                order='relevance'
            ).execute()
            
            for comment_thread in comments_response['items']:
                comment = comment_thread['snippet']['topLevelComment']['snippet']
                comment_data = {
                    'id': comment_thread['id'],
                    'video_id': video_id,
                    'author': comment['authorDisplayName'],
                    'author_channel_id': comment.get('authorChannelId', {}).get('value'),
                    'text': comment['textDisplay'],
                    'like_count': comment['likeCount'],
                    'published_at': comment['publishedAt'],
                    'updated_at': comment['updatedAt'],
                    'platform': 'youtube'
                }
                comments.append(comment_data)
        except Exception as e:
            self.logger.error(f"Failed to get YouTube comments: {str(e)}")
        
        return comments
```

---

# Core Components

## 4. Twitter Connector

```python
# src/connectors/twitter.py
import tweepy
from typing import Dict, Any, List
from .base import BaseConnector

class TwitterConnector(BaseConnector):
    def __init__(self, bearer_token: str, consumer_key: str = None, 
                 consumer_secret: str = None, access_token: str = None, 
                 access_token_secret: str = None):
        super().__init__(bearer_token, rate_limit=300)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.client = None
        self.api = None
    
    async def authenticate(self) -> bool:
        """Authenticate with Twitter API"""
        try:
            # For read-only operations, bearer token is sufficient
            self.client = tweepy.Client(bearer_token=self.api_key)
            
            # For write operations, use OAuth 1.0a
            if self.consumer_key and self.consumer_secret:
                auth = tweepy.OAuth1UserHandler(
                    self.consumer_key,
                    self.consumer_secret,
                    self.access_token,
                    self.access_token_secret
                )
                self.api = tweepy.API(auth)
            
            return True
        except Exception as e:
            self.logger.error(f"Twitter authentication failed: {str(e)}")
            return False
    
    async def search_tweets(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search for tweets"""
        if not self.client:
            await self.authenticate()
        
        tweets = []
        try:
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(limit, 100),  # Twitter API limit
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'context_annotations']
            )
            
            if response.data:
                for tweet in response.data:
                    tweet_data = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'author_id': tweet.author_id,
                        'created_at': tweet.created_at.isoformat(),
                        'retweet_count': tweet.public_metrics['retweet_count'],
                        'like_count': tweet.public_metrics['like_count'],
                        'reply_count': tweet.public_metrics['reply_count'],
                        'quote_count': tweet.public_metrics['quote_count'],
                        'platform': 'twitter'
                    }
                    tweets.append(tweet_data)
        except Exception as e:
            self.logger.error(f"Twitter search failed: {str(e)}")
        
        return tweets
    
    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get Twitter user profile"""
        if not self.client:
            await self.authenticate()
        
        try:
            user = self.client.get_user(
                username=username,
                user_fields=['created_at', 'public_metrics', 'description', 'verified']
            )
            
            if user.data:
                return {
                    'id': user.data.id,
                    'username': user.data.username,
                    'name': user.data.name,
                    'description': user.data.description,
                    'created_at': user.data.created_at.isoformat(),
                    'followers_count': user.data.public_metrics['followers_count'],
                    'following_count': user.data.public_metrics['following_count'],
                    'tweet_count': user.data.public_metrics['tweet_count'],
                    'verified': user.data.verified,
                    'platform': 'twitter'
                }
        except Exception as e:
            self.logger.error(f"Failed to get Twitter user profile: {str(e)}")
        
        return {}
    
    async def get_tweet_replies(self, tweet_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get replies to a specific tweet"""
        if not self.client:
            await self.authenticate()
        
        replies = []
        try:
            response = self.client.search_recent_tweets(
                query=f"conversation_id:{tweet_id}",
                max_results=min(limit, 100),
                tweet_fields=['created_at', 'public_metrics', 'author_id']
            )
            
            if response.data:
                for tweet in response.data:
                    if tweet.id != tweet_id:  # Exclude the original tweet
                        reply_data = {
                            'id': tweet.id,
                            'text': tweet.text,
                            'author_id': tweet.author_id,
                            'created_at': tweet.created_at.isoformat(),
                            'retweet_count': tweet.public_metrics['retweet_count'],
                            'like_count': tweet.public_metrics['like_count'],
                            'reply_count': tweet.public_metrics['reply_count'],
                            'platform': 'twitter'
                        }
                        replies.append(reply_data)
        except Exception as e:
            self.logger.error(f"Failed to get Twitter replies: {str(e)}")
        
        return replies
```

---

# Data Processing

## Data Normalization

```python
# src/services/data_processor.py
from typing import Dict, Any, List
from datetime import datetime
import re

class DataProcessor:
    def __init__(self):
        self.platform_processors = {
            'reddit': self._process_reddit_data,
            'youtube': self._process_youtube_data,
            'twitter': self._process_twitter_data
        }
    
    def normalize_post(self, raw_data: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """Normalize post data from different platforms"""
        processor = self.platform_processors.get(platform)
        if processor:
            return processor(raw_data)
        return raw_data
    
    def _process_reddit_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process Reddit-specific data"""
        return {
            'id': data['id'],
            'platform': 'reddit',
            'title': data.get('title', ''),
            'content': data.get('content', ''),
            'author': data.get('author', ''),
            'community': data.get('subreddit', ''),
            'score': data.get('score', 0),
            'engagement': {
                'upvotes': data.get('score', 0),
                'comments': data.get('num_comments', 0),
                'awards': data.get('awards', 0)
            },
            'created_at': datetime.fromtimestamp(data.get('created_utc', 0)),
            'url': data.get('url', ''),
            'metadata': {
                'subreddit': data.get('subreddit', ''),
                'flair': data.get('flair'),
                'nsfw': data.get('over_18', False),
                'stickied': data.get('stickied', False)
            }
        }
    
    def _process_youtube_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process YouTube-specific data"""
        return {
            'id': data['id'],
            'platform': 'youtube',
            'title': data.get('title', ''),
            'content': data.get('description', ''),
            'author': data.get('channel_title', ''),
            'community': data.get('channel_id', ''),
            'score': data.get('likes', 0),
            'engagement': {
                'views': data.get('views', 0),
                'likes': data.get('likes', 0),
                'dislikes': data.get('dislikes', 0),
                'comments': data.get('comments', 0)
            },
            'created_at': datetime.fromisoformat(data.get('published_at', '').replace('Z', '+00:00')),
            'url': f"https://www.youtube.com/watch?v={data['id']}",
            'metadata': {
                'channel_id': data.get('channel_id', ''),
                'duration': data.get('duration', ''),
                'category_id': data.get('category_id', ''),
                'tags': data.get('tags', []),
                'thumbnail_url': data.get('thumbnail_url', '')
            }
        }
    
    def _process_twitter_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process Twitter-specific data"""
        return {
            'id': data['id'],
            'platform': 'twitter',
            'title': '',  # Twitter doesn't have titles
            'content': data.get('text', ''),
            'author': data.get('author_id', ''),
            'community': 'twitter',
            'score': data.get('like_count', 0),
            'engagement': {
                'retweets': data.get('retweet_count', 0),
                'likes': data.get('like_count', 0),
                'replies': data.get('reply_count', 0),
                'quotes': data.get('quote_count', 0)
            },
            'created_at': datetime.fromisoformat(data.get('created_at', '').replace('Z', '+00:00')),
            'url': f"https://twitter.com/i/status/{data['id']}",
            'metadata': {
                'author_id': data.get('author_id', ''),
                'context_annotations': data.get('context_annotations', [])
            }
        }
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        hashtag_pattern = r'#\w+'
        return re.findall(hashtag_pattern, text)
    
    def extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text"""
        mention_pattern = r'@\w+'
        return re.findall(mention_pattern, text)
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        return text.strip()
```

---

# Rate Limiting

## API Rate Management

```python
# src/services/rate_limiter.py
import asyncio
import time
from typing import Dict, Any
from datetime import datetime, timedelta
import redis

class RateLimiter:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.rate_limits = {
            'reddit': {'requests': 100, 'window': 3600},  # 100 requests per hour
            'youtube': {'requests': 10000, 'window': 3600},  # 10000 requests per hour
            'twitter': {'requests': 300, 'window': 900},  # 300 requests per 15 minutes
            'linkedin': {'requests': 100, 'window': 3600},  # 100 requests per hour
        }
    
    async def check_rate_limit(self, platform: str) -> bool:
        """Check if we can make a request to the platform"""
        key = f"rate_limit:{platform}"
        limits = self.rate_limits.get(platform, {'requests': 100, 'window': 3600})
        
        current_time = int(time.time())
        window_start = current_time - limits['window']
        
        # Remove old entries
        self.redis_client.zremrangebyscore(key, 0, window_start)
        
        # Count current requests
        current_requests = self.redis_client.zcard(key)
        
        if current_requests >= limits['requests']:
            return False
        
        # Add current request
        self.redis_client.zadd(key, {str(current_time): current_time})
        self.redis_client.expire(key, limits['window'])
        
        return True
    
    async def wait_for_rate_limit(self, platform: str) -> None:
        """Wait until rate limit allows a request"""
        while not await self.check_rate_limit(platform):
            await asyncio.sleep(1)
    
    def get_rate_limit_status(self, platform: str) -> Dict[str, Any]:
        """Get current rate limit status for a platform"""
        key = f"rate_limit:{platform}"
        limits = self.rate_limits.get(platform, {'requests': 100, 'window': 3600})
        
        current_requests = self.redis_client.zcard(key)
        remaining = max(0, limits['requests'] - current_requests)
        
        return {
            'platform': platform,
            'current_requests': current_requests,
            'limit': limits['requests'],
            'remaining': remaining,
            'window_seconds': limits['window']
        }
```

---

# Background Processing

## Celery Workers

```python
# src/workers/collector.py
from celery import Celery
from typing import Dict, Any, List
import asyncio
from src.connectors.reddit import RedditConnector
from src.connectors.youtube import YouTubeConnector
from src.connectors.twitter import TwitterConnector
from src.services.data_processor import DataProcessor
from src.services.rate_limiter import RateLimiter

app = Celery('social_media_collector')

@app.task
def collect_reddit_data(query: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Collect Reddit data for a query"""
    async def _collect():
        connector = RedditConnector(
            client_id="your_client_id",
            client_secret="your_client_secret",
            user_agent="FastOpp Data Collector"
        )
        
        rate_limiter = RateLimiter()
        await rate_limiter.wait_for_rate_limit('reddit')
        
        posts = await connector.search_posts(query, limit)
        processor = DataProcessor()
        
        normalized_posts = []
        for post in posts:
            normalized = processor.normalize_post(post, 'reddit')
            normalized_posts.append(normalized)
        
        return normalized_posts
    
    return asyncio.run(_collect())

@app.task
def collect_youtube_data(query: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Collect YouTube data for a query"""
    async def _collect():
        connector = YouTubeConnector(api_key="your_api_key")
        
        rate_limiter = RateLimiter()
        await rate_limiter.wait_for_rate_limit('youtube')
        
        videos = await connector.search_videos(query, limit)
        processor = DataProcessor()
        
        normalized_videos = []
        for video in videos:
            normalized = processor.normalize_post(video, 'youtube')
            normalized_videos.append(normalized)
        
        return normalized_videos
    
    return asyncio.run(_collect())

@app.task
def collect_twitter_data(query: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Collect Twitter data for a query"""
    async def _collect():
        connector = TwitterConnector(bearer_token="your_bearer_token")
        
        rate_limiter = RateLimiter()
        await rate_limiter.wait_for_rate_limit('twitter')
        
        tweets = await connector.search_tweets(query, limit)
        processor = DataProcessor()
        
        normalized_tweets = []
        for tweet in tweets:
            normalized = processor.normalize_post(tweet, 'twitter')
            normalized_tweets.append(normalized)
        
        return normalized_tweets
    
    return asyncio.run(_collect())

@app.task
def collect_all_platforms(query: str, limit: int = 100) -> Dict[str, List[Dict[str, Any]]]:
    """Collect data from all platforms"""
    results = {}
    
    # Collect from all platforms in parallel
    reddit_task = collect_reddit_data.delay(query, limit)
    youtube_task = collect_youtube_data.delay(query, limit)
    twitter_task = collect_twitter_data.delay(query, limit)
    
    results['reddit'] = reddit_task.get()
    results['youtube'] = youtube_task.get()
    results['twitter'] = twitter_task.get()
    
    return results
```

---

# API Endpoints

## FastAPI Integration

```python
# src/api/endpoints.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from src.workers.collector import collect_all_platforms, collect_reddit_data
from src.services.rate_limiter import RateLimiter

router = APIRouter()
rate_limiter = RateLimiter()

class SearchRequest(BaseModel):
    query: str
    limit: int = 100
    platforms: Optional[List[str]] = None

class SearchResponse(BaseModel):
    query: str
    total_results: int
    platforms: Dict[str, int]
    data: Dict[str, List[Dict[str, Any]]]

@router.post("/search", response_model=SearchResponse)
async def search_social_media(request: SearchRequest, background_tasks: BackgroundTasks):
    """Search across multiple social media platforms"""
    try:
        # Check rate limits for all platforms
        for platform in request.platforms or ['reddit', 'youtube', 'twitter']:
            if not await rate_limiter.check_rate_limit(platform):
                raise HTTPException(
                    status_code=429, 
                    detail=f"Rate limit exceeded for {platform}"
                )
        
        # Collect data from all platforms
        results = collect_all_platforms.delay(request.query, request.limit).get()
        
        # Calculate totals
        total_results = sum(len(platform_data) for platform_data in results.values())
        platform_counts = {platform: len(data) for platform, data in results.items()}
        
        return SearchResponse(
            query=request.query,
            total_results=total_results,
            platforms=platform_counts,
            data=results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rate-limits")
async def get_rate_limits():
    """Get current rate limit status for all platforms"""
    status = {}
    for platform in ['reddit', 'youtube', 'twitter', 'linkedin']:
        status[platform] = rate_limiter.get_rate_limit_status(platform)
    
    return status

@router.get("/platforms/{platform}/search")
async def search_single_platform(platform: str, query: str, limit: int = 100):
    """Search a single platform"""
    if platform not in ['reddit', 'youtube', 'twitter']:
        raise HTTPException(status_code=400, detail="Unsupported platform")
    
    if not await rate_limiter.check_rate_limit(platform):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        if platform == 'reddit':
            results = collect_reddit_data.delay(query, limit).get()
        elif platform == 'youtube':
            results = collect_youtube_data.delay(query, limit).get()
        elif platform == 'twitter':
            results = collect_twitter_data.delay(query, limit).get()
        
        return {
            'platform': platform,
            'query': query,
            'results': results,
            'count': len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

# Testing

## Comprehensive Test Suite

```python
# tests/test_connectors.py
import pytest
from unittest.mock import Mock, patch
from src.connectors.reddit import RedditConnector
from src.connectors.youtube import YouTubeConnector
from src.connectors.twitter import TwitterConnector

class TestRedditConnector:
    @pytest.fixture
    def reddit_connector(self):
        return RedditConnector(
            client_id="test_client_id",
            client_secret="test_client_secret",
            user_agent="test_user_agent"
        )
    
    @patch('praw.Reddit')
    async def test_authenticate_success(self, mock_reddit, reddit_connector):
        mock_reddit_instance = Mock()
        mock_reddit_instance.user.me.return_value = Mock()
        mock_reddit.return_value = mock_reddit_instance
        
        result = await reddit_connector.authenticate()
        assert result is True
    
    @patch('praw.Reddit')
    async def test_authenticate_failure(self, mock_reddit, reddit_connector):
        mock_reddit.side_effect = Exception("Authentication failed")
        
        result = await reddit_connector.authenticate()
        assert result is False
    
    @patch('praw.Reddit')
    async def test_search_posts(self, mock_reddit, reddit_connector):
        # Mock Reddit instance
        mock_reddit_instance = Mock()
        mock_subreddit = Mock()
        mock_post = Mock()
        mock_post.id = "test_id"
        mock_post.title = "Test Post"
        mock_post.selftext = "Test content"
        mock_post.author = "test_author"
        mock_post.subreddit = "test_subreddit"
        mock_post.score = 100
        mock_post.upvote_ratio = 0.95
        mock_post.num_comments = 50
        mock_post.created_utc = 1640995200
        mock_post.url = "https://reddit.com/test"
        mock_post.permalink = "/r/test/comments/test_id/"
        mock_post.is_self = True
        mock_post.over_18 = False
        mock_post.stickied = False
        mock_post.total_awards_received = 5
        mock_post.link_flair_text = "Discussion"
        
        mock_subreddit.search.return_value = [mock_post]
        mock_reddit_instance.subreddit.return_value = mock_subreddit
        mock_reddit.return_value = mock_reddit_instance
        
        reddit_connector.reddit = mock_reddit_instance
        
        results = await reddit_connector.search_posts("test query", 10)
        
        assert len(results) == 1
        assert results[0]['id'] == "test_id"
        assert results[0]['title'] == "Test Post"
        assert results[0]['platform'] == 'reddit'

class TestYouTubeConnector:
    @pytest.fixture
    def youtube_connector(self):
        return YouTubeConnector(api_key="test_api_key")
    
    @patch('googleapiclient.discovery.build')
    async def test_authenticate_success(self, mock_build, youtube_connector):
        mock_youtube = Mock()
        mock_request = Mock()
        mock_request.execute.return_value = {}
        mock_youtube.channels.return_value.list.return_value = mock_request
        mock_build.return_value = mock_youtube
        
        result = await youtube_connector.authenticate()
        assert result is True
    
    @patch('googleapiclient.discovery.build')
    async def test_search_videos(self, mock_build, youtube_connector):
        mock_youtube = Mock()
        mock_search_response = {
            'items': [{'id': {'videoId': 'test_video_id'}}]
        }
        mock_video_response = {
            'items': [{
                'id': 'test_video_id',
                'snippet': {
                    'title': 'Test Video',
                    'description': 'Test description',
                    'channelId': 'test_channel_id',
                    'channelTitle': 'Test Channel',
                    'publishedAt': '2024-01-01T00:00:00Z',
                    'categoryId': '22',
                    'tags': ['test', 'video'],
                    'thumbnails': {'high': {'url': 'https://example.com/thumb.jpg'}}
                },
                'statistics': {
                    'viewCount': '1000',
                    'likeCount': '100',
                    'dislikeCount': '10',
                    'commentCount': '50'
                },
                'contentDetails': {'duration': 'PT5M30S'}
            }]
        }
        
        mock_youtube.search.return_value.list.return_value.execute.return_value = mock_search_response
        mock_youtube.videos.return_value.list.return_value.execute.return_value = mock_video_response
        mock_build.return_value = mock_youtube
        
        youtube_connector.youtube = mock_youtube
        
        results = await youtube_connector.search_videos("test query", 10)
        
        assert len(results) == 1
        assert results[0]['id'] == 'test_video_id'
        assert results[0]['title'] == 'Test Video'
        assert results[0]['platform'] == 'youtube'
```

---

# Success Criteria

## Must-Have Features

- [ ] **Multi-Platform Integration** - Connect to Reddit, YouTube, and Twitter
- [ ] **Rate Limiting** - Respect API limits and implement proper throttling
- [ ] **Data Normalization** - Standardize data from different platforms
- [ ] **Error Handling** - Robust error handling and retry logic
- [ ] **Background Processing** - Use Celery for async data collection
- [ ] **API Endpoints** - RESTful API for data access
- [ ] **Data Validation** - Ensure data quality and consistency
- [ ] **Comprehensive Testing** - Unit tests and integration tests

---

# Bonus Challenges

## Advanced Features

- [ ] **Real-time Streaming** - WebSocket connections for live data
- [ ] **Data Caching** - Redis caching for improved performance
- [ ] **Sentiment Analysis** - Analyze sentiment of collected content
- [ ] **Trend Detection** - Identify trending topics and hashtags
- [ ] **User Profiling** - Build comprehensive user profiles
- [ ] **Content Recommendation** - Recommend relevant content to users
- [ ] **Data Visualization** - Create dashboards for data insights
- [ ] **Machine Learning** - Use ML for content classification and analysis

---

# Getting Started

## Setup Instructions

1. **Get API Keys** - Register for Reddit, YouTube, and Twitter APIs
2. **Set up environment** - Install required packages and dependencies
3. **Configure Redis** - Set up Redis for rate limiting and caching
4. **Set up Celery** - Configure background task processing
5. **Implement connectors** - Start with one platform, then expand
6. **Add data processing** - Normalize and clean collected data
7. **Build API endpoints** - Create RESTful API for data access
8. **Add testing** - Write comprehensive tests for all components

---

# Dependencies

## requirements.txt

```txt
praw>=7.7.0
google-api-python-client>=2.100.0
tweepy>=4.14.0
fastapi>=0.100.0
celery>=5.3.0
redis>=4.6.0
aiohttp>=3.8.0
pandas>=2.0.0
pydantic>=2.0.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

---

# Resources

## Helpful Links

- **PRAW Documentation** - https://praw.readthedocs.io/
- **YouTube Data API** - https://developers.google.com/youtube/v3
- **Twitter API v2** - https://developer.twitter.com/en/docs/twitter-api
- **Celery** - https://docs.celeryproject.org/
- **Redis** - https://redis.io/docs/
- **FastAPI** - https://fastapi.tiangolo.com/

---

# Let's Connect to Social Media!

## Ready to Start?

**This assignment will teach you:**
- API integration and authentication
- Rate limiting and error handling
- Data normalization and processing
- Background task processing
- Real-time data collection
- Social media data analysis

**Start with one platform and build up to a comprehensive social media integration system!**

---

# Next Steps

## After Completing This Assignment

1. **Deploy your system** - Set up production infrastructure
2. **Monitor performance** - Track API usage and system performance
3. **Share your insights** - Document your findings and learnings
4. **Contribute to open source** - Share your connectors with the community
5. **Move to the next track** - Try advanced search algorithms or machine learning next!

**Happy social media integration! 🚀**
