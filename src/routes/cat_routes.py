from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.cat import CatCreate, CatRead, CatUpdateSalary
from src.database.session import get_db
from src.repo import cat_repo
from src.services.cat_api import CatApiClient, CatApiError

router = APIRouter(prefix="/cats", tags=["cats"])
cat_api_client = CatApiClient()


@router.post("", response_model=CatRead, status_code=status.HTTP_201_CREATED)
def create_cat(cat_create: CatCreate, db: Session = Depends(get_db)):

    try:
        cat_api_client.search_breed(cat_create.breed)
    except CatApiError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    cat = cat_repo.create_cat(db, cat_create)
    return cat


@router.get("", response_model=List[CatRead])
def list_cats(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    cats = cat_repo.list_cats(db, skip=skip, limit=limit)
    return cats


@router.get("/{cat_id}", response_model=CatRead)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = cat_repo.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat not found",
        )
    return cat


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = cat_repo.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat not found",
        )
    cat_repo.delete_cat(db, cat)
    return None


@router.patch("/{cat_id}/salary", response_model=CatRead)
def update_cat_salary(
    cat_id: int,
    salary_update: CatUpdateSalary,
    db: Session = Depends(get_db),
):
    cat = cat_repo.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat not found",
        )
    updated = cat_repo.update_cat_salary(db, cat, salary_update.salary)
    return updated
