# app/crud/vehicle.py
from sqlalchemy.orm import Session, joinedload
from app.models.vehicle import Vehicle as VehicleModel
from app.models.veh_details import Veh_Details as VehDetailsModel
from app.models.ext_details import EXTENDED_DETAILS as VehExtDetailsModel
from app.schemas.vehicle import VehicleDetailsRequest, Vehicle, VehicleDetailsResponse, Status
import enum
from typing import Optional


class VehicleCRUD:
    async def get_by_registration(self, db: Session, registration: str) -> Optional[Vehicle]:
        print(f"Retrieving vehicle with registration: {registration}")
        print(f"Database session: {db}")

        """
        Retrieve a vehicle by its registration number.
        """
        registration = registration.strip()
        vehicle = db.query(VehicleModel).filter(VehicleModel.registration.ilike(registration)).first()
        print(f"Vehicle found: {vehicle}")
        if vehicle:
            return Vehicle.from_orm(vehicle)
        else:
            print("No vehicle found with the given registration.")
            return None

    async def create(self, db: Session, data: VehicleDetailsRequest) -> Vehicle:
        """
        Create a new vehicle record.
        """
        print(f"Creating vehicle with data: {data.__dict__}")

        db_vehicle = VehicleModel(**data.dict())
        print(f"Database vehicle object: {db_vehicle}")
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return Vehicle.from_orm(db_vehicle)

    async def get_vehicle_detail_by_id(self, db: Session, vehicle_id: int) -> Optional[VehicleModel]:
        """
        Retrieve the raw SQLAlchemy vehicle model by ID.
        """
        return db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    

    async def update_location_radius(self, db: Session, vehicle_id: int, with_in_radius: bool) -> Optional[Vehicle]:
        """
        Update the location radius status of a vehicle.
        """
        print(f"Updating vehicle with ID {vehicle_id} to with_in_radius {with_in_radius}")
        vehicle = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        if not vehicle:
            print(f"No vehicle found with ID {vehicle_id}")
            return None
        vehicle.with_in_radius = with_in_radius
        db.commit()
        db.refresh(vehicle)
        return Vehicle.from_orm(vehicle)
    
    async def update_status(self, db: Session, vehicle_id: int, status: str) -> Optional[Vehicle]:
        """
        Update the status of a vehicle.
        """
        print(f"Updating vehicle with ID {vehicle_id} to status {status}")
        vehicle = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        if not vehicle:
            print(f"No vehicle found with ID {vehicle_id}")
            return None
        setattr(vehicle, "status", status)
        db.commit()
        db.refresh(vehicle)
        return Vehicle.from_orm(vehicle)
    
    async def get_vehicle_details_by_id(self, db: Session, vehicle_id: int) -> Optional[VehicleDetailsResponse]:
        """
        Retrieve vehicle details by ID.
        """
        print(f"Retrieving vehicle details for ID: {vehicle_id}")
        # Fetch the vehicle details from the database as well
        vehicle = db.query(VehicleModel).options(
            joinedload(VehicleModel.veh_details)
                .options(
                    joinedload(VehDetailsModel.veh_mot_details),
                    joinedload(VehDetailsModel.veh_ext_details),
                )
        ).filter(VehicleModel.id == vehicle_id).first()
        print(f"Vehicle found: {vehicle}")
        if not vehicle:
            print(f"No vehicle found with ID {vehicle_id}")
            return None
        return VehicleDetailsResponse.from_orm(vehicle)
    
    async def update(self, db:Session, key:str, value: any, id:int):
        vehicle = db.query(VehicleModel).filter(VehicleModel.id == id).first()
        setattr(vehicle, key, value)
        db.commit()
        db.refresh(vehicle)
        return Vehicle.from_orm(vehicle)
        

vehicle_crud = VehicleCRUD()