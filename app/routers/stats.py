from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.core.dataset import load_transactions_enriched
from app.services import stats_service as ss

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/overview")
def overview() -> dict[str, Any]:
    df = load_transactions_enriched()
    return ss.overview(df)


@router.get("/amount-distribution")
def amount_distribution() -> dict[str, Any]:
    df = load_transactions_enriched()
    return ss.amount_distribution(df)


@router.get("/by-type")
def by_type() -> list[dict[str, Any]]:
    df = load_transactions_enriched()
    return ss.by_type(df)


@router.get("/daily")
def daily() -> list[dict[str, Any]]:
    df = load_transactions_enriched()
    return ss.daily(df)
