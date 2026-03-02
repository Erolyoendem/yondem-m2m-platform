import logging
from sqlalchemy.orm import Session
from app.models.agent import Agent
from app.models.transaction import Transaction
from app.models.smart_contract import SmartContract
from app.database.session import SessionLocal

logger = logging.getLogger("yondem")

class TrustScorer:
    """Berechnet Trust-Score für Agents"""
    
    def __init__(self):
        self.success_weight = 0.9  # 90% Erfolgsrate
        self.payment_weight = 0.1  # 10% Zahlungshistorie
    
    def calculate_trust_score(self, agent_id):
        """Berechnet Trust-Score (0-100)"""
        db = SessionLocal()
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                return 50  # Default mittlerer Wert
            
            # Erfolgsrate aus Smart Contracts
            success_rate = self._get_success_rate(db, agent_id)
            
            # Zahlungshistorie aus Transaktionen
            payment_score = self._get_payment_score(db, agent_id)
            
            # Gewichtete Berechnung
            trust_score = (success_rate * self.success_weight + 
                          payment_score * self.payment_weight) * 100
            
            # Update Agent
            agent.trust_level = int(min(100, max(0, trust_score)))
            db.commit()
            
            logger.info(f"Trust Score for {agent_id}: {agent.trust_level}")
            return agent.trust_level
            
        except Exception as e:
            logger.error(f"Error calculating trust score: {e}")
            return 50
        finally:
            db.close()
    
    def _get_success_rate(self, db, agent_id):
        """Erfolgsrate aus Contracts (0.0 - 1.0)"""
        contracts = db.query(SmartContract).filter(
            SmartContract.agent_id == agent_id
        ).all()
        
        if not contracts:
            return 0.5  # Neutral
        
        total_executions = sum(c.execution_count for c in contracts)
        total_successes = sum(c.success_count for c in contracts)
        
        if total_executions == 0:
            return 0.5
        
        return total_successes / total_executions
    
    def _get_payment_score(self, db, agent_id):
        """Zahlungstreue (0.0 - 1.0)"""
        transactions = db.query(Transaction).filter(
            Transaction.publisher_id == agent_id
        ).all()
        
        if not transactions:
            return 0.5  # Neutral
        
        completed = sum(1 for t in transactions if t.status == "completed")
        return completed / len(transactions)

# Singleton
scorer = TrustScorer()

def update_trust_score(agent_id):
    """Öffentliche Funktion zum Updaten des Trust-Scores"""
    return scorer.calculate_trust_score(agent_id)
