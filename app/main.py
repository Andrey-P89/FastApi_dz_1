# app/main.py

from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.lifespan import lifespan
from app.database import AsyncSessionLocal
from app import models, schemas

from app.dependencies import get_db_session

from app.services import add_item, get_item, update_item, delete_item, search_item

app = FastAPI(
    title="Advertisement App",
    description="This is a very simple advertisement application API",
    version="0.0.1",
    lifespan=lifespan
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@app.post(
    "/v1/ad", 
    response_model=schemas.CreateAdResponse, 
    summary="Создать новое объявление"
)
async def create_ad(
    ad_data: schemas.CreateAdRequest,
    session: SessionDep
    ):
    new_ad = await add_item(session, models.Ad, ad_data)
    return schemas.CreateAdResponse(id=new_ad.id)


@app.get(
    "/v1/ad/{item_id}", 
    response_model=schemas.GetAdResponse, 
    summary="Получить объявление по ID"
)
async def get_ad(
    item_id: int,
    session: SessionDep
    ):
    ad = await get_item(session, models.Ad, item_id)
    return schemas.GetAdResponse(**ad.to_dict())


@app.patch(
    "/v1/ad/{item_id}", 
    response_model=schemas.UpdateAdResponse, 
    summary="Обновить объявление"
)
async def update_ad(
    item_id: int,
    update_data: schemas.UpdateAdRequest,
    session: SessionDep
    ):
    updated_ad = await update_item(session, models.Ad, item_id, update_data)
    return schemas.UpdateAdResponse(**updated_ad.to_dict())


@app.delete(
    "/v1/ad/{item_id}", 
    status_code=204, 
    summary="Удалить объявление"
)
async def delete_ad(
    item_id: int,
    session: SessionDep
    ):
    await delete_item(session, models.Ad, item_id)


@app.get("/v1/ad",
    response_model=list[schemas.GetAdResponse],
    summary="Поиск объявлений"
)
async def search_ads(
    session: SessionDep,
    title: str | None = None,
    author: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    limit: int = 100,
    offset: int = 0,
    ):
    ads = await search_item(
        session,
        models.Ad,
        title,
        author,
        price_min,
        price_max,
        limit,
        offset
    )
    return [schemas.GetAdResponse(**ad.to_dict()) for ad in ads]