# app/services.py
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from asyncpg.exceptions import UniqueViolationError


import models, schemas


async def add_item(
    session: AsyncSession,
    orm_model: type[models.Ad],
    item_data: schemas.CreateAdRequest
) -> models.Ad:
    """
    Универсальная функция для добавления записи в БД.
    """
    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    try:
        await session.commit()
        await session.refresh(new_item)
        return new_item
    except IntegrityError as e:
        await session.rollback()
        if isinstance(e.orig, UniqueViolationError) and e.orig.pgcode == '23505':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with such data already exists."
            )
        else:
            raise e


async def get_item(
    session: AsyncSession,
    orm_model: type[models.Ad],
    item_id: int
) -> models.Ad:
    """
    Получает запись по ID или выбрасывает 404.
    """
    stmt = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} with id {item_id} not found"
        )
    return item


async def update_item(
    session: AsyncSession,
    orm_model: type[models.Ad],
    item_id: int,
    update_data: schemas.UpdateAdRequest
) -> models.Ad:
    """
    Обновляет запись.
    """
    item = await get_item(session, orm_model, item_id)
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(
    session: AsyncSession,
    orm_model: type[models.Ad],
    item_id: int
) -> None:
    """
    Удаляет запись.
    """
    item = await get_item(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()


async def search_item(
    session: AsyncSession,
    title: str | None = None,
    author: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None
) -> list[models.Ad]:
    """
    Поиск объявлений по фильтрам.
    """
    query = select(models.Ad)
    
    if title:
        query = query.where(models.Ad.title.ilike(f"%{title}%"))
    if author:
        query = query.where(models.Ad.author.ilike(f"%{author}%"))
    if price_min is not None:
        query = query.where(models.Ad.price >= price_min)
    if price_max is not None:
        query = query.where(models.Ad.price <= price_max)
    
    result = await session.execute(query)
    return result.scalars().all()


async def search_item(
    session: AsyncSession,
    orm_model: type[models.Ad],
    title: str | None = None,
    author: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None
) -> list[models.Ad]:
    """
    Поиск объявлений по фильтрам.
    """
    query = select(orm_model)

    if title:
        query = query.where(orm_model.title.ilike(f"%{title}%"))
    if author:
        query = query.where(orm_model.author.ilike(f"%{author}%"))
    if price_min is not None:
        query = query.where(orm_model.price >= price_min)
    if price_max is not None:
        query = query.where(orm_model.price <= price_max)

    result = await session.execute(query)
    return result.scalars().all()