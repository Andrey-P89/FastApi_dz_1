# app/schemas.py
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class CreateAdRequest(BaseModel):
    title: str
    description: str | None = None
    price: Decimal
    author: str


class CreateAdResponse(BaseModel):
    id: int


class GetAdResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: Decimal
    author: str
    created_at: str


class UpdateAdRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None


class UpdateAdResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: Decimal
    author: str
    created_at: str


class OKResponse(BaseModel):
    status: str = "ok"