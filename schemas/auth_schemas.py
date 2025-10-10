from pydantic import BaseModel, Field, ConfigDict


class AuthRequestSchema(BaseModel):
    name: str = Field(description='User name (can be empty)')


class AuthResponseSchema(BaseModel):
    token: str = Field(description='Authorization token')
    user: str = Field(description='User name (can be empty)')

    model_config = ConfigDict(from_attributes=True)
