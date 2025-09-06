#!/usr/bin/env python3
"""
Script to add sample messages for testing the conversation browser functionality
Fixed version with proper content matching conversation titles
"""

import asyncio
import uuid
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from datetime import timedelta
from db import AsyncSessionLocal
from models import Message, Conversation
from sqlmodel import select


async def add_sample_messages():
    """Add sample messages to existing conversations"""
    
    async with AsyncSessionLocal() as session:
        # Get all existing conversations
        conversations_result = await session.execute(select(Conversation))
        conversations = conversations_result.scalars().all()
        
        if not conversations:
            print("❌ No conversations found. Please run add_sample_conversations.py first.")
            return
        
        # Create appropriate messages for each conversation based on its title
        sample_messages = []
        
        for i, conv in enumerate(conversations):
            conv_id = conv.id
            base_time = conv.created_at
            
            # Create messages based on conversation title
            if "Sony AI Developer Community Strategy" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We need to develop a comprehensive strategy for Sony's AI developer community in the US market. What are the key components we should focus on?",
                        "raw_content": "We need to develop a comprehensive strategy for Sony's AI developer community in the US market. What are the key components we should focus on?",
                        "model": "gpt-4",
                        "token_count": 35,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant", 
                        "content": "For Sony's AI developer community strategy in the US market, I recommend focusing on these key components:\n\n**1. Technical Content & Documentation**\n- Comprehensive API documentation for Sony's AI/ML platforms\n- Interactive tutorials and code examples\n- Video content featuring real-world use cases\n- Technical blog posts by Sony engineers and external developers\n\n**2. Developer Tools & SDKs**\n- Easy-to-use SDKs for major programming languages (Python, JavaScript, C++)\n- Cloud-based development environments\n- Integration with popular AI/ML frameworks (TensorFlow, PyTorch)\n- Performance optimization tools and debugging utilities\n\n**3. Community Building**\n- Developer forums and Discord/Slack communities\n- Regular virtual meetups and hackathons\n- Partner with US universities and coding bootcamps\n- Developer ambassador program with key influencers",
                        "raw_content": "For Sony's AI developer community strategy in the US market, I recommend focusing on these key components:\n\n**1. Technical Content & Documentation**\n- Comprehensive API documentation for Sony's AI/ML platforms\n- Interactive tutorials and code examples\n- Video content featuring real-world use cases\n- Technical blog posts by Sony engineers and external developers\n\n**2. Developer Tools & SDKs**\n- Easy-to-use SDKs for major programming languages (Python, JavaScript, C++)\n- Cloud-based development environments\n- Integration with popular AI/ML frameworks (TensorFlow, PyTorch)\n- Performance optimization tools and debugging utilities\n\n**3. Community Building**\n- Developer forums and Discord/Slack communities\n- Regular virtual meetups and hackathons\n- Partner with US universities and coding bootcamps\n- Developer ambassador program with key influencers",
                        "model": "gpt-4",
                        "token_count": 280,
                        "created_at": base_time + timedelta(minutes=2)
                    }
                ])
            
            elif "Intel AI/ML Hardware Influencer Marketing" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We're launching Intel's AI/ML hardware influencer marketing campaign in the US. What's our strategy for reaching data scientists and AI developers?",
                        "raw_content": "We're launching Intel's AI/ML hardware influencer marketing campaign in the US. What's our strategy for reaching data scientists and AI developers?",
                        "model": "gpt-4",
                        "token_count": 30,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For Intel's AI/ML hardware influencer marketing campaign targeting US data scientists and AI developers, here's a comprehensive strategy:\n\n**1. Target Influencer Categories**\n\n**Academic & Research Influencers:**\n- **Andrew Ng** - Stanford professor, Coursera founder, massive AI education reach\n- **Yann LeCun** - NYU professor, Meta AI chief, deep learning pioneer\n- **Fei-Fei Li** - Stanford professor, AI4ALL founder, computer vision expert\n\n**Technical Content Creators:**\n- **sentdex** - Python programming and AI tutorials (1M+ subscribers)\n- **Two Minute Papers** - AI research explained (2M+ subscribers)\n- **3Blue1Brown** - Mathematical explanations of AI concepts (4M+ subscribers)\n\n**2. Content Strategy**\n- **Technical Deep Dives**: Performance benchmarks of Intel AI hardware\n- **Educational Content**: How Intel's AI acceleration works\n- **Case Studies**: Real-world AI applications using Intel hardware\n- **Tutorial Series**: Building AI models with Intel tools",
                        "raw_content": "For Intel's AI/ML hardware influencer marketing campaign targeting US data scientists and AI developers, here's a comprehensive strategy:\n\n**1. Target Influencer Categories**\n\n**Academic & Research Influencers:**\n- **Andrew Ng** - Stanford professor, Coursera founder, massive AI education reach\n- **Yann LeCun** - NYU professor, Meta AI chief, deep learning pioneer\n- **Fei-Fei Li** - Stanford professor, AI4ALL founder, computer vision expert\n\n**Technical Content Creators:**\n- **sentdex** - Python programming and AI tutorials (1M+ subscribers)\n- **Two Minute Papers** - AI research explained (2M+ subscribers)\n- **3Blue1Brown** - Mathematical explanations of AI concepts (4M+ subscribers)\n\n**2. Content Strategy**\n- **Technical Deep Dives**: Performance benchmarks of Intel AI hardware\n- **Educational Content**: How Intel's AI acceleration works\n- **Case Studies**: Real-world AI applications using Intel hardware\n- **Tutorial Series**: Building AI models with Intel tools",
                        "model": "gpt-4",
                        "token_count": 280,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "AMD Developer Documentation Strategy" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "AMD needs to improve their developer documentation and SDKs for AI/ML workloads. What specific areas should we focus on for the US developer market?",
                        "raw_content": "AMD needs to improve their developer documentation and SDKs for AI/ML workloads. What specific areas should we focus on for the US developer market?",
                        "model": "gpt-4",
                        "token_count": 28,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For AMD's developer documentation and SDK improvements targeting the US AI/ML market, focus on these key areas:\n\n**1. ROCm Documentation Overhaul**\n- Clear getting-started guides for AI/ML frameworks\n- Performance tuning guides for different GPU models\n- Troubleshooting sections for common issues\n- Code examples for popular use cases\n\n**2. SDK Improvements**\n- Better Python bindings for ROCm\n- Integration examples with PyTorch, TensorFlow, and JAX\n- Performance profiling tools and documentation\n- Cross-platform compatibility guides\n\n**3. Developer Experience**\n- Interactive tutorials and Jupyter notebooks\n- Video content for complex setup procedures\n- Community-driven examples and best practices\n- Regular updates and changelog documentation",
                        "raw_content": "For AMD's developer documentation and SDK improvements targeting the US AI/ML market, focus on these key areas:\n\n**1. ROCm Documentation Overhaul**\n- Clear getting-started guides for AI/ML frameworks\n- Performance tuning guides for different GPU models\n- Troubleshooting sections for common issues\n- Code examples for popular use cases\n\n**2. SDK Improvements**\n- Better Python bindings for ROCm\n- Integration examples with PyTorch, TensorFlow, and JAX\n- Performance profiling tools and documentation\n- Cross-platform compatibility guides\n\n**3. Developer Experience**\n- Interactive tutorials and Jupyter notebooks\n- Video content for complex setup procedures\n- Community-driven examples and best practices\n- Regular updates and changelog documentation",
                        "model": "gpt-4",
                        "token_count": 250,
                        "created_at": base_time + timedelta(minutes=4)
                    }
                ])
            
            elif "Rapidus 2nm Technology" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "Rapidus is planning to enter the US market with their 2nm semiconductor technology. What's our go-to-market strategy for reaching US tech companies?",
                        "raw_content": "Rapidus is planning to enter the US market with their 2nm semiconductor technology. What's our go-to-market strategy for reaching US tech companies?",
                        "model": "gpt-4",
                        "token_count": 32,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For Rapidus's 2nm technology US market entry, here's a comprehensive go-to-market strategy:\n\n**1. Target Market Segments**\n- **AI/ML Companies**: NVIDIA, AMD, Intel competitors\n- **Cloud Providers**: AWS, Google Cloud, Microsoft Azure\n- **Automotive**: Tesla, Ford, GM for autonomous driving chips\n- **Mobile**: Apple, Samsung for next-gen processors\n\n**2. Partnership Strategy**\n- Establish design partnerships with major US chip designers\n- Collaborate with US universities on research projects\n- Partner with US-based foundry customers\n- Work with US government on strategic semiconductor initiatives\n\n**3. Market Entry Approach**\n- Open US engineering and sales offices\n- Participate in major US semiconductor conferences\n- Establish relationships with US supply chain partners\n- Focus on advanced packaging and 3D integration capabilities",
                        "raw_content": "For Rapidus's 2nm technology US market entry, here's a comprehensive go-to-market strategy:\n\n**1. Target Market Segments**\n- **AI/ML Companies**: NVIDIA, AMD, Intel competitors\n- **Cloud Providers**: AWS, Google Cloud, Microsoft Azure\n- **Automotive**: Tesla, Ford, GM for autonomous driving chips\n- **Mobile**: Apple, Samsung for next-gen processors\n\n**2. Partnership Strategy**\n- Establish design partnerships with major US chip designers\n- Collaborate with US universities on research projects\n- Partner with US-based foundry customers\n- Work with US government on strategic semiconductor initiatives\n\n**3. Market Entry Approach**\n- Open US engineering and sales offices\n- Participate in major US semiconductor conferences\n- Establish relationships with US supply chain partners\n- Focus on advanced packaging and 3D integration capabilities",
                        "model": "gpt-4",
                        "token_count": 280,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Healthcare Vertical" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We need to create AI-generated technical content for the healthcare vertical. What types of content would be most valuable for healthcare AI developers?",
                        "raw_content": "We need to create AI-generated technical content for the healthcare vertical. What types of content would be most valuable for healthcare AI developers?",
                        "model": "gpt-4",
                        "token_count": 30,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For AI-generated technical content targeting healthcare AI developers, focus on these high-value content types:\n\n**1. Regulatory Compliance Content**\n- HIPAA compliance guides for AI systems\n- FDA approval processes for AI medical devices\n- Data privacy best practices for healthcare AI\n- Security frameworks for medical AI applications\n\n**2. Technical Implementation Guides**\n- Medical image analysis with computer vision\n- Natural language processing for clinical notes\n- Predictive analytics for patient outcomes\n- Integration with EHR systems (Epic, Cerner)\n\n**3. Use Case Documentation**\n- Radiology AI applications and implementation\n- Drug discovery and molecular modeling\n- Clinical decision support systems\n- Telemedicine and remote monitoring solutions\n\n**4. Industry-Specific Resources**\n- Healthcare AI ethics and bias considerations\n- Performance benchmarks for medical AI models\n- Case studies from successful healthcare AI deployments",
                        "raw_content": "For AI-generated technical content targeting healthcare AI developers, focus on these high-value content types:\n\n**1. Regulatory Compliance Content**\n- HIPAA compliance guides for AI systems\n- FDA approval processes for AI medical devices\n- Data privacy best practices for healthcare AI\n- Security frameworks for medical AI applications\n\n**2. Technical Implementation Guides**\n- Medical image analysis with computer vision\n- Natural language processing for clinical notes\n- Predictive analytics for patient outcomes\n- Integration with EHR systems (Epic, Cerner)\n\n**3. Use Case Documentation**\n- Radiology AI applications and implementation\n- Drug discovery and molecular modeling\n- Clinical decision support systems\n- Telemedicine and remote monitoring solutions\n\n**4. Industry-Specific Resources**\n- Healthcare AI ethics and bias considerations\n- Performance benchmarks for medical AI models\n- Case studies from successful healthcare AI deployments",
                        "model": "gpt-4",
                        "token_count": 320,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Canon AI Imaging Solutions" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "Canon wants to reach developers working on AI imaging solutions. What's our strategy for engaging the computer vision and image processing developer community?",
                        "raw_content": "Canon wants to reach developers working on AI imaging solutions. What's our strategy for engaging the computer vision and image processing developer community?",
                        "model": "gpt-4",
                        "token_count": 35,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For Canon's AI imaging solutions developer outreach, here's a targeted strategy:\n\n**1. Developer Community Engagement**\n- Sponsor computer vision conferences (CVPR, ICCV, ECCV)\n- Partner with OpenCV and other imaging libraries\n- Create developer challenges and hackathons\n- Establish partnerships with AI/ML bootcamps\n\n**2. Technical Content Strategy**\n- Camera API documentation and SDKs\n- Image quality optimization guides\n- Real-time processing tutorials\n- Integration examples with popular AI frameworks\n\n**3. Hardware-Software Integration**\n- Showcase Canon's sensor technology advantages\n- Provide development kits for AI imaging projects\n- Create benchmarks comparing Canon vs competitors\n- Offer technical support for developer projects",
                        "raw_content": "For Canon's AI imaging solutions developer outreach, here's a targeted strategy:\n\n**1. Developer Community Engagement**\n- Sponsor computer vision conferences (CVPR, ICCV, ECCV)\n- Partner with OpenCV and other imaging libraries\n- Create developer challenges and hackathons\n- Establish partnerships with AI/ML bootcamps\n\n**2. Technical Content Strategy**\n- Camera API documentation and SDKs\n- Image quality optimization guides\n- Real-time processing tutorials\n- Integration examples with popular AI frameworks\n\n**3. Hardware-Software Integration**\n- Showcase Canon's sensor technology advantages\n- Provide development kits for AI imaging projects\n- Create benchmarks comparing Canon vs competitors\n- Offer technical support for developer projects",
                        "model": "gpt-4",
                        "token_count": 280,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Ricoh B2B AI Solutions" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "Ricoh is planning B2B AI solutions events in the US. What types of events would best showcase their AI capabilities to enterprise customers?",
                        "raw_content": "Ricoh is planning B2B AI solutions events in the US. What types of events would best showcase their AI capabilities to enterprise customers?",
                        "model": "gpt-4",
                        "token_count": 32,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For Ricoh's B2B AI solutions events in the US, consider these event types:\n\n**1. Industry-Specific Events**\n- Healthcare AI solutions showcase\n- Financial services automation demos\n- Manufacturing AI integration workshops\n- Legal document processing seminars\n\n**2. Technology Demonstration Events**\n- Live AI document processing demos\n- Workflow automation showcases\n- Integration with existing enterprise systems\n- ROI calculator presentations\n\n**3. Partner and Customer Events**\n- Executive roundtables on AI adoption\n- Customer success story presentations\n- Partner ecosystem showcases\n- Technical deep-dive sessions for IT teams",
                        "raw_content": "For Ricoh's B2B AI solutions events in the US, consider these event types:\n\n**1. Industry-Specific Events**\n- Healthcare AI solutions showcase\n- Financial services automation demos\n- Manufacturing AI integration workshops\n- Legal document processing seminars\n\n**2. Technology Demonstration Events**\n- Live AI document processing demos\n- Workflow automation showcases\n- Integration with existing enterprise systems\n- ROI calculator presentations\n\n**3. Partner and Customer Events**\n- Executive roundtables on AI adoption\n- Customer success story presentations\n- Partner ecosystem showcases\n- Technical deep-dive sessions for IT teams",
                        "model": "gpt-4",
                        "token_count": 250,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Conference & Meetup Planning" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We're planning US AI/ML conferences and meetups. What are the key events we should target for our Japanese tech clients?",
                        "raw_content": "We're planning US AI/ML conferences and meetups. What are the key events we should target for our Japanese tech clients?",
                        "model": "gpt-4",
                        "token_count": 28,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For US AI/ML conference and meetup planning targeting Japanese tech clients, focus on these key events:\n\n**1. Major AI/ML Conferences**\n- **NeurIPS** (Neural Information Processing Systems)\n- **ICML** (International Conference on Machine Learning)\n- **ICLR** (International Conference on Learning Representations)\n- **AAAI** (Association for the Advancement of Artificial Intelligence)\n\n**2. Industry-Specific Events**\n- **GTC** (NVIDIA GPU Technology Conference)\n- **Strata Data Conference**\n- **O'Reilly AI Conference**\n- **AI DevCon**\n\n**3. Regional Meetups**\n- Silicon Valley AI meetups\n- New York AI/ML groups\n- Boston AI community events\n- Austin tech meetups\n\n**4. Japanese-US Bridge Events**\n- Japan-US AI collaboration summits\n- Bilingual technical meetups\n- Cultural exchange tech events",
                        "raw_content": "For US AI/ML conference and meetup planning targeting Japanese tech clients, focus on these key events:\n\n**1. Major AI/ML Conferences**\n- **NeurIPS** (Neural Information Processing Systems)\n- **ICML** (International Conference on Machine Learning)\n- **ICLR** (International Conference on Learning Representations)\n- **AAAI** (Association for the Advancement of Artificial Intelligence)\n\n**2. Industry-Specific Events**\n- **GTC** (NVIDIA GPU Technology Conference)\n- **Strata Data Conference**\n- **O'Reilly AI Conference**\n- **AI DevCon**\n\n**3. Regional Meetups**\n- Silicon Valley AI meetups\n- New York AI/ML groups\n- Boston AI community events\n- Austin tech meetups\n\n**4. Japanese-US Bridge Events**\n- Japan-US AI collaboration summits\n- Bilingual technical meetups\n- Cultural exchange tech events",
                        "model": "gpt-4",
                        "token_count": 300,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Financial Services AI Content" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We need to create AI content strategy for the financial services vertical. What topics would resonate with fintech and banking AI developers?",
                        "raw_content": "We need to create AI content strategy for the financial services vertical. What topics would resonate with fintech and banking AI developers?",
                        "model": "gpt-4",
                        "token_count": 30,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For financial services AI content strategy, focus on these high-impact topics:\n\n**1. Regulatory Compliance**\n- AI model explainability for regulatory requirements\n- Fair lending and bias detection in AI systems\n- GDPR and data privacy in financial AI\n- Model risk management frameworks\n\n**2. Core Financial AI Applications**\n- Fraud detection and prevention systems\n- Credit scoring and risk assessment\n- Algorithmic trading and market analysis\n- Customer service chatbots and virtual assistants\n\n**3. Technical Implementation**\n- Real-time transaction processing with AI\n- Integration with legacy banking systems\n- High-frequency trading AI infrastructure\n- Secure AI model deployment in financial environments",
                        "raw_content": "For financial services AI content strategy, focus on these high-impact topics:\n\n**1. Regulatory Compliance**\n- AI model explainability for regulatory requirements\n- Fair lending and bias detection in AI systems\n- GDPR and data privacy in financial AI\n- Model risk management frameworks\n\n**2. Core Financial AI Applications**\n- Fraud detection and prevention systems\n- Credit scoring and risk assessment\n- Algorithmic trading and market analysis\n- Customer service chatbots and virtual assistants\n\n**3. Technical Implementation**\n- Real-time transaction processing with AI\n- Integration with legacy banking systems\n- High-frequency trading AI infrastructure\n- Secure AI model deployment in financial environments",
                        "model": "gpt-4",
                        "token_count": 280,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Developer Influencer Partnership" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We want to establish developer influencer partnerships. What's the best approach for building relationships with key developer influencers?",
                        "raw_content": "We want to establish developer influencer partnerships. What's the best approach for building relationships with key developer influencers?",
                        "model": "gpt-4",
                        "token_count": 28,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For building developer influencer partnerships, follow this strategic approach:\n\n**1. Identify and Research Influencers**\n- Analyze GitHub activity and project contributions\n- Review YouTube channels and technical content\n- Check conference speaking engagements\n- Assess social media following and engagement\n\n**2. Relationship Building Strategy**\n- Start with genuine engagement on their content\n- Offer early access to new products/features\n- Provide technical resources and documentation\n- Invite to exclusive developer events\n\n**3. Partnership Models**\n- Sponsored technical content creation\n- Conference speaking opportunities\n- Product advisory roles\n- Open source project collaborations\n\n**4. Long-term Relationship Management**\n- Regular check-ins and feedback sessions\n- Co-creation of technical content\n- Joint community building initiatives\n- Performance tracking and optimization",
                        "raw_content": "For building developer influencer partnerships, follow this strategic approach:\n\n**1. Identify and Research Influencers**\n- Analyze GitHub activity and project contributions\n- Review YouTube channels and technical content\n- Check conference speaking engagements\n- Assess social media following and engagement\n\n**2. Relationship Building Strategy**\n- Start with genuine engagement on their content\n- Offer early access to new products/features\n- Provide technical resources and documentation\n- Invite to exclusive developer events\n\n**3. Partnership Models**\n- Sponsored technical content creation\n- Conference speaking opportunities\n- Product advisory roles\n- Open source project collaborations\n\n**4. Long-term Relationship Management**\n- Regular check-ins and feedback sessions\n- Co-creation of technical content\n- Joint community building initiatives\n- Performance tracking and optimization",
                        "model": "gpt-4",
                        "token_count": 300,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Automotive AI Applications" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We're analyzing automotive AI applications for the US market. What are the key opportunities and challenges for Japanese automotive AI companies?",
                        "raw_content": "We're analyzing automotive AI applications for the US market. What are the key opportunities and challenges for Japanese automotive AI companies?",
                        "model": "gpt-4",
                        "token_count": 32,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For Japanese automotive AI companies entering the US market, here's the analysis:\n\n**1. Key Opportunities**\n- **Autonomous Driving**: Advanced ADAS and self-driving systems\n- **Connected Vehicles**: V2X communication and smart infrastructure\n- **Manufacturing AI**: Quality control and predictive maintenance\n- **Electric Vehicle AI**: Battery management and charging optimization\n\n**2. Market Challenges**\n- **Regulatory Differences**: US vs Japanese safety standards\n- **Competition**: Tesla, Waymo, and established US players\n- **Cultural Adaptation**: US consumer preferences and expectations\n- **Partnership Requirements**: Need for local US partnerships\n\n**3. Strategic Recommendations**\n- Establish US R&D centers and partnerships\n- Focus on specific niches (commercial vehicles, fleet management)\n- Leverage Japanese manufacturing excellence\n- Invest in US regulatory compliance and testing",
                        "raw_content": "For Japanese automotive AI companies entering the US market, here's the analysis:\n\n**1. Key Opportunities**\n- **Autonomous Driving**: Advanced ADAS and self-driving systems\n- **Connected Vehicles**: V2X communication and smart infrastructure\n- **Manufacturing AI**: Quality control and predictive maintenance\n- **Electric Vehicle AI**: Battery management and charging optimization\n\n**2. Market Challenges**\n- **Regulatory Differences**: US vs Japanese safety standards\n- **Competition**: Tesla, Waymo, and established US players\n- **Cultural Adaptation**: US consumer preferences and expectations\n- **Partnership Requirements**: Need for local US partnerships\n\n**3. Strategic Recommendations**\n- Establish US R&D centers and partnerships\n- Focus on specific niches (commercial vehicles, fleet management)\n- Leverage Japanese manufacturing excellence\n- Invest in US regulatory compliance and testing",
                        "model": "gpt-4",
                        "token_count": 320,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Technical Documentation AI Content" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We need to generate technical documentation using AI. What's the best approach for creating high-quality, accurate technical docs?",
                        "raw_content": "We need to generate technical documentation using AI. What's the best approach for creating high-quality, accurate technical docs?",
                        "model": "gpt-4",
                        "token_count": 28,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For AI-generated technical documentation, follow this comprehensive approach:\n\n**1. Content Generation Strategy**\n- Use AI for initial drafts and structure\n- Human review for accuracy and completeness\n- Automated fact-checking against source code\n- Version control integration for documentation\n\n**2. Quality Assurance Process**\n- Technical accuracy validation by engineers\n- User experience testing with target audience\n- Automated grammar and style checking\n- Regular updates based on user feedback\n\n**3. Content Types and Tools**\n- API documentation generation from code comments\n- Tutorial creation with step-by-step guides\n- Troubleshooting guides with common issues\n- Interactive examples and code snippets\n\n**4. Maintenance and Updates**\n- Automated change detection in source code\n- Regular content freshness audits\n- User feedback integration\n- Performance metrics and improvement tracking",
                        "raw_content": "For AI-generated technical documentation, follow this comprehensive approach:\n\n**1. Content Generation Strategy**\n- Use AI for initial drafts and structure\n- Human review for accuracy and completeness\n- Automated fact-checking against source code\n- Version control integration for documentation\n\n**2. Quality Assurance Process**\n- Technical accuracy validation by engineers\n- User experience testing with target audience\n- Automated grammar and style checking\n- Regular updates based on user feedback\n\n**3. Content Types and Tools**\n- API documentation generation from code comments\n- Tutorial creation with step-by-step guides\n- Troubleshooting guides with common issues\n- Interactive examples and code snippets\n\n**4. Maintenance and Updates**\n- Automated change detection in source code\n- Regular content freshness audits\n- User feedback integration\n- Performance metrics and improvement tracking",
                        "model": "gpt-4",
                        "token_count": 300,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "General AI Market Research" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "What are the current trends in the US AI market that Japanese companies should be aware of?",
                        "raw_content": "What are the current trends in the US AI market that Japanese companies should be aware of?",
                        "model": "gpt-4",
                        "token_count": 20,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "Current US AI market trends that Japanese companies should monitor:\n\n**1. Generative AI Boom**\n- ChatGPT and LLM adoption across industries\n- Enterprise AI assistant implementations\n- Content generation and automation tools\n- AI-powered development tools (GitHub Copilot, etc.)\n\n**2. AI Infrastructure Evolution**\n- Cloud AI services dominance (AWS, Azure, GCP)\n- Edge AI and on-device processing growth\n- AI chip specialization and optimization\n- MLOps and AI lifecycle management\n\n**3. Regulatory and Ethical Focus**\n- AI bias and fairness requirements\n- Data privacy and security regulations\n- AI transparency and explainability demands\n- Industry-specific AI governance frameworks\n\n**4. Industry Applications**\n- Healthcare AI for drug discovery and diagnostics\n- Financial services AI for fraud detection\n- Manufacturing AI for quality control\n- Retail AI for personalization and automation",
                        "raw_content": "Current US AI market trends that Japanese companies should monitor:\n\n**1. Generative AI Boom**\n- ChatGPT and LLM adoption across industries\n- Enterprise AI assistant implementations\n- Content generation and automation tools\n- AI-powered development tools (GitHub Copilot, etc.)\n\n**2. AI Infrastructure Evolution**\n- Cloud AI services dominance (AWS, Azure, GCP)\n- Edge AI and on-device processing growth\n- AI chip specialization and optimization\n- MLOps and AI lifecycle management\n\n**3. Regulatory and Ethical Focus**\n- AI bias and fairness requirements\n- Data privacy and security regulations\n- AI transparency and explainability demands\n- Industry-specific AI governance frameworks\n\n**4. Industry Applications**\n- Healthcare AI for drug discovery and diagnostics\n- Financial services AI for fraud detection\n- Manufacturing AI for quality control\n- Retail AI for personalization and automation",
                        "model": "gpt-4",
                        "token_count": 280,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Client Onboarding Process" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "We need to improve our client onboarding process for Japanese companies entering the US market. What should our process include?",
                        "raw_content": "We need to improve our client onboarding process for Japanese companies entering the US market. What should our process include?",
                        "model": "gpt-4",
                        "token_count": 28,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For Japanese companies entering the US market, create a comprehensive onboarding process:\n\n**1. Initial Assessment Phase**\n- Market entry strategy evaluation\n- Competitive landscape analysis\n- Regulatory compliance requirements\n- Cultural and business practice differences\n\n**2. Strategic Planning**\n- Go-to-market strategy development\n- Partnership and channel identification\n- Brand positioning and messaging\n- Budget and timeline planning\n\n**3. Implementation Support**\n- Legal entity setup and compliance\n- Local team building and hiring\n- Marketing and PR campaign launch\n- Sales and distribution channel establishment\n\n**4. Ongoing Support**\n- Performance monitoring and optimization\n- Regular strategy reviews and adjustments\n- Market feedback integration\n- Long-term relationship management",
                        "raw_content": "For Japanese companies entering the US market, create a comprehensive onboarding process:\n\n**1. Initial Assessment Phase**\n- Market entry strategy evaluation\n- Competitive landscape analysis\n- Regulatory compliance requirements\n- Cultural and business practice differences\n\n**2. Strategic Planning**\n- Go-to-market strategy development\n- Partnership and channel identification\n- Brand positioning and messaging\n- Budget and timeline planning\n\n**3. Implementation Support**\n- Legal entity setup and compliance\n- Local team building and hiring\n- Marketing and PR campaign launch\n- Sales and distribution channel establishment\n\n**4. Ongoing Support**\n- Performance monitoring and optimization\n- Regular strategy reviews and adjustments\n- Market feedback integration\n- Long-term relationship management",
                        "model": "gpt-4",
                        "token_count": 280,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
            
            elif "Team Meeting Notes" in conv.title:
                sample_messages.extend([
                    {
                        "conversation_id": conv_id,
                        "role": "user",
                        "content": "Let's discuss our Q4 planning priorities. What should we focus on for the rest of the year?",
                        "raw_content": "Let's discuss our Q4 planning priorities. What should we focus on for the rest of the year?",
                        "model": "gpt-4",
                        "token_count": 20,
                        "created_at": base_time + timedelta(minutes=1)
                    },
                    {
                        "conversation_id": conv_id,
                        "role": "assistant",
                        "content": "For Q4 planning, here are our key priorities:\n\n**1. Client Acquisition**\n- Target 3 new Japanese tech clients\n- Expand existing client relationships\n- Develop case studies and success stories\n- Improve client retention rates\n\n**2. Service Development**\n- Launch AI content generation service\n- Enhance market research capabilities\n- Develop influencer partnership program\n- Create industry-specific service packages\n\n**3. Team and Operations**\n- Hire 2 additional team members\n- Implement new project management tools\n- Establish quality assurance processes\n- Develop training programs for new hires\n\n**4. Market Expansion**\n- Explore opportunities in other Asian markets\n- Develop partnerships with US-based agencies\n- Attend key industry conferences\n- Build thought leadership content",
                        "raw_content": "For Q4 planning, here are our key priorities:\n\n**1. Client Acquisition**\n- Target 3 new Japanese tech clients\n- Expand existing client relationships\n- Develop case studies and success stories\n- Improve client retention rates\n\n**2. Service Development**\n- Launch AI content generation service\n- Enhance market research capabilities\n- Develop influencer partnership program\n- Create industry-specific service packages\n\n**3. Team and Operations**\n- Hire 2 additional team members\n- Implement new project management tools\n- Establish quality assurance processes\n- Develop training programs for new hires\n\n**4. Market Expansion**\n- Explore opportunities in other Asian markets\n- Develop partnerships with US-based agencies\n- Attend key industry conferences\n- Build thought leadership content",
                        "model": "gpt-4",
                        "token_count": 280,
                        "created_at": base_time + timedelta(minutes=3)
                    }
                ])
        
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
