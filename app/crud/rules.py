from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, delete
from app.models.rules import Rule, CompoundRule
from app.schemas.rules import RuleRequest, RuleType
from enum import Enum

class RuleCRUD:
    def create(self, db, rule_data: RuleRequest) -> Rule:

        rule_dict = rule_data.dict(exclude={"compoundRules"})
        rule = Rule(**rule_dict)
        db.add(rule)
        db.commit()
        db.refresh(rule)

        if rule_data.compoundCondition and rule_data.compoundRules:
            for cr in rule_data.compoundRules:
                compound_rule = CompoundRule(
                    **cr.dict(),
                    rule_id=rule.id
                )
                db.add(compound_rule)
            db.commit()
        return rule

    
    
    def get_by_type(self, db, active_rule_type: str) -> list[Rule]:

        rule_type_value = active_rule_type.value if isinstance(active_rule_type, RuleType) else active_rule_type
        return db.query(Rule).filter(Rule.type == rule_type_value).all()

    def get_by_id(self, db: Session, rule_id: int):
        return db.query(Rule).filter(Rule.id == rule_id).first()
    
    
    def update(self, db, rule_id: int, rule_data: RuleRequest) -> Rule | None:
        rule = db.query(Rule).filter(Rule.id == rule_id).first()
        if not rule:
            return None

        data = rule_data.dict(exclude_unset=True)
        compound_rules = data.pop("compoundRules", None)  # remove compoundRules from data

        # Update normal rule fields (excluding compoundRules)
        for key, value in data.items():
            if hasattr(rule, key):
                setattr(rule, key, value)

        # Handle compound rules based on compoundCondition and compound_rules
        if rule.compoundCondition is True and isinstance(compound_rules, list) and len(compound_rules) > 0:
            # Delete old compound rules
            db.query(CompoundRule).filter(CompoundRule.rule_id == rule.id).delete()
            # Insert new compound rules
            for cr in compound_rules:
                compound_rule = CompoundRule(
                    **cr,
                    rule_id=rule.id
                )
                db.add(compound_rule)
        elif (len(compound_rules) == 0) or compound_rules is None :
            # Delete existing compound rules when compoundCondition is False or compound_rules is empty/undefined
            db.query(CompoundRule).filter(CompoundRule.rule_id == rule.id)
                
        db.commit()
        db.refresh(rule)
        return rule
    
    
    def delete(self, db: Session, rule_id: int) -> bool:
        rule = db.query(Rule).filter(Rule.id == rule_id).first()
        if not rule:
            return False
        # Delete all compound rules for this rule
        db.query(CompoundRule).filter(CompoundRule.rule_id == rule_id).delete()
        # Delete the rule itself
        db.delete(rule)
        db.commit()
        return True
    def get_all_active(self, db: Session) -> list[Rule]:
        return db.query(Rule).options(joinedload(Rule.compoundRules)).filter(Rule.isActive == True).all()
    
rules_crud = RuleCRUD()