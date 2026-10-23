from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.snippet import Snippet
from schemas.snippet import SnippetCreate, SnippetUpdate


async def create_snippet(db: AsyncSession, owner_id: int, data: SnippetCreate) -> Snippet:
    snippet = Snippet(**data.model_dump(), owner_id=owner_id)
    db.add(snippet)
    await db.commit()
    await db.refresh(snippet)
    return snippet


async def get_by_uuid(db: AsyncSession, snippet_uuid: str) -> Snippet | None:
    return await db.scalar(select(Snippet).where(Snippet.uuid == snippet_uuid))


async def list_owner_snippets(db: AsyncSession, owner_id: int) -> list[Snippet]:
    result = await db.scalars(select(Snippet).where(Snippet.owner_id == owner_id))
    return list(result.all())


async def update_snippet(db: AsyncSession, snippet: Snippet, data: SnippetUpdate) -> Snippet:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(snippet, key, value)
    await db.commit()
    await db.refresh(snippet)
    return snippet


async def delete_snippet(db: AsyncSession, snippet: Snippet) -> None:
    await db.delete(snippet)
    await db.commit()
