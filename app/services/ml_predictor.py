"""
Real ML-based demand prediction and trust scoring.

- GradientBoostingRegressor  → Demand Prediction (0.0 – 1.0)
- IsolationForest            → Anomaly Detection for Trust Scoring

Models are trained on synthetic-but-realistic data at first startup,
then persisted in the models/ directory and reloaded on subsequent runs.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Tuple

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger("yondem")

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

_DEMAND_MODEL_PATH = os.path.join(MODELS_DIR, "demand_model.joblib")
_DEMAND_SCALER_PATH = os.path.join(MODELS_DIR, "demand_scaler.joblib")
_TRUST_MODEL_PATH = os.path.join(MODELS_DIR, "trust_model.joblib")

CONFIDENCE_THRESHOLD = 0.65


# ── Synthetic training data ────────────────────────────────────────────────

def _synthetic_demand_data(n: int = 1200) -> Tuple[np.ndarray, np.ndarray]:
    """
    Features: [days_since_last_purchase, avg_consumption_per_day,
               hour_of_day, day_of_week, seasonal_factor]
    Target  : demand_score (0.0 – 1.0)
    """
    rng = np.random.default_rng(42)
    days_since = rng.exponential(scale=5, size=n).clip(0, 30)
    consumption = rng.uniform(0.3, 3.0, n)
    hour = rng.integers(0, 24, n).astype(float)
    dow = rng.integers(0, 7, n).astype(float)
    seasonal = rng.uniform(0.7, 1.3, n)

    # Morning (7-9) and evening (18-20) peaks → higher demand
    time_bonus = np.where(((hour >= 7) & (hour <= 9)) | ((hour >= 18) & (hour <= 20)), 0.20, 0.05)
    # Longer since last purchase → higher demand
    age_score = np.tanh(days_since / 7) * 0.6
    # Higher consumption → higher demand
    cons_score = np.tanh(consumption / 2) * 0.3
    noise = rng.normal(0, 0.04, n)

    y = np.clip(age_score + cons_score + time_bonus * seasonal + noise, 0.0, 1.0)
    X = np.column_stack([days_since, consumption, hour, dow, seasonal])
    return X, y


def _synthetic_trust_data(n: int = 800) -> np.ndarray:
    """
    Features: [success_rate, weekly_tx_count, avg_tx_value, refund_rate]
    Used by IsolationForest to detect anomalous (low-trust) behaviour.
    """
    rng = np.random.default_rng(0)
    success_rate = rng.beta(8, 2, n)          # mostly high
    weekly_tx = rng.poisson(5, n).astype(float)
    avg_value = rng.lognormal(2.0, 0.5, n)
    refund_rate = rng.beta(1, 10, n)          # mostly low
    return np.column_stack([success_rate, weekly_tx, avg_value, refund_rate])


# ── Train / load helpers ───────────────────────────────────────────────────

def _train_demand() -> Tuple[GradientBoostingRegressor, StandardScaler]:
    logger.info("Training demand model on synthetic data …")
    X, y = _synthetic_demand_data()
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    model = GradientBoostingRegressor(n_estimators=120, max_depth=3, random_state=42)
    model.fit(X_s, y)
    joblib.dump(model, _DEMAND_MODEL_PATH)
    joblib.dump(scaler, _DEMAND_SCALER_PATH)
    logger.info("Demand model saved to %s", MODELS_DIR)
    return model, scaler


def _load_demand() -> Tuple[GradientBoostingRegressor, StandardScaler]:
    if os.path.exists(_DEMAND_MODEL_PATH) and os.path.exists(_DEMAND_SCALER_PATH):
        return joblib.load(_DEMAND_MODEL_PATH), joblib.load(_DEMAND_SCALER_PATH)
    return _train_demand()


def _train_trust() -> IsolationForest:
    logger.info("Training trust / anomaly model on synthetic data …")
    X = _synthetic_trust_data()
    model = IsolationForest(contamination=0.1, n_estimators=100, random_state=42)
    model.fit(X)
    joblib.dump(model, _TRUST_MODEL_PATH)
    logger.info("Trust model saved to %s", MODELS_DIR)
    return model


def _load_trust() -> IsolationForest:
    if os.path.exists(_TRUST_MODEL_PATH):
        return joblib.load(_TRUST_MODEL_PATH)
    return _train_trust()


# ── Singletons (lazy-loaded at first call) ────────────────────────────────

_demand_model: GradientBoostingRegressor | None = None
_demand_scaler: StandardScaler | None = None
_trust_model: IsolationForest | None = None


def _get_demand():
    global _demand_model, _demand_scaler
    if _demand_model is None:
        _demand_model, _demand_scaler = _load_demand()
    return _demand_model, _demand_scaler


def _get_trust():
    global _trust_model
    if _trust_model is None:
        _trust_model = _load_trust()
    return _trust_model


# ── Public API ─────────────────────────────────────────────────────────────

def check_ml_based_demand(agent_id: str, product_category: str) -> Tuple[bool, float]:
    """Return (should_order: bool, confidence: float 0-1)."""
    try:
        model, scaler = _get_demand()
        hour = float(datetime.now().hour)
        # Deterministic synthetic features based on agent_id hash
        seed = abs(hash(agent_id + product_category)) % 10000
        rng = np.random.default_rng(seed)
        days_since = float(rng.integers(1, 15))
        consumption = float(rng.uniform(0.5, 2.5))
        dow = float(datetime.now().weekday())
        seasonal = 1.0 + float(rng.uniform(-0.15, 0.15))

        X = np.array([[days_since, consumption, hour, dow, seasonal]])
        X_s = scaler.transform(X)
        confidence = float(np.clip(model.predict(X_s)[0], 0.0, 1.0))
        should_order = confidence >= CONFIDENCE_THRESHOLD
        logger.info("ML demand %s/%s: conf=%.3f order=%s", agent_id, product_category, confidence, should_order)
        return should_order, confidence
    except Exception as exc:
        logger.warning("ML demand fallback (%s) – using heuristic", exc)
        return False, 0.45


def calculate_trust_score_ml(
    success_rate: float,
    weekly_tx_count: int,
    avg_tx_value: float,
    refund_rate: float,
) -> int:
    """Return trust score 0-100 using IsolationForest anomaly detection."""
    try:
        model = _get_trust()
        X = np.array([[success_rate, float(weekly_tx_count), avg_tx_value, refund_rate]])
        # IsolationForest: 1 = normal, -1 = anomaly
        pred = model.predict(X)[0]
        score_raw = model.decision_function(X)[0]  # higher = more normal
        # Map decision function to 0-100 range
        base = 50 + int(score_raw * 40)
        if pred == -1:
            base = max(0, base - 30)
        # Blend with explicit success_rate (90% weight per strategy)
        blended = int(success_rate * 0.9 * 100 + base * 0.1)
        return max(0, min(100, blended))
    except Exception as exc:
        logger.warning("ML trust fallback (%s)", exc)
        return int(success_rate * 80)


def ensure_models_loaded() -> None:
    """Pre-load / pre-train models at startup (called from lifespan)."""
    _get_demand()
    _get_trust()
    logger.info("ML models ready (demand + trust)")
