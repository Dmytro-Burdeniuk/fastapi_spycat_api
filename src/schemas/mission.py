from typing import Optional, List

from pydantic import BaseModel, Field, root_validator

from src.schemas.target import TargetCreate, TargetRead
from src.schemas.cat import CatRead


class MissionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class MissionCreate(MissionBase):
    targets: List[TargetCreate] = Field(min_items=1, max_items=3)
    cat_id: Optional[int] = None


class MissionAssignCat(BaseModel):
    cat_id: int


class MissionRead(MissionBase):
    id: int
    is_completed: bool
    cat: Optional[CatRead]
    targets: List[TargetRead]

    class Config:
        from_attributes = True
