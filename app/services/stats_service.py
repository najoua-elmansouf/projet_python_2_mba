from __future__ import annotations

from typing import Any

import pandas as pd


def get_type_column(df: pd.DataFrame) -> str | None:
    if "type" in df.columns:
        return "type"
    if "use_chip" in df.columns:
        return "use_chip"
    return None


def overview(df: pd.DataFrame) -> dict[str, Any]:
    total = int(len(df))
    fraud_rate = float(df["isFraud"].mean()) if total > 0 and "isFraud" in df.columns else 0.0
    avg_amount = float(df["amount"].mean()) if total > 0 and "amount" in df.columns else 0.0

    tcol = get_type_column(df)
    most_common: str | None = None
    if tcol is not None and not df[tcol].dropna().empty:
        most_common = str(df[tcol].mode().iloc[0])

    return {
        "total_transactions": total,
        "fraud_rate": fraud_rate,
        "avg_amount": avg_amount,
        "most_common_type": most_common,
    }


def amount_distribution(df: pd.DataFrame) -> dict[str, Any]:
    if "amount" not in df.columns:
        return {"bins": [], "counts": []}

    bins = [0, 100, 500, 1000, 5000, 1_000_000_000]
    labels = ["0-100", "100-500", "500-1000", "1000-5000", "5000+"]

    cats = df["amount"].clip(lower=0)
    binned = pd.cut(cats, bins=bins, labels=labels, include_lowest=True)

    counts = binned.value_counts().reindex(labels, fill_value=0).tolist()
    return {"bins": labels, "counts": counts}


def by_type(df: pd.DataFrame) -> list[dict[str, Any]]:
    tcol = get_type_column(df)
    if tcol is None or "amount" not in df.columns:
        return []

    g = df.groupby(tcol)["amount"].agg(["count", "mean"]).reset_index()
    return [
        {"type": str(r[tcol]), "count": int(r["count"]), "avg_amount": float(r["mean"])}
        for _, r in g.iterrows()
    ]


def daily(df: pd.DataFrame) -> list[dict[str, Any]]:
    if "date" in df.columns and "amount" in df.columns:
        d = pd.to_datetime(df["date"], errors="coerce").dt.date
        g = df.assign(day=d).dropna(subset=["day"]).groupby("day")["amount"].agg(["count", "mean"]).reset_index()
        return [{"date": str(r["day"]), "count": int(r["count"]), "avg_amount": float(r["mean"])} for _, r in g.iterrows()]

    if "step" in df.columns and "amount" in df.columns:
        g = df.groupby("step")["amount"].agg(["count", "mean"]).reset_index()
        return [{"step": int(r["step"]), "count": int(r["count"]), "avg_amount": float(r["mean"])} for _, r in g.iterrows()]

    return []
