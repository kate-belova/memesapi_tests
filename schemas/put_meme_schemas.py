from typing import Any

from pydantic import BaseModel, Field


class PutMemeRequestSchema(BaseModel):
    id: int = Field(description='Meme id')
    text: str = Field(description='Meme text')
    url: str = Field(description='Meme URL')
    tags: list[str] = Field(description='Meme tags')
    info: dict[str, Any] = Field(description='Meme info')
