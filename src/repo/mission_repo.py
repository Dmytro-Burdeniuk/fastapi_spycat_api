from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Mission, Target, Cat
from src.schemas.mission import MissionCreate
from src.schemas.target import TargetUpdate


def ensure_cat_available(db: Session, cat_id: int, mission_id: Optional[int] = None):
    active_missions = (
        db.query(Mission)
        .filter(
            Mission.cat_id == cat_id,
            Mission.is_completed == False,  # noqa: E712
        )
        .all()
    )

    for m in active_missions:
        if mission_id is None or m.id != mission_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cat already has an active mission",
            )


def create_mission(db: Session, mission_create: MissionCreate) -> Mission:
    if mission_create.cat_id is not None:
        ensure_cat_available(db, mission_create.cat_id)

    mission = Mission(
        name=mission_create.name,
        cat_id=mission_create.cat_id,
        is_completed=False,
    )

    for t in mission_create.targets:
        target = Target(
            name=t.name,
            country=t.country,
            notes=t.notes,
            is_completed=False,
        )
        mission.targets.append(target)

    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


def get_mission(db: Session, mission_id: int) -> Optional[Mission]:
    return db.query(Mission).filter(Mission.id == mission_id).first()


def list_missions(db: Session, skip: int = 0, limit: int = 100) -> List[Mission]:
    return db.query(Mission).offset(skip).limit(limit).all()


def delete_mission(db: Session, mission: Mission) -> None:
    if mission.cat_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mission cannot be deleted because it is assigned to a cat",
        )
    db.delete(mission)
    db.commit()


def assign_cat_to_mission(
    db: Session,
    mission: Mission,
    cat: Cat,
) -> Mission:
    if mission.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign a cat to a completed mission",
        )

    ensure_cat_available(db, cat.id, mission_id=mission.id)

    mission.cat_id = cat.id
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


def get_target_in_mission(
    db: Session,
    mission_id: int,
    target_id: int,
) -> Target:
    target = (
        db.query(Target)
        .filter(
            Target.id == target_id,
            Target.mission_id == mission_id,
        )
        .first()
    )
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found in this mission",
        )
    return target


def update_target(
    db: Session,
    mission: Mission,
    target: Target,
    target_update: TargetUpdate,
) -> Target:
    if mission.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update targets of a completed mission",
        )

    if target.is_completed and target_update.notes is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update notes of a completed target",
        )

    if target.is_completed and target_update.is_completed is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot mark a completed target as incomplete",
        )

    if target_update.notes is not None:
        target.notes = target_update.notes

    if target_update.is_completed is True:
        target.is_completed = True

    db.add(target)
    db.commit()
    db.refresh(target)

    if not mission.is_completed:
        all_completed = all(t.is_completed for t in mission.targets)
        if all_completed:
            mission.is_completed = True
            db.add(mission)
            db.commit()
            db.refresh(mission)

    return target
