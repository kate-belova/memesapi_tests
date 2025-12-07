import json
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, field_validator


class MemeResponseSchema(BaseModel):
    id: int = Field(description='Meme ID')
    info: dict[str, Any] = Field(
        default_factory=dict, description='Meme info dict'
    )
    tags: list[Any] = Field(default_factory=list, description='List of tags')
    text: str = Field(default='', description='Meme text')
    updated_by: str = Field(default='', description='User name')
    url: str = Field(default='', description='Meme URL')

    model_config = ConfigDict(from_attributes=True)

    @field_validator(
        'info', 'tags', 'text', 'updated_by', 'url', mode='before'
    )
    @classmethod
    def handle_empty_fields(cls, v, info):
        field_name = info.field_name

        if v is None:
            if field_name == 'info':
                return {}
            elif field_name == 'tags':
                return []
            elif field_name in ['text', 'updated_by', 'url']:
                return ''
        return v

    @field_validator('tags', mode='before')
    @classmethod
    def validate_tags(cls, v):
        if v is None:
            return []

        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
                return [parsed]
            except (json.JSONDecodeError, TypeError):
                return [v]

        if not isinstance(v, list):
            return [v]

        return v

    @field_validator('url', mode='before')
    @classmethod
    def validate_url(cls, v):
        if isinstance(v, str) and v:
            if v.startswith('www.'):
                return f'https://{v}'
            elif not v.startswith(('http://', 'https://')):
                return f'https://{v}'
        return v


class MemesResponseSchema(BaseModel):
    data: list[MemeResponseSchema] = Field(description='List of all memes')
