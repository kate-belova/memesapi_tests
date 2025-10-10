from typing import Any

from pydantic import BaseModel, Field


class PostMemeRequestSchema(BaseModel):
    text: str = Field(description='Meme text')
    url: str = Field(description='Meme URL')
    tags: list[str] = Field(description='Meme tags')
    info: dict[str, Any] = Field(description='Meme info')
