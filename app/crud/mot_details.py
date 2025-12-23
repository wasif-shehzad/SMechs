# app/crud/vehicle.py
from sqlalchemy.orm import Session
from app.models.mot_details import MOT_TESTS, DEFECTS, MOT_DETAILS
from app.schemas.mot_details import Mot_Details, Mot_Tests, Defects, Mot_Details_DB, Mot_Tests_DB, Defects_DB
from typing import Optional

class MotDetailsCRUD: 
    def create_mot_details(self, db: Session, data: Mot_Details) -> Mot_Details_DB:
        """
        Create a new MOT detail record.
        """
        print(f"Creating MOT details record")
        mot_details = MOT_DETAILS(**data.model_dump(exclude={"motTests"}))
        print(f"Database mot details object saved")
        db.add(mot_details)
        db.commit()
        db.refresh(mot_details)
        return Mot_Details_DB.from_orm(mot_details)
    async def get_mot_details_by_veh_details_id(self, db: Session, veh_details_id: int) -> Optional[list[Mot_Tests_DB]]:
        """
        Retrieve MOT details by vehicle details ID.
        """
        mot_details = db.query(MOT_DETAILS).filter(MOT_DETAILS.veh_details_id == veh_details_id).first()
        if not mot_details:
            return None
        motTests = db.query(MOT_TESTS).filter(MOT_TESTS.mot_details_id == mot_details.id).all()
        
        if mot_details and motTests:
            return motTests
        return None
    def create_or_get_mot_details_by_veh_details_id(self, db: Session, data: Mot_Details) -> Optional[Mot_Details_DB]:
        """
        Create or retrieve MOT details by vehicle details ID.
        """
        mot_details = db.query(MOT_DETAILS).filter(MOT_DETAILS.veh_details_id == data.veh_details_id).first()
        if not mot_details:
            return self.create_mot_details(db, data)
        else:
            return self.get_mot_details_by_veh_details_id(db, data.veh_details_id)
            
    
    def create_mot_test(self, db: Session, data: Mot_Tests) -> Optional[Mot_Tests_DB]:
        """
        Create a new MOT tests record.
        """
        print(f"Creating MOT tests record: {data}")
        db_mot_tests = MOT_TESTS(**data.model_dump(exclude={"defects"}))
        print(f"Database MOT tests object saved")
        db.add(db_mot_tests)
        db.commit()
        db.refresh(db_mot_tests)
        return Mot_Tests_DB.from_orm(db_mot_tests)
    
    def create_or_update_mot_test_by_mot_details_id(self, db: Session, mot_details_id: int, data: Mot_Tests) -> Optional[Mot_Tests_DB]:
        """
        Create or retrieve MOT tests by MOT details ID.
        """
        mot_tests = db.query(MOT_TESTS).filter(MOT_TESTS.mot_details_id == mot_details_id).all()
        if not mot_tests:
                return self.create_mot_test(db, data)
        else:
            for m_test in mot_tests:
                    if data.odometerValue == m_test.odometerValue and data.completedDate == m_test.completedDate:
                        return m_test
            return self.create_mot_test(db, data)

    def create_or_update_defects(self, db: Session, mot_test_id: int, data: Defects) -> Optional[Defects_DB]:
        """
        Create or retrieve defects by MOT test ID.
        """
        defects = db.query(DEFECTS).filter(DEFECTS.mot_test_id == mot_test_id).all()
        if not defects:
            return self.create_defects(db, data)
        else:
            for defect in defects:
                if data.type == defect.type and data.dangerous == defect.dangerous and data.text == defect.text:
                    return defect
            return self.create_defects(db, data)
        
    def create_defects(self, db: Session, data: Defects) -> Defects_DB:
        """
        Create a new defects record.
        """
        print(f"Creating defects record: {data}")
        db_defects = DEFECTS(**data.model_dump())
        print(f"Database defects object: {db_defects}")
        db.add(db_defects)
        db.commit()
        db.refresh(db_defects)
        return Defects_DB.from_orm(db_defects)
    
mot_details_crud = MotDetailsCRUD()
