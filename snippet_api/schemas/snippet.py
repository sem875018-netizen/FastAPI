from pydantic import BaseModel, ConfigDict, Field


class SnippetCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=1)
    language: str = Field(default="text", max_length=50)
    is_public: bool = True


class SnippetUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    code: str | None = None
    language: str | None = Field(default=None, max_length=50)
    is_public: bool | None = None


class SnippetRead(BaseModel):
    uuid: str
    title: str
    code: str
    language: str
    is_public: bool
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
