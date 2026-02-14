from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.dataset import load_transactions_enriched
from app.services import fraud_detection_service as fds

router = APIRouter(prefix="/api/fraud", tags=["fraud"])


class FraudPredictIn(BaseModel):
    type: str | None = None
    amount: float | None = None


@router.get("/summary")
def summary() -> dict[str, Any]:
    df = load_transactions_enriched()
    return fds.summary(df)


@router.get("/by-type")
def fraud_by_type() -> list[dict[str, Any]]:
    df = load_transactions_enriched()
    return fds.by_type(df)


@router.post("/predict")
def predict(body: FraudPredictIn) -> dict[str, Any]:
    return fds.predict(body.type, body.amount)
