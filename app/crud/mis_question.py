

from sqlalchemy.orm import Session
from app.models.mis_question import VehMisQuestion
from app.schemas.mis_question import VehicleQuestionsRequest
from typing import Dict


class VehMisQuestionCRUD:
    def create_or_update(self, db: Session, data: VehicleQuestionsRequest):
        """Create new or update vehicle mis questions based on veh_id"""
        existing = db.query(VehMisQuestion).filter(
            VehMisQuestion.veh_id == data.veh_id
        ).first()

        if existing:
            # Update existing
            for field, value in data.dict(exclude_unset=True).items():
                setattr(existing, field, value)
            db.commit()
            db.refresh(existing)
            return existing

        # Create new
        new_entry = VehMisQuestion(**data.dict())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry

    def get_mis_question_by_veh_id(self, db: Session, veh_id: int):
        """Retrieve vehicle mis questions by veh_id"""
        return (db.query(VehMisQuestion).filter(VehMisQuestion.veh_id == veh_id).first())

veh_mis_question_crud = VehMisQuestionCRUD()
