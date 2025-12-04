from typing import Optional

from pydantic import BaseModel, Field


class TargetBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=1, max_length=100)
    notes: Optional[str] = None


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_completed: Optional[bool] = None


class TargetRead(TargetBase):
    id: int
    is_completed: bool

    class Config:
        from_attributes = True
