"""
Service for managing content templates
"""
import uuid
import json
from typing import List, Optional, Dict, Any
from sqlmodel import select, Session
from models import ContentTemplate, ContentTemplateCreate, ContentTemplateUpdate


class ContentTemplateService:
    @staticmethod
    async def create_template(session: Session, template_data: ContentTemplateCreate) -> ContentTemplate:
        """Create a new content template"""
        template_dict = template_data.dict()
        if template_dict.get('variables'):
            template_dict['variables'] = json.dumps(template_dict['variables'])
        
        template = ContentTemplate(**template_dict)
        session.add(template)
        await session.commit()
        await session.refresh(template)
        return template

    @staticmethod
    async def get_templates(session: Session, content_type: Optional[str] = None, 
                           skip: int = 0, limit: int = 100) -> List[ContentTemplate]:
        """Get content templates, optionally filtered by type"""
        query = select(ContentTemplate).where(ContentTemplate.is_active == True).offset(skip).limit(limit)
        if content_type:
            query = query.where(ContentTemplate.content_type == content_type)
        
        result = await session.execute(query)
        templates = result.scalars().all()
        return list(templates)

    @staticmethod
    async def get_template(session: Session, template_id: uuid.UUID) -> Optional[ContentTemplate]:
        """Get a specific template by ID"""
        template = await session.get(ContentTemplate, template_id)
        return template if template and template.is_active else None

    @staticmethod
    async def update_template(session: Session, template_id: uuid.UUID, template_data: ContentTemplateUpdate) -> Optional[ContentTemplate]:
        """Update template information"""
        template = await session.get(ContentTemplate, template_id)
        if not template or not template.is_active:
            return None
        
        update_data = template_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(template, key):
                if key == 'variables' and isinstance(value, list):
                    setattr(template, key, json.dumps(value))
                else:
                    setattr(template, key, value)
        
        session.add(template)
        await session.commit()
        await session.refresh(template)
        return template

    @staticmethod
    async def delete_template(session: Session, template_id: uuid.UUID) -> bool:
        """Soft delete a template"""
        template = await session.get(ContentTemplate, template_id)
        if not template or not template.is_active:
            return False
        
        template.is_active = False
        session.add(template)
        await session.commit()
        return True

    @staticmethod
    async def render_template(template_id: uuid.UUID, variables: Dict[str, Any]) -> Optional[str]:
        """Render a template with provided variables"""
        template = await ContentTemplateService.get_template(template_id)
        if not template:
            return None
        
        try:
            # Parse template variables
            template_vars = json.loads(template.variables) if template.variables else []
            
            # Replace variables in the template prompt
            rendered_prompt = template.template_prompt
            for var in template_vars:
                if var in variables:
                    rendered_prompt = rendered_prompt.replace(f"{{{var}}}", str(variables[var]))
            
            return rendered_prompt
        except Exception:
            return None

    @staticmethod
    async def get_content_types() -> List[str]:
        """Get all unique content types"""
        async with AsyncSessionLocal() as session:
            query = select(ContentTemplate.content_type).where(
                ContentTemplate.is_active == True
            ).distinct()
            
            result = await session.execute(query)
            content_types = result.scalars().all()
            return list(content_types)
