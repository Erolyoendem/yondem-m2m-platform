import logging
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.smart_contract import SmartContract
from app.models.agent import Agent
from app.database.session import SessionLocal

logger = logging.getLogger("yondem")

class DemandPredictor:
    """ML-basierte Bedarfserkennung für Publisher-Agenten"""
    
    def __init__(self):
        self.confidence_threshold = 0.7  # 70% Konfidenz für Bestellung
    
    def predict_demand(self, agent_id, product_category, historical_data=None):
        """Vorhersage ob Bedarf besteht (0.0 - 1.0)"""
        # Simulierte ML-Vorhersage basierend auf:
        # - Historische Verbrauchsdaten
        # - Tageszeit
        # - Saisonalität
        
        if historical_data is None:
            historical_data = self._get_historical_data(agent_id, product_category)
        
        # Faktoren
        time_factor = self._time_based_probability()
        history_factor = self._history_based_probability(historical_data)
        random_factor = random.uniform(0.1, 0.3)  # Rauschen
        
        confidence = (time_factor * 0.3 + history_factor * 0.5 + random_factor * 0.2)
        
        logger.info(f"ML Prediction for {agent_id}/{product_category}: {confidence:.2f}")
        return min(1.0, max(0.0, confidence))
    
    def _get_historical_data(self, agent_id, product_category):
        """Holt historische Daten (simuliert)"""
        # In echt: DB-Abfrage nach vergangenen Bestellungen
        return {
            "avg_consumption_per_day": random.uniform(0.5, 2.0),
            "last_purchase_days_ago": random.randint(1, 10),
            "seasonal_factor": random.uniform(0.8, 1.2)
        }
    
    def _time_based_probability(self):
        """Tageszeit-basierte Wahrscheinlichkeit"""
        hour = datetime.now().hour
        # Morgens (7-9) und Abends (18-20) höhere Wahrscheinlichkeit
        if 7 <= hour <= 9 or 18 <= hour <= 20:
            return 0.8
        elif 10 <= hour <= 17:
            return 0.5
        else:
            return 0.3
    
    def _history_based_probability(self, historical_data):
        """Historische Daten auswerten"""
        days_since_last = historical_data.get("last_purchase_days_ago", 5)
        avg_consumption = historical_data.get("avg_consumption_per_day", 1.0)
        
        # Je länger her, desto wahrscheinlicher
        if days_since_last > 7:
            return 0.9
        elif days_since_last > 3:
            return 0.6
        else:
            return 0.3

# Singleton Instance
predictor = DemandPredictor()

def check_ml_based_demand(agent_id, product_category):
    """Öffentliche Funktion für ML-Vorhersage"""
    confidence = predictor.predict_demand(agent_id, product_category)
    return confidence >= predictor.confidence_threshold, confidence
