# app/crud/audit_trail.py
from sqlalchemy.orm import Session
from app.schemas.veh_audit_trail import VehAuditTrailCreate, PaginatedAudiTrailRespose
from app.models.veh_audit_trail import VehAuditTrail
class AuditTrailCRUD:
    
    def create_audit_trail(self, db: Session, data: VehAuditTrailCreate) -> VehAuditTrail:
        """Create audit trail record in DB"""
        audit_data = VehAuditTrail(**data.dict())
        db.add(audit_data)
        db.commit()
        db.refresh(audit_data)
        return audit_data
    
    def get_audit_trail_id(self, db: Session, audit_id: int) -> list[VehAuditTrail]:
        """Get audit trail records by ID"""
        audit_trail = db.query(VehAuditTrail).filter(VehAuditTrail.id == audit_id).first()
        if not audit_trail:
            return None
        return audit_trail        
        
    def get_by_vehicle_id(self, db:Session, vehicle_id: int)-> VehAuditTrail:
        """Get audit trail by vechicle ID"""
        return db.query(VehAuditTrail).filter(VehAuditTrail.veh_id == vehicle_id).first()
    
    # get all audit trails
    def get_all_audit_trails(self, db: Session, page:int , limit:int ) -> dict:
        """Get all audit trail records"""
        query = db.query(VehAuditTrail)
        total = query.count()
        items = (
            query.order_by(VehAuditTrail.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return PaginatedAudiTrailRespose(items=items, items_per_page=len(items), total_items=total, page=page, page_limit=limit)
    
    def create_or_update_based_on_vehicle_id(self, db: Session, data: VehAuditTrailCreate) -> VehAuditTrail:
        """Create or update audit trail based on vehicle ID"""
        existing_audit = db.query(VehAuditTrail).filter(VehAuditTrail.veh_id == data.veh_id).first()
        if existing_audit:
            for key, value in data.dict().items():
                setattr(existing_audit, key, value)
            db.commit()
            db.refresh(existing_audit)
            return existing_audit
        else:
            new_audit = VehAuditTrail(**data.dict())
            db.add(new_audit)
            db.commit()
            db.refresh(new_audit)
            return new_audit

    def get_audit_trails_by_registration(self, db: Session, registration: str, page:int, limit: int):
        query = db.query(VehAuditTrail).filter(VehAuditTrail.registration.ilike(f"%{registration}%"))
        total = query.count()
        items = (
            query.order_by(VehAuditTrail.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return PaginatedAudiTrailRespose(items=items, items_per_page=len(items), total_items=total, page=page, page_limit=limit)

audit_trail_crud = AuditTrailCRUD()