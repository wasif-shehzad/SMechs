from sqlalchemy.orm import Session
from app.schemas.contact import ContactRequest
from app.models.contact import Contact


class ContactCRUD:
    def create_veh_contact(self, db: Session, contact_data: ContactRequest):
        """Create a new contact in the database."""
        db_contact = Contact(**contact_data.dict())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)

        return db_contact
    
    def get_all_veh_contact(self, db: Session):
        return db.query(Contact).all()
    
    

contact_crud = ContactCRUD()
