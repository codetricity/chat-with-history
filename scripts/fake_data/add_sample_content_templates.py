#!/usr/bin/env python3
"""
Script to add sample content templates for the marketing firm system.
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path so we can import from the project
sys.path.append(str(Path(__file__).parent.parent))

from db import AsyncSessionLocal
from models import ContentTemplate
from sqlmodel import select


async def add_sample_templates():
    """Add sample content templates to the database."""
    
    sample_templates = [
        {
            "name": "Blog Post Outline",
            "description": "Generate a comprehensive blog post outline with headings, subheadings, and key points",
            "content_type": "blog_post",
            "template_prompt": """Create a detailed blog post outline for the topic: {topic}

Include:
1. Compelling headline
2. Introduction hook
3. 3-5 main sections with subheadings
4. Key points for each section
5. Call-to-action conclusion
6. SEO keywords to include

Target audience: {audience}
Tone: {tone}
Word count: {word_count}""",
            "variables": json.dumps(["topic", "audience", "tone", "word_count"])
        },
        {
            "name": "Social Media Post",
            "description": "Generate engaging social media posts for various platforms",
            "content_type": "social_media",
            "template_prompt": """Create a {platform} post about: {topic}

Requirements:
- Platform: {platform}
- Tone: {tone}
- Include relevant hashtags
- Add a call-to-action
- Keep within character limits
- Make it engaging and shareable

Brand voice: {brand_voice}
Target audience: {audience}""",
            "variables": json.dumps(["platform", "topic", "tone", "brand_voice", "audience"])
        },
        {
            "name": "Email Newsletter",
            "description": "Create compelling email newsletter content",
            "content_type": "email_marketing",
            "template_prompt": """Create an email newsletter with the following structure:

Subject Line: {subject_line}
From: {sender_name}

Content:
1. Welcome message
2. Main story/article summary
3. Secondary content piece
4. Company updates
5. Call-to-action
6. Footer with contact info

Brand: {brand_name}
Tone: {tone}
Target audience: {audience}
Length: {length}""",
            "variables": json.dumps(["subject_line", "sender_name", "brand_name", "tone", "audience", "length"])
        },
        {
            "name": "Product Description",
            "description": "Generate compelling product descriptions for e-commerce",
            "content_type": "product_description",
            "template_prompt": """Write a product description for: {product_name}

Include:
1. Compelling headline
2. Key features and benefits
3. Technical specifications
4. Use cases and applications
5. Why choose this product
6. Call-to-action

Product category: {category}
Target audience: {audience}
Price point: {price_range}
Tone: {tone}""",
            "variables": json.dumps(["product_name", "category", "audience", "price_range", "tone"])
        },
        {
            "name": "Press Release",
            "description": "Create professional press releases for announcements",
            "content_type": "press_release",
            "template_prompt": """Write a press release for: {announcement}

Structure:
1. Headline
2. Dateline and location
3. Lead paragraph (who, what, when, where, why)
4. Body paragraphs with quotes
5. Company background
6. Contact information

Company: {company_name}
Industry: {industry}
Tone: Professional and newsworthy
Target media: {target_media}""",
            "variables": json.dumps(["announcement", "company_name", "industry", "target_media"])
        },
        {
            "name": "Landing Page Copy",
            "description": "Generate persuasive landing page content",
            "content_type": "landing_page",
            "template_prompt": """Create landing page copy for: {offer}

Include:
1. Headline (H1)
2. Subheadline
3. Value proposition
4. Key benefits (3-5 points)
5. Social proof/testimonials section
6. Call-to-action buttons
7. FAQ section
8. Trust signals

Product/service: {product}
Target audience: {audience}
Goal: {conversion_goal}
Tone: {tone}""",
            "variables": json.dumps(["offer", "product", "audience", "conversion_goal", "tone"])
        },
        {
            "name": "Ad Copy",
            "description": "Create compelling advertising copy for various platforms",
            "content_type": "advertising",
            "template_prompt": """Write ad copy for: {campaign}

Platform: {platform}
Ad format: {ad_format}

Include:
1. Headline (attention-grabbing)
2. Description text
3. Call-to-action
4. Relevant keywords
5. Emotional triggers

Product: {product}
Target audience: {audience}
Campaign goal: {goal}
Budget: {budget}
Tone: {tone}""",
            "variables": json.dumps(["campaign", "platform", "ad_format", "product", "audience", "goal", "budget", "tone"])
        },
        {
            "name": "Case Study",
            "description": "Generate professional case studies showcasing success stories",
            "content_type": "case_study",
            "template_prompt": """Create a case study for: {client_name}

Structure:
1. Executive summary
2. Challenge/problem statement
3. Solution approach
4. Implementation process
5. Results and metrics
6. Client testimonial
7. Key takeaways

Industry: {industry}
Service provided: {service}
Timeline: {timeline}
Results achieved: {results}
Tone: Professional and data-driven""",
            "variables": json.dumps(["client_name", "industry", "service", "timeline", "results"])
        }
    ]
    
    async with AsyncSessionLocal() as session:
        # Check if templates already exist
        existing_templates = await session.execute(select(ContentTemplate))
        existing_count = len(existing_templates.scalars().all())
        
        if existing_count > 0:
            print(f"Found {existing_count} existing templates. Skipping sample data creation.")
            return
        
        print("Adding sample content templates...")
        
        for template_data in sample_templates:
            template = ContentTemplate(**template_data)
            session.add(template)
            print(f"Added template: {template_data['name']}")
        
        await session.commit()
        print(f"Successfully added {len(sample_templates)} content templates!")


async def main():
    """Main function to run the script."""
    try:
        await add_sample_templates()
    except Exception as e:
        print(f"Error adding sample templates: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
