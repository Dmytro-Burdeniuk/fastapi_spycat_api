from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.mission import MissionCreate, MissionRead, MissionAssignCat
from src.schemas.target import TargetRead, TargetUpdate
from src.database.session import get_db
from src.repo import cat_repo, mission_repo

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("", response_model=MissionRead, status_code=status.HTTP_201_CREATED)
def create_mission(
    mission_in: MissionCreate,
    db: Session = Depends(get_db),
):
    if mission_in.cat_id is not None:
        cat = cat_repo.get_cat(db, mission_in.cat_id)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cat for mission does not exist",
            )
    mission = mission_repo.create_mission(db, mission_in)
    return mission


@router.get("", response_model=List[MissionRead])
def list_missions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    missions = mission_repo.list_missions(db, skip=skip, limit=limit)
    return missions


@router.get("/{mission_id}", response_model=MissionRead)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = mission_repo.get_mission(db, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found",
        )
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = mission_repo.get_mission(db, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found",
        )
    mission_repo.delete_mission(db, mission)
    return None


@router.post("/{mission_id}/assign-cat", response_model=MissionRead)
def assign_cat(
    mission_id: int,
    payload: MissionAssignCat,
    db: Session = Depends(get_db),
):
    mission = mission_repo.get_mission(db, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found",
        )

    cat = cat_repo.get_cat(db, payload.cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat not found",
        )

    mission = mission_repo.assign_cat_to_mission(db, mission, cat)
    return mission


@router.patch(
    "/{mission_id}/targets/{target_id}",
    response_model=TargetRead,
)
def update_target(
    mission_id: int,
    target_id: int,
    target_update: TargetUpdate,
    db: Session = Depends(get_db),
):
    mission = mission_repo.get_mission(db, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found",
        )

    target = mission_repo.get_target_in_mission(db, mission_id, target_id)
    updated_target = mission_repo.update_target(db, mission, target, target_update)
    return updated_target
