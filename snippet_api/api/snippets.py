import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_current_user
from db.database import get_db
from models.user import User
from schemas.snippet import SnippetCreate, SnippetRead, SnippetUpdate
from services.snippets import (create_snippet, get_by_uuid, list_owner_snippets,
                               update_snippet, delete_snippet)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/snippets", tags=["snippets"])


@router.post("", response_model=SnippetRead, status_code=201)
async def create(data: SnippetCreate, db: AsyncSession = Depends(get_db),
                 user: User = Depends(get_current_user)):
    return await create_snippet(db, user.id, data)


@router.get("/mine", response_model=list[SnippetRead])
async def mine(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await list_owner_snippets(db, user.id)


@router.get("/{snippet_uuid}", response_model=SnippetRead)
async def read(snippet_uuid: str, db: AsyncSession = Depends(get_db)):
    snippet = await get_by_uuid(db, snippet_uuid)
    if snippet is None or not snippet.is_public:
        raise HTTPException(status_code=404, detail="Публичный сниппет не найден")
    return snippet


@router.patch("/{snippet_uuid}", response_model=SnippetRead)
async def update(snippet_uuid: str, data: SnippetUpdate,
                 db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    snippet = await get_by_uuid(db, snippet_uuid)
    if snippet is None:
        raise HTTPException(status_code=404, detail="Сниппет не найден")
    if snippet.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Можно редактировать только свой сниппет")
    return await update_snippet(db, snippet, data)


@router.delete("/{snippet_uuid}", status_code=204)
async def remove(snippet_uuid: str, db: AsyncSession = Depends(get_db),
                 user: User = Depends(get_current_user)):
    snippet = await get_by_uuid(db, snippet_uuid)
    if snippet is None:
        raise HTTPException(status_code=404, detail="Сниппет не найден")
    if snippet.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Можно удалить только свой сниппет")
    await delete_snippet(db, snippet)
