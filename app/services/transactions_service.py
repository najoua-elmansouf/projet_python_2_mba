from __future__ import annotations

from typing import Any, Optional, cast

import pandas as pd


def get_type_column(df: pd.DataFrame) -> str | None:
    """Return the column name used as 'transaction type' in the dataset."""
    if "type" in df.columns:
        return "type"
    if "use_chip" in df.columns:
        return "use_chip"
    return None


def df_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Convert DataFrame to JSON-safe records:
    - replace NaN/NA with None
    - cast for mypy
    """
    cleaned = df.astype(object).mask(pd.isna(df), None)
    records_any = cleaned.to_dict(orient="records")
    return cast(list[dict[str, Any]], records_any)


def filter_transactions(
    df: pd.DataFrame,
    tx_type: Optional[str] = None,
    type_col: Optional[str] = None,
    is_fraud: Optional[int] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
) -> pd.DataFrame:
    """Apply filters to the transactions dataframe."""
    out = df

    if tx_type is not None and type_col is not None and type_col in out.columns:
        out = out[out[type_col] == tx_type]

    if is_fraud is not None and "isFraud" in out.columns:
        out = out[out["isFraud"] == int(is_fraud)]

    if min_amount is not None and "amount" in out.columns:
        out = out[out["amount"] >= float(min_amount)]

    if max_amount is not None and "amount" in out.columns:
        out = out[out["amount"] <= float(max_amount)]

    return out


def paginate(df: pd.DataFrame, page: int, limit: int) -> pd.DataFrame:
    """Return a slice of df using page/limit."""
    start = (page - 1) * limit
    end = start + limit
    return df.iloc[start:end]


def get_by_id(df: pd.DataFrame, tx_id: str) -> pd.DataFrame:
    """Return df slice with one transaction by id."""
    if "id" not in df.columns:
        return df.iloc[0:0]
    return df[df["id"] == str(tx_id)]


def by_customer(df: pd.DataFrame, customer_id: int) -> pd.DataFrame:
    """Return transactions for one customer (client_id)."""
    if "client_id" not in df.columns:
        return df.iloc[0:0]
    return df[df["client_id"] == int(customer_id)]


def search(
    df: pd.DataFrame,
    body: dict[str, Any],
    type_col: str | None,
) -> pd.DataFrame:
    """Search multi-critères using request body."""
    out = df

    tx_type = body.get("type")
    if tx_type is not None and type_col is not None:
        out = out[out[type_col] == tx_type]

    is_fraud = body.get("isFraud")
    if is_fraud is not None and "isFraud" in out.columns:
        out = out[out["isFraud"] == int(is_fraud)]

    amount_min = body.get("amount_min")
    if amount_min is not None and "amount" in out.columns:
        out = out[out["amount"] >= float(amount_min)]

    amount_max = body.get("amount_max")
    if amount_max is not None and "amount" in out.columns:
        out = out[out["amount"] <= float(amount_max)]

    client_id = body.get("client_id")
    if client_id is not None and "client_id" in out.columns:
        out = out[out["client_id"] == int(client_id)]

    card_id = body.get("card_id")
    if card_id is not None and "card_id" in out.columns:
        out = out[out["card_id"] == int(card_id)]

    merchant_id = body.get("merchant_id")
    if merchant_id is not None and "merchant_id" in out.columns:
        out = out[out["merchant_id"] == int(merchant_id)]

    return out
