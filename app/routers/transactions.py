from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.core.dataset import load_transactions_enriched
from app.services import transactions_service as txs

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

DELETED_IDS: set[str] = set()  # delete fictif


class TransactionSearchBody(BaseModel):
    type: str | None = None
    isFraud: int | None = None
    amount_min: float | None = None
    amount_max: float | None = None
    client_id: int | None = None
    card_id: int | None = None
    merchant_id: int | None = None


@router.get("")
def list_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=200),
    type: Optional[str] = None,
    isFraud: Optional[int] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
) -> dict[str, Any]:
    df = load_transactions_enriched()
    df2 = df[~df["id"].isin(DELETED_IDS)]

    type_col = txs.get_type_column(df2)

    df2 = txs.filter_transactions(
        df2,
        tx_type=type,
        type_col=type_col,
        is_fraud=isFraud,
        min_amount=min_amount,
        max_amount=max_amount,
    )

    page_df = txs.paginate(df2, page, limit)
    rows = txs.df_to_records(page_df)

    return {"page": page, "transactions": rows}


@router.post("/search")
def search_transactions(body: TransactionSearchBody) -> dict[str, Any]:
    df = load_transactions_enriched()
    df2 = df[~df["id"].isin(DELETED_IDS)]

    type_col = txs.get_type_column(df2)
    df2 = txs.search(df2, body.model_dump(), type_col)

    rows = txs.df_to_records(df2.head(200))
    return {"count": int(len(df2)), "transactions": rows}


@router.get("/by-customer/{customer_id}")
def by_customer(customer_id: int) -> dict[str, Any]:
    df = load_transactions_enriched()
    df2 = df[~df["id"].isin(DELETED_IDS)]

    out = txs.by_customer(df2, customer_id)
    rows = txs.df_to_records(out)

    return {"customer_id": customer_id, "transactions": rows}


@router.get("/to-customer/{customer_id}")
def to_customer(customer_id: int) -> dict[str, Any]:
    return {
        "customer_id": customer_id,
        "transactions": [],
        "note": (
            "Dataset does not include a destination customer field "
            "(only client -> merchant)."
        ),
    }


@router.get("/types")
def list_types() -> dict[str, list[str]]:
    df = load_transactions_enriched()
    type_col = txs.get_type_column(df)

    if type_col is None:
        return {"types": []}

    return {"types": sorted(df[type_col].dropna().unique().tolist())}


@router.get("/recent")
def recent(n: int = Query(10, ge=1, le=200)) -> dict[str, Any]:
    df = load_transactions_enriched()
    df2 = df[~df["id"].isin(DELETED_IDS)]

    rows = txs.df_to_records(df2.tail(n))
    return {"transactions": rows}


@router.get("/{id}")
def get_transaction(id: str) -> dict[str, Any]:
    if id in DELETED_IDS:
        raise HTTPException(status_code=404, detail="Transaction not found")

    df = load_transactions_enriched()
    out = txs.get_by_id(df, id)
    if out.empty:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return txs.df_to_records(out.iloc[0:1])[0]


@router.delete("/{id}")
def delete_fake(id: str) -> dict[str, Any]:
    df = load_transactions_enriched()
    out = txs.get_by_id(df, id)
    if out.empty:
        raise HTTPException(status_code=404, detail="Transaction not found")

    DELETED_IDS.add(str(id))
    return {"deleted": True, "id": str(id)}
