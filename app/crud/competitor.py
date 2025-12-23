from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.competitor_qoute import VEH_COMPETITOR_QUOTE
from app.schemas.competitor_quotes import COMPETITORS
from typing import Dict

class CompetitorCRUD:
  
    def save(self, vehicle_id: int, price: str, db: Session, competitor: COMPETITORS):
        """Save competitor quote data to the database."""
        competitor_quote = VEH_COMPETITOR_QUOTE(
            veh_id=vehicle_id,
            price=price,
            competitor=competitor
        )
        db.add(competitor_quote)
        db.commit()
        db.refresh(competitor_quote)
        return competitor_quote 
    
    def create_or_update_price(self,db: Session, veh_id: int, price: str,  competitor: COMPETITORS):
        competitor_db = db.query(VEH_COMPETITOR_QUOTE).filter(VEH_COMPETITOR_QUOTE.veh_id == veh_id, VEH_COMPETITOR_QUOTE.competitor==competitor).order_by(
            desc(VEH_COMPETITOR_QUOTE.updated_at)).first()
        if not competitor_db:
            return self.save(veh_id, price, db, competitor)
        else:
            if competitor_db.price == price:
                return competitor_db
            else:
                setattr(competitor_db, 'price' , price)
                db.commit()
                db.refresh(competitor_db)
                return competitor_db
        
        
    def get_competitor_by_vehicle_id(self, db: Session, veh_id: int ) -> Dict[str, float]:
        """Retrieve all competitor prices for a given vehicle ID."""
        quotes = (
            db.query(VEH_COMPETITOR_QUOTE)
            .filter(VEH_COMPETITOR_QUOTE.veh_id == veh_id)
            .all()
        )
        
        return {quote.competitor.value: float(quote.price) for quote in quotes}
    

    def get_price_by_source(self, db: Session, veh_id: int, competitor: COMPETITORS):
        """Get the latest price for a vehicle from a specific competitor"""
        competitor_db = db.query(VEH_COMPETITOR_QUOTE).filter(
            VEH_COMPETITOR_QUOTE.veh_id == veh_id, 
            VEH_COMPETITOR_QUOTE.competitor == competitor
        ).first()
        
        return competitor_db
    
competitor_crud = CompetitorCRUD()