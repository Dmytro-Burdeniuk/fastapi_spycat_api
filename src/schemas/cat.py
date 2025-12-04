from pydantic import BaseModel, Field


class CatBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    years_experience: int = Field(ge=0, le=50)
    breed: str = Field(min_length=1, max_length=100)
    salary: int = Field(ge=0)


class CatCreate(CatBase):
    pass


class CatUpdateSalary(BaseModel):
    salary: int = Field(ge=0)


class CatRead(CatBase):
    id: int

    class Config:
        from_attributes = True
