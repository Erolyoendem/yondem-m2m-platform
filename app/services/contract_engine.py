import logging
import json
import re
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.smart_contract import SmartContract
from app.models.agent import Agent
from app.models.product import Product
from app.models.shop import Shop
from app.models.transaction import Transaction
from app.database.session import SessionLocal
from app.services.ml_predictor import check_ml_based_demand
from app.services.trust_scorer import update_trust_score

logger = logging.getLogger("yondem")

def parse_condition(condition_str):
    match = re.match(r"(\w+)\s*(<|>|<=|>=|==|!=)\s*([\d.]+)", condition_str)
    if match:
        field, operator, value = match.groups()
        return field, operator, float(value)
    return None, None, None

def find_best_product(db, product_name, max_price):
    products = db.query(Product).filter(
        func.lower(Product.name).contains(func.lower(product_name)),
        Product.price <= max_price
    ).order_by(Product.price.asc()).all()
    
    if not products:
        return None
    
    best = products[0]
    logger.info(f"Found product: {best.name} at {best.price}€")
    return best

def calculate_commission(product_price, commission_rate=0.10):
    commission = product_price * commission_rate
    platform_fee = commission * 0.20
    publisher_commission = commission - platform_fee
    return publisher_commission, platform_fee

def create_transaction(db, contract, product, publisher, shop):
    publisher_commission, platform_fee = calculate_commission(product.price)
    
    transaction = Transaction(
        id=str(uuid.uuid4()),
        publisher_id=publisher.id,
        advertiser_id=shop.agent_id if shop else product.shop_id,
        product_id=product.id,
        contract_id=contract.id,
        product_price=product.price,
        commission_amount=publisher_commission,
        platform_fee=platform_fee,
        status="completed"
    )
    
    db.add(transaction)
    publisher.commission_earned_total += publisher_commission
    publisher.performance_score = min(1.0, publisher.performance_score + 0.01)
    
    # Update Trust Score nach erfolgreicher Transaktion
    new_trust = update_trust_score(publisher.id)
    logger.info(f"Trust Score updated: {new_trust}")
    
    db.commit()
    logger.info(f"TRANSACTION: {transaction.id} - Provision: {publisher_commission:.2f}€")
    return transaction

def execute_purchase(db, contract, product, ml_confidence=None):
    logger.info(f"PURCHASE: Contract {contract.id} -> Product {product.id}")
    
    # Trust-Score Check (nur kaufen wenn Trust > 30)
    publisher = db.query(Agent).filter(Agent.id == contract.agent_id).first()
    if publisher and publisher.trust_level < 30:
        logger.warning(f"Trust Score too low: {publisher.trust_level}")
        return False
    
    if contract.spent_this_month + product.price > contract.monthly_budget:
        logger.warning(f"Budget limit reached")
        return False
    
    if not publisher:
        return False
    
    shop = db.query(Shop).filter(Shop.id == product.shop_id).first()
    
    if ml_confidence:
        logger.info(f"ML Confidence: {ml_confidence:.2f}")
    
    create_transaction(db, contract, product, publisher, shop)
    
    contract.execution_count += 1
    contract.success_count += 1
    contract.spent_this_month += product.price
    contract.last_executed = func.now()
    
    db.commit()
    logger.info(f"PURCHASE COMPLETED: {product.name} for {product.price}€")
    return True

def check_all_contracts():
    db = SessionLocal()
    try:
        active_contracts = db.query(SmartContract).filter(SmartContract.is_active == 1).all()
        logger.info(f"Checking {len(active_contracts)} contracts with ML + Trust")
        for contract in active_contracts:
            rules = contract.rules
            if isinstance(rules, str):
                rules = json.loads(rules)
            process_contract_rules(db, contract, rules)
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        db.close()

def process_contract_rules(db, contract, rules):
    product_name = rules.get("product")
    condition = rules.get("condition")
    max_price = rules.get("max_price", float("inf"))
    
    if not product_name or not condition:
        return
    
    should_order, confidence = check_ml_based_demand(contract.agent_id, product_name)
    
    logger.info(f"Contract {contract.id}: {product_name} - ML: {confidence:.2f}")
    
    if should_order:
        product = find_best_product(db, product_name, max_price)
        if product:
            execute_purchase(db, contract, product, ml_confidence=confidence)
        else:
            logger.info(f"No product found under {max_price}€")
    else:
        logger.info(f"ML: No demand detected for {product_name}")
