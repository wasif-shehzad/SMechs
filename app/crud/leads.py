from sqlalchemy.orm import Session
from app.models.leads import VehLeads
from app.schemas.leads import VehLeadRequest,AbandonedLeadRequest,LeadFilterQuery,CallToActionLead
from app.schemas.leads import LeadStatus
from sqlalchemy.inspection import inspect
from app.crud.audit_trail import audit_trail_crud
class LeadCRUD:

    def get_lead_by_id(self, db: Session, lead_id: int):
        return db.query(VehLeads).filter(VehLeads.id == lead_id).first()

    def delete_veh_lead(db: Session, lead_id: int):
        lead = db.query(VehLeads).filter(VehLeads.id == lead_id).first()
        if lead:
            db.delete(lead)
            db.commit()
            return True
        return False

    def get_all_veh_leads(self, db: Session):
        return db.query(VehLeads).all()

    def create_or_update_lead(self, db: Session, data: CallToActionLead):
        """Get existing lead by veh_id or create a new call to action lead."""

        if "phone_number" in data:
            data["phone"] = data.pop("phone_number")
        
        if "id" in data:
            data.pop("id")

        lead_columns = {c.key for c in inspect(VehLeads).mapper.column_attrs}
        data_dict = None
        if type(data) is not dict:
            data = {**data.dict()}
        data_dict = {k: v for k, v in data.items() if k in lead_columns}
        existing_lead = db.query(VehLeads).filter(VehLeads.veh_id == data_dict["veh_id"]).first()
        print("existing lead", existing_lead)
        if existing_lead:
            for key, value in data_dict.items():
                setattr(existing_lead, key, value)
            if not existing_lead.quoteValue:
                audit_trail = audit_trail_crud.get_by_vehicle_id(db, data['veh_id'])
                if audit_trail:
                    if audit_trail.quote:
                        existing_lead.quoteValue = audit_trail.quote
            db.commit()
            db.refresh(existing_lead)
            return existing_lead
        else:
            # print("data",data)
            veh_id = data['veh_id']
            audit_trail = audit_trail_crud.get_by_vehicle_id(db, veh_id)
            print("audit_trail",audit_trail)
            quote_value = None
            if audit_trail:
                quote_value = audit_trail.quote

            data_dict["quoteValue"] = quote_value
            print("data_dict", data_dict)
            new_lead = VehLeads(**data_dict)
            db.add(new_lead)
            db.commit()
            db.refresh(new_lead)
            return new_lead
    
    def get_filters_by_leads(self, db:Session, filters: LeadFilterQuery, page: int, limit: int):

        query = db.query(VehLeads)

        if filters.status and filters.status != "all":
            query = query.filter(VehLeads.status == filters.status)

        if filters.registration:
            query = query.filter(VehLeads.registration.ilike(f"%{filters.registration}%"))

        if filters.days:
            from datetime import datetime, timedelta
            date_from = datetime.utcnow() - timedelta(days=filters.days)
            query = query.filter(VehLeads.created_at >= date_from)

        query = query.order_by(VehLeads.created_at.desc())
        total = query.count()
        items = (
        query.offset((page - 1) * limit)
             .limit(limit)
             .all()
        )
        return  { "items": items,"total_items": total, "items_per_page": len(items), "page": page,"page_limit": limit}
        



lead_crud = LeadCRUD()