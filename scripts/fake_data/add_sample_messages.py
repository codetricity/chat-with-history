#!/usr/bin/env python3
"""
Script to add sample messages for testing the conversation browser functionality
"""

import asyncio
import uuid
from datetime import timedelta
from db import AsyncSessionLocal
from models import Message, Conversation
from sqlmodel import select


async def add_sample_messages():
    """Add sample messages to existing conversations"""
    
    async with AsyncSessionLocal() as session:
        # Get some existing conversations
        conversations_result = await session.execute(select(Conversation).limit(5))
        conversations = conversations_result.scalars().all()
        
        if not conversations:
            print("❌ No conversations found. Please run add_sample_conversations.py first.")
            return
        
        # Sample message data for different conversations
        sample_messages = [
            # Messages for first conversation (Sony AI Developer Community Strategy)
            {
                "conversation_id": conversations[0].id,
                "role": "user",
                "content": "We need to develop a comprehensive strategy for Sony's AI developer community in the US market. What are the key components we should focus on?",
                "raw_content": "We need to develop a comprehensive strategy for Sony's AI developer community in the US market. What are the key components we should focus on?",
                "model": "gpt-4",
                "token_count": 35,
                "created_at": conversations[0].created_at + timedelta(minutes=1)
            },
            {
                "conversation_id": conversations[0].id,
                "role": "assistant", 
                "content": "For Sony's AI developer community strategy in the US market, I recommend focusing on these key components:\n\n**1. Technical Content & Documentation**\n- Comprehensive API documentation for Sony's AI/ML platforms\n- Interactive tutorials and code examples\n- Video content featuring real-world use cases\n- Technical blog posts by Sony engineers and external developers\n\n**2. Developer Tools & SDKs**\n- Easy-to-use SDKs for major programming languages (Python, JavaScript, C++)\n- Cloud-based development environments\n- Integration with popular AI/ML frameworks (TensorFlow, PyTorch)\n- Performance optimization tools and debugging utilities\n\n**3. Community Building**\n- Developer forums and Discord/Slack communities\n- Regular virtual meetups and hackathons\n- Partner with US universities and coding bootcamps\n- Developer ambassador program with key influencers\n\n**4. Influencer Marketing Strategy**\n- Identify top AI/ML developers and researchers in the US\n- Create technical content partnerships\n- Sponsor conferences like NeurIPS, ICML, and local AI meetups\n- Collaborate with YouTube tech channels and technical bloggers\n\n**5. US Market-Specific Considerations**\n- Focus on gaming and entertainment AI applications\n- Emphasize privacy and data security (important for US market)\n- Highlight real-time performance capabilities\n- Showcase integration with popular US developer tools and platforms",
                "raw_content": "For Sony's AI developer community strategy in the US market, I recommend focusing on these key components:\n\n**1. Technical Content & Documentation**\n- Comprehensive API documentation for Sony's AI/ML platforms\n- Interactive tutorials and code examples\n- Video content featuring real-world use cases\n- Technical blog posts by Sony engineers and external developers\n\n**2. Developer Tools & SDKs**\n- Easy-to-use SDKs for major programming languages (Python, JavaScript, C++)\n- Cloud-based development environments\n- Integration with popular AI/ML frameworks (TensorFlow, PyTorch)\n- Performance optimization tools and debugging utilities\n\n**3. Community Building**\n- Developer forums and Discord/Slack communities\n- Regular virtual meetups and hackathons\n- Partner with US universities and coding bootcamps\n- Developer ambassador program with key influencers\n\n**4. Influencer Marketing Strategy**\n- Identify top AI/ML developers and researchers in the US\n- Create technical content partnerships\n- Sponsor conferences like NeurIPS, ICML, and local AI meetups\n- Collaborate with YouTube tech channels and technical bloggers\n\n**5. US Market-Specific Considerations**\n- Focus on gaming and entertainment AI applications\n- Emphasize privacy and data security (important for US market)\n- Highlight real-time performance capabilities\n- Showcase integration with popular US developer tools and platforms",
                "model": "gpt-4",
                "token_count": 280,
                "created_at": conversations[0].created_at + timedelta(minutes=2)
            },
            {
                "conversation_id": conversations[0].id,
                "role": "user",
                "content": "What specific influencers should we target for Sony's AI gaming technology?",
                "raw_content": "What specific influencers should we target for Sony's AI gaming technology?",
                "model": "gpt-4",
                "token_count": 20,
                "created_at": conversations[0].created_at + timedelta(minutes=5)
            },
            {
                "conversation_id": conversations[0].id,
                "role": "assistant",
                "content": "For Sony's AI gaming technology, I recommend targeting these key influencer categories:\n\n**Technical Gaming Influencers:**\n- **Linus Tech Tips** - Massive reach, focuses on gaming hardware and AI\n- **Digital Foundry** - Deep technical analysis of gaming technology\n- **Gamers Nexus** - Hardware-focused with technical audience\n- **Hardware Unboxed** - GPU and AI performance analysis\n\n**AI/ML Developer Influencers:**\n- **Two Minute Papers** - AI research explained for general audience\n- **sentdex** - Python programming and AI tutorials\n- **3Blue1Brown** - Mathematical explanations of AI concepts\n- **Lex Fridman** - AI researcher with large following\n\n**Gaming Industry Influencers:**\n- **Game Developers Conference (GDC)** speakers\n- **Unity and Unreal Engine** community leaders\n- **Indie game developers** with technical focus\n- **Gaming YouTubers** who create technical content\n\n**Strategy for Each Category:**\n1. **Technical Gaming**: Focus on performance benchmarks, AI-powered features in games\n2. **AI/ML Developers**: Emphasize Sony's AI research, open-source contributions\n3. **Gaming Industry**: Highlight practical applications, developer tools, and SDKs\n\n**Content Collaboration Ideas:**\n- Sponsor technical deep-dives into Sony's AI technology\n- Provide early access to AI gaming features for review\n- Create joint educational content about AI in gaming\n- Host technical workshops and coding sessions",
                "raw_content": "For Sony's AI gaming technology, I recommend targeting these key influencer categories:\n\n**Technical Gaming Influencers:**\n- **Linus Tech Tips** - Massive reach, focuses on gaming hardware and AI\n- **Digital Foundry** - Deep technical analysis of gaming technology\n- **Gamers Nexus** - Hardware-focused with technical audience\n- **Hardware Unboxed** - GPU and AI performance analysis\n\n**AI/ML Developer Influencers:**\n- **Two Minute Papers** - AI research explained for general audience\n- **sentdex** - Python programming and AI tutorials\n- **3Blue1Brown** - Mathematical explanations of AI concepts\n- **Lex Fridman** - AI researcher with large following\n\n**Gaming Industry Influencers:**\n- **Game Developers Conference (GDC)** speakers\n- **Unity and Unreal Engine** community leaders\n- **Indie game developers** with technical focus\n- **Gaming YouTubers** who create technical content\n\n**Strategy for Each Category:**\n1. **Technical Gaming**: Focus on performance benchmarks, AI-powered features in games\n2. **AI/ML Developers**: Emphasize Sony's AI research, open-source contributions\n3. **Gaming Industry**: Highlight practical applications, developer tools, and SDKs\n\n**Content Collaboration Ideas:**\n- Sponsor technical deep-dives into Sony's AI technology\n- Provide early access to AI gaming features for review\n- Create joint educational content about AI in gaming\n- Host technical workshops and coding sessions",
                "model": "gpt-4",
                "token_count": 320,
                "created_at": conversations[0].created_at + timedelta(minutes=7)
            },
            
            # Messages for second conversation (Intel AI/ML Hardware Influencer Marketing)
            {
                "conversation_id": conversations[1].id,
                "role": "user",
                "content": "We're launching Intel's AI/ML hardware influencer marketing campaign in the US. What's our strategy for reaching data scientists and AI developers?",
                "raw_content": "We're launching Intel's AI/ML hardware influencer marketing campaign in the US. What's our strategy for reaching data scientists and AI developers?",
                "model": "gpt-4",
                "token_count": 30,
                "created_at": conversations[1].created_at + timedelta(minutes=1)
            },
            {
                "conversation_id": conversations[1].id,
                "role": "assistant",
                "content": "For Intel's AI/ML hardware influencer marketing campaign targeting US data scientists and AI developers, here's a comprehensive strategy:\n\n**1. Target Influencer Categories**\n\n**Academic & Research Influencers:**\n- **Andrew Ng** - Stanford professor, Coursera founder, massive AI education reach\n- **Yann LeCun** - NYU professor, Meta AI chief, deep learning pioneer\n- **Fei-Fei Li** - Stanford professor, AI4ALL founder, computer vision expert\n- **Anima Anandkumar** - Caltech professor, NVIDIA research director\n\n**Technical Content Creators:**\n- **sentdex** - Python programming and AI tutorials (1M+ subscribers)\n- **Two Minute Papers** - AI research explained (2M+ subscribers)\n- **3Blue1Brown** - Mathematical explanations of AI concepts (4M+ subscribers)\n- **Lex Fridman** - AI researcher with large following (2M+ subscribers)\n\n**Industry Practitioners:**\n- **Jeremy Howard** - fast.ai founder, practical deep learning\n- **Rachel Thomas** - fast.ai co-founder, AI ethics advocate\n- **Cassie Kozyrkov** - Google's Chief Decision Scientist\n- **François Chollet** - Keras creator, Google AI researcher\n\n**2. Content Strategy**\n- **Technical Deep Dives**: Performance benchmarks of Intel AI hardware\n- **Educational Content**: How Intel's AI acceleration works\n- **Case Studies**: Real-world AI applications using Intel hardware\n- **Tutorial Series**: Building AI models with Intel tools\n\n**3. Partnership Approaches**\n- **Research Collaborations**: Fund AI research using Intel hardware\n- **Open Source Projects**: Support popular AI frameworks with Intel optimization\n- **Conference Sponsorships**: NeurIPS, ICML, ICLR, AAAI\n- **University Partnerships**: Provide hardware for AI courses and research\n\n**4. US Market-Specific Tactics**\n- **Silicon Valley Focus**: Target Bay Area AI companies and researchers\n- **Academic Institutions**: Partner with top US universities\n- **Startup Ecosystem**: Engage with AI startups and accelerators\n- **Enterprise AI**: Target Fortune 500 companies implementing AI",
                "raw_content": "For Intel's AI/ML hardware influencer marketing campaign targeting US data scientists and AI developers, here's a comprehensive strategy:\n\n**1. Target Influencer Categories**\n\n**Academic & Research Influencers:**\n- **Andrew Ng** - Stanford professor, Coursera founder, massive AI education reach\n- **Yann LeCun** - NYU professor, Meta AI chief, deep learning pioneer\n- **Fei-Fei Li** - Stanford professor, AI4ALL founder, computer vision expert\n- **Anima Anandkumar** - Caltech professor, NVIDIA research director\n\n**Technical Content Creators:**\n- **sentdex** - Python programming and AI tutorials (1M+ subscribers)\n- **Two Minute Papers** - AI research explained (2M+ subscribers)\n- **3Blue1Brown** - Mathematical explanations of AI concepts (4M+ subscribers)\n- **Lex Fridman** - AI researcher with large following (2M+ subscribers)\n\n**Industry Practitioners:**\n- **Jeremy Howard** - fast.ai founder, practical deep learning\n- **Rachel Thomas** - fast.ai co-founder, AI ethics advocate\n- **Cassie Kozyrkov** - Google's Chief Decision Scientist\n- **François Chollet** - Keras creator, Google AI researcher\n\n**2. Content Strategy**\n- **Technical Deep Dives**: Performance benchmarks of Intel AI hardware\n- **Educational Content**: How Intel's AI acceleration works\n- **Case Studies**: Real-world AI applications using Intel hardware\n- **Tutorial Series**: Building AI models with Intel tools\n\n**3. Partnership Approaches**\n- **Research Collaborations**: Fund AI research using Intel hardware\n- **Open Source Projects**: Support popular AI frameworks with Intel optimization\n- **Conference Sponsorships**: NeurIPS, ICML, ICLR, AAAI\n- **University Partnerships**: Provide hardware for AI courses and research\n\n**4. US Market-Specific Tactics**\n- **Silicon Valley Focus**: Target Bay Area AI companies and researchers\n- **Academic Institutions**: Partner with top US universities\n- **Startup Ecosystem**: Engage with AI startups and accelerators\n- **Enterprise AI**: Target Fortune 500 companies implementing AI",
                "model": "gpt-4",
                "token_count": 280,
                "created_at": conversations[1].created_at + timedelta(minutes=3)
            },
            
            # Messages for third conversation (Client API Requirements)
            {
                "conversation_id": conversations[2].id,
                "role": "user",
                "content": "Our client needs an API that can handle 10,000 requests per minute. What architecture would you recommend?",
                "raw_content": "Our client needs an API that can handle 10,000 requests per minute. What architecture would you recommend?",
                "model": "gpt-4",
                "token_count": 20,
                "created_at": conversations[2].created_at + timedelta(minutes=1)
            },
            {
                "conversation_id": conversations[2].id,
                "role": "assistant",
                "content": "For handling 10,000 requests per minute (~167 RPS), I recommend this architecture:\n\n**Backend Stack:**\n- **FastAPI** with async/await for high concurrency\n- **PostgreSQL** with connection pooling (pgbouncer)\n- **Redis** for caching and session storage\n- **Celery** with Redis broker for background tasks\n\n**Infrastructure:**\n- **Load balancer** (nginx or AWS ALB)\n- **Multiple app instances** behind the load balancer\n- **Database read replicas** for read-heavy operations\n- **CDN** for static content\n\n**Performance optimizations:**\n- Database indexing on frequently queried columns\n- Connection pooling (20-50 connections per instance)\n- Response caching with appropriate TTL\n- Database query optimization\n- Async database operations\n\n**Monitoring:**\n- Application metrics (Prometheus + Grafana)\n- Database performance monitoring\n- Error tracking and logging\n\nThis setup should easily handle your requirements with room for growth.",
                "raw_content": "For handling 10,000 requests per minute (~167 RPS), I recommend this architecture:\n\n**Backend Stack:**\n- **FastAPI** with async/await for high concurrency\n- **PostgreSQL** with connection pooling (pgbouncer)\n- **Redis** for caching and session storage\n- **Celery** with Redis broker for background tasks\n\n**Infrastructure:**\n- **Load balancer** (nginx or AWS ALB)\n- **Multiple app instances** behind the load balancer\n- **Database read replicas** for read-heavy operations\n- **CDN** for static content\n\n**Performance optimizations:**\n- Database indexing on frequently queried columns\n- Connection pooling (20-50 connections per instance)\n- Response caching with appropriate TTL\n- Database query optimization\n- Async database operations\n\n**Monitoring:**\n- Application metrics (Prometheus + Grafana)\n- Database performance monitoring\n- Error tracking and logging\n\nThis setup should easily handle your requirements with room for growth.",
                "model": "gpt-4",
                "token_count": 280,
                "created_at": conversations[2].created_at + timedelta(minutes=4)
            },
            
            # Messages for fourth conversation (Performance Optimization)
            {
                "conversation_id": conversations[3].id,
                "role": "user",
                "content": "My FastAPI app is running slowly. How can I identify and fix performance bottlenecks?",
                "raw_content": "My FastAPI app is running slowly. How can I identify and fix performance bottlenecks?",
                "model": "gpt-4",
                "token_count": 18,
                "created_at": conversations[3].created_at + timedelta(minutes=1)
            },
            {
                "conversation_id": conversations[3].id,
                "role": "assistant",
                "content": "Here's a systematic approach to identify and fix FastAPI performance issues:\n\n**1. Profiling and Monitoring:**\n- Use `py-spy` for CPU profiling\n- Add `time.time()` measurements around slow functions\n- Use FastAPI's built-in middleware for request timing\n- Monitor database query performance\n\n**2. Common Bottlenecks:**\n- **Database queries**: Use `EXPLAIN ANALYZE` on slow queries\n- **N+1 queries**: Implement eager loading or batch queries\n- **Synchronous operations**: Convert to async/await\n- **Memory leaks**: Profile memory usage over time\n\n**3. FastAPI-specific optimizations:**\n- Use async database operations\n- Implement response caching\n- Optimize Pydantic models (use `Config.orm_mode`)\n- Use dependency injection efficiently\n\n**4. Database optimizations:**\n- Add proper indexes\n- Use connection pooling\n- Implement query result caching\n- Consider read replicas for read-heavy workloads\n\n**5. Infrastructure:**\n- Use gunicorn with multiple workers\n- Implement horizontal scaling\n- Use a reverse proxy (nginx)\n- Consider containerization for easy scaling\n\nStart with profiling to identify the specific bottlenecks in your application.",
                "raw_content": "Here's a systematic approach to identify and fix FastAPI performance issues:\n\n**1. Profiling and Monitoring:**\n- Use `py-spy` for CPU profiling\n- Add `time.time()` measurements around slow functions\n- Use FastAPI's built-in middleware for request timing\n- Monitor database query performance\n\n**2. Common Bottlenecks:**\n- **Database queries**: Use `EXPLAIN ANALYZE` on slow queries\n- **N+1 queries**: Implement eager loading or batch queries\n- **Synchronous operations**: Convert to async/await\n- **Memory leaks**: Profile memory usage over time\n\n**3. FastAPI-specific optimizations:**\n- Use async database operations\n- Implement response caching\n- Optimize Pydantic models (use `Config.orm_mode`)\n- Use dependency injection efficiently\n\n**4. Database optimizations:**\n- Add proper indexes\n- Use connection pooling\n- Implement query result caching\n- Consider read replicas for read-heavy workloads\n\n**5. Infrastructure:**\n- Use gunicorn with multiple workers\n- Implement horizontal scaling\n- Use a reverse proxy (nginx)\n- Consider containerization for easy scaling\n\nStart with profiling to identify the specific bottlenecks in your application.",
                "model": "gpt-4",
                "token_count": 320,
                "created_at": conversations[3].created_at + timedelta(minutes=3)
            },
            
            # Messages for fifth conversation (Learning Python Async)
            {
                "conversation_id": conversations[4].id,
                "role": "user",
                "content": "I'm new to Python async programming. Can you explain the basics of async/await?",
                "raw_content": "I'm new to Python async programming. Can you explain the basics of async/await?",
                "model": "gpt-4",
                "token_count": 20,
                "created_at": conversations[4].created_at + timedelta(minutes=1)
            },
            {
                "conversation_id": conversations[4].id,
                "role": "assistant",
                "content": "Async/await in Python allows you to write concurrent code that can handle many operations without blocking. Here's a beginner-friendly explanation:\n\n**Key Concepts:**\n\n1. **`async def`**: Defines an asynchronous function\n2. **`await`**: Pauses execution until the awaited operation completes\n3. **Event loop**: Manages and executes async tasks\n\n**Basic Example:**\n```python\nimport asyncio\nimport aiohttp\n\nasync def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.text()\n\nasync def main():\n    # These run concurrently, not sequentially\n    task1 = fetch_data('https://api.example.com/data1')\n    task2 = fetch_data('https://api.example.com/data2')\n    \n    # Wait for both to complete\n    result1, result2 = await asyncio.gather(task1, task2)\n    print(f'Data 1: {result1[:100]}...')\n    print(f'Data 2: {result2[:100]}...')\n\n# Run the async function\nasyncio.run(main())\n```\n\n**Why use async?**\n- **Non-blocking**: While waiting for I/O (network, file), other tasks can run\n- **Efficient**: Handle thousands of concurrent operations\n- **Perfect for web APIs**: Handle many requests simultaneously\n\n**Common use cases:**\n- Web scraping\n- API calls\n- Database operations\n- File I/O\n- Web servers (like FastAPI)\n\nStart with simple examples and gradually work up to more complex scenarios!",
                "raw_content": "Async/await in Python allows you to write concurrent code that can handle many operations without blocking. Here's a beginner-friendly explanation:\n\n**Key Concepts:**\n\n1. **`async def`**: Defines an asynchronous function\n2. **`await`**: Pauses execution until the awaited operation completes\n3. **Event loop**: Manages and executes async tasks\n\n**Basic Example:**\n```python\nimport asyncio\nimport aiohttp\n\nasync def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.text()\n\nasync def main():\n    # These run concurrently, not sequentially\n    task1 = fetch_data('https://api.example.com/data1')\n    task2 = fetch_data('https://api.example.com/data2')\n    \n    # Wait for both to complete\n    result1, result2 = await asyncio.gather(task1, task2)\n    print(f'Data 1: {result1[:100]}...')\n    print(f'Data 2: {result2[:100]}...')\n\n# Run the async function\nasyncio.run(main())\n```\n\n**Why use async?**\n- **Non-blocking**: While waiting for I/O (network, file), other tasks can run\n- **Efficient**: Handle thousands of concurrent operations\n- **Perfect for web APIs**: Handle many requests simultaneously\n\n**Common use cases:**\n- Web scraping\n- API calls\n- Database operations\n- File I/O\n- Web servers (like FastAPI)\n\nStart with simple examples and gradually work up to more complex scenarios!",
                "model": "gpt-4",
                "token_count": 380,
                "created_at": conversations[4].created_at + timedelta(minutes=3)
            }
        ]
        
        created_messages = []
        
        for msg_data in sample_messages:
            # Check if message already exists (by content and conversation)
            existing = await session.execute(
                select(Message).where(
                    Message.content == msg_data['content'],
                    Message.conversation_id == msg_data['conversation_id']
                )
            )
            if existing.scalar_one_or_none():
                print(f"Message already exists in conversation, skipping...")
                continue
            
            message = Message(
                id=uuid.uuid4(),
                conversation_id=msg_data['conversation_id'],
                role=msg_data['role'],
                content=msg_data['content'],
                raw_content=msg_data['raw_content'],
                model=msg_data['model'],
                token_count=msg_data['token_count'],
                created_at=msg_data['created_at']
            )
            
            session.add(message)
            created_messages.append(message)
            print(f"Added {msg_data['role']} message to conversation")
        
        await session.commit()
        print(f"\n✅ Successfully added {len(created_messages)} sample messages!")
        
        # Show summary by conversation
        print("\nMessages by conversation:")
        for conv in conversations:
            conv_messages = [m for m in created_messages if m.conversation_id == conv.id]
            if conv_messages:
                user_msgs = len([m for m in conv_messages if m.role == 'user'])
                assistant_msgs = len([m for m in conv_messages if m.role == 'assistant'])
                print(f"- {conv.title}: {user_msgs} user + {assistant_msgs} assistant messages")


if __name__ == "__main__":
    asyncio.run(add_sample_messages())
