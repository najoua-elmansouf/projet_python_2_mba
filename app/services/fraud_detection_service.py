from __future__ import annotations

from typing import Any

import pandas as pd


def get_type_column(df: pd.DataFrame) -> str | None:
    if "type" in df.columns:
        return "type"
    if "use_chip" in df.columns:
        return "use_chip"
    return None


def summary(df: pd.DataFrame) -> dict[str, Any]:
    total_frauds = int(df["isFraud"].sum()) if "isFraud" in df.columns else 0
    return {"total_frauds": total_frauds, "flagged": 0, "precision": 0.0, "recall": 0.0}


def by_type(df: pd.DataFrame) -> list[dict[str, Any]]:
    tcol = get_type_column(df)
    if tcol is None or "isFraud" not in df.columns:
        return []
    g = df.groupby(tcol)["isFraud"].mean().reset_index()
    return [{"type": str(r[tcol]), "fraud_rate": float(r["isFraud"])} for _, r in g.iterrows()]


def predict(tx_type: str | None, amount: float | None) -> dict[str, Any]:
    amt = float(amount or 0.0)
    t = (tx_type or "").upper()

    prob = 0.05
    if amt > 5000:
        prob += 0.25
    if t in {"TRANSFER", "CASH_OUT"}:
        prob += 0.25
    prob = max(0.0, min(0.99, prob))

    return {"isFraud": prob >= 0.5, "probability": prob}
