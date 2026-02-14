from __future__ import annotations

from typing import Any

import pandas as pd


def find_customer_column(df: pd.DataFrame) -> str | None:
    for col in ["client_id", "user_id", "customer_id", "nameOrig"]:
        if col in df.columns:
            return col
    return None


def list_customers(users: pd.DataFrame, page: int, limit: int) -> dict[str, Any]:
    if "id" not in users.columns:
        return {"page": page, "customers": []}

    ids: list[str] = users["id"].astype(str).tolist()
    start = (page - 1) * limit
    end = start + limit
    return {"page": page, "customers": ids[start:end]}


def customer_profile(tx: pd.DataFrame, customer_id: str) -> dict[str, Any] | None:
    col = find_customer_column(tx)
    if col is None:
        return None

    t = tx[tx[col].astype(str) == str(customer_id)]
    count = int(len(t))
    avg_amount = float(t["amount"].mean()) if count > 0 and "amount" in t.columns else 0.0
    fraudulent = bool(int(t["isFraud"].sum()) > 0) if "isFraud" in t.columns else False

    return {
        "id": str(customer_id),
        "transactions_count": count,
        "avg_amount": avg_amount,
        "fraudulent": fraudulent,
    }


def top_customers(tx: pd.DataFrame, n: int) -> list[dict[str, Any]] | None:
    col = find_customer_column(tx)
    if col is None:
        return None
    if "amount" not in tx.columns:
        return []

    g = tx.groupby(col)["amount"].sum().sort_values(ascending=False).head(n)
    return [{"customer_id": str(idx), "total_amount": float(val)} for idx, val in g.items()]
