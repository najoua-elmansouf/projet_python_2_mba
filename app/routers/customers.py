from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.core.dataset import load_transactions_enriched, load_users
from app.services import customer_service as cs

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("")
def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=200),
) -> dict[str, Any]:
    users = load_users()
    return cs.list_customers(users, page, limit)


@router.get("/top")
def top_customers(n: int = Query(10, ge=1, le=100)) -> list[dict[str, Any]]:
    tx = load_transactions_enriched()
    out = cs.top_customers(tx, n)
    if out is None:
        raise HTTPException(
            status_code=501,
            detail="No customer column found in transactions_data.csv",
        )
    return out


@router.get("/{customer_id}")
def customer_profile(customer_id: str) -> dict[str, Any]:
    tx = load_transactions_enriched()
    out = cs.customer_profile(tx, customer_id)
    if out is None:
        raise HTTPException(
            status_code=501,
            detail="No customer column found in transactions_data.csv",
        )
    return out
