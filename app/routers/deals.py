from fastapi import APIRouter, Depends, HTTPException
from typing import List
import psycopg2
from app.database.connection import get_db_connection
from app.dependencies import get_language, get_translation_func
from app.schemas.deals import AgentDeal, DealCreate

router = APIRouter(prefix="/deals", tags=["deals"])

@router.get("/", response_model=List[AgentDeal])
def list_deals(lang: str = Depends(get_language)):
    t = get_translation_func(lang)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM agent_deals ORDER BY created_at DESC")
            deals = cur.fetchall()
            return deals
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail=t("errors.server_error"))
    finally:
        conn.close()


@router.get("/{deal_id}", response_model=AgentDeal)
def get_deal(deal_id: int, lang: str = Depends(get_language)):
    t = get_translation_func(lang)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM agent_deals WHERE id = %s", (deal_id,))
            deal = cur.fetchone()
            if not deal:
                raise HTTPException(status_code=404, detail=t("errors.deal_not_found", deal_id=deal_id))
            return deal
    except psycopg2.Error:
        raise HTTPException(status_code=500, detail=t("errors.server_error"))
    finally:
        conn.close()


@router.post("/", response_model=AgentDeal)
def create_deal(deal: DealCreate, lang: str = Depends(get_language)):
    t = get_translation_func(lang)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO agent_deals (shop_program_id, publisher_agent_id, commission_rate)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (str(deal.shop_program_id), str(deal.publisher_agent_id), deal.commission_rate))
            new_deal = cur.fetchone()
            conn.commit()
            return new_deal
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
