# app/crud/vehicle.py
from sqlalchemy.orm import Session
from app.models.veh_details import Veh_Details as VehicleDetailsModel
from app.schemas.veh_details import Veh_Details, Veh_Details_DB, Veh_Details_With_Vech_Id
from app.schemas.ext_detail import Extended_Details_DB, Extended_Details
from app.models.ext_details import EXTENDED_DETAILS
from typing import Optional

class VehDetailsCRUD:
    async def get_by_id(self, db: Session, id:int) -> Optional[Veh_Details]:
        print(f"Retrieving vehicle details by id: {id}")

        """
        Retrieve a vehicle detail record by its ID.
        """
        vehicle_details = db.query(Veh_Details).filter(Veh_Details.id == id).first()
        print(f"Vehicle details found: {vehicle_details}")
        if vehicle_details:
            return Veh_Details.from_orm(vehicle_details)
        else:
            print("No vehicle details found with the given ID.")
            return None

    def get_details_by_veh_id(self, db: Session, veh_id: int) -> Optional[Veh_Details_DB]:
        """
        Retrieve vehicle details by vehicle ID.
        """
        print(f"Retrieving vehicle details by vehicle ID: {veh_id}")
        vehicle_details = db.query(VehicleDetailsModel).filter(VehicleDetailsModel.veh_id == veh_id).first()
        print(f"Vehicle details found: {vehicle_details}")
        if vehicle_details:
            return Veh_Details_DB.from_orm(vehicle_details)
        else:
            print("No vehicle details found with the given vehicle ID.")
            return None
        
    async def create(self, db: Session, data: Veh_Details_With_Vech_Id) -> Veh_Details_DB:
        """
        Create a new vehicle detail record.
        """
        print(f"Creating vehicle details record: {data}")
        db_vehicle_details = VehicleDetailsModel(**data.model_dump())
        print(f"Database vehicle details object: {db_vehicle_details}")
        db.add(db_vehicle_details)
        db.commit()
        db.refresh(db_vehicle_details)
        return Veh_Details_DB.from_orm(db_vehicle_details)
    
    async def create_extended_details(self, db: Session, data:Extended_Details) -> Extended_Details_DB:
        """
        Create a new extended vehicle detail record.
        """
        print(f"Creating extended vehicle details record: {data}")
        db_extended_details = EXTENDED_DETAILS(**data.model_dump())
        print(f"Database extended details object: {db_extended_details}")
        db.add(db_extended_details)
        db.commit()
        db.refresh(db_extended_details)
        return Extended_Details_DB.from_orm(db_extended_details)
    
    async def get_extended_details_by_vehicle_detail_id(self, db:Session, id:int)-> Optional[Extended_Details_DB]:
        extended_details = db.query(EXTENDED_DETAILS).filter(EXTENDED_DETAILS.veh_details_id == id).first()
        if extended_details:
            return extended_details
        else:
            return None
    
veh_details_crud = VehDetailsCRUD()