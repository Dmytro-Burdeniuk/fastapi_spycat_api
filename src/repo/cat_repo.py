from sqlalchemy.orm import Session

from src.schemas.cat import CatCreate
from src.database.models import Cat


def create_cat(db: Session, cat_create: CatCreate) -> Cat:
    cat = Cat(
        name=cat_create.name,
        years_experience=cat_create.years_experience,
        breed=cat_create.breed,
        salary=cat_create.salary,
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def get_cat(db: Session, cat_id: int) -> Cat | None:
    return db.query(Cat).filter(Cat.id == cat_id).first()


def list_cats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cat).offset(skip).limit(limit).all()


def delete_cat(db: Session, cat: Cat) -> None:
    db.delete(cat)
    db.commit()


def update_cat_salary(db: Session, cat: Cat, salary: int) -> Cat:
    cat.salary = salary
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat
