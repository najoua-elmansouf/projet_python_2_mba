from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import json

import pandas as pd

import os
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))

FILES = {
    "transactions": DATA_DIR / "transactions_data.csv",
    "users": DATA_DIR / "users_data.csv",
    "cards": DATA_DIR / "cards_data.csv",
    "fraud_labels": DATA_DIR / "train_fraud_labels.json",
    "mcc": DATA_DIR / "mcc_codes.json",
}

_CACHE: Dict[str, pd.DataFrame] = {}
_META: Dict[str, Any] = {"dataset_loaded": False}


def _require(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")


def _parse_amount(x: Any) -> float:
    """
    Convert amounts like '$14.57', '$80.00 ', '($77.00)' to float.
    Parentheses mean negative.
    Also handles '$-77.00'
    """
    s = str(x).strip()
    if not s or s.lower() == "nan":
        return 0.0

    neg_paren = s.startswith("(") and s.endswith(")")
    s = s.replace("(", "").replace(")", "")
    s = s.replace("$", "").replace(",", "").strip()

    try:
        val = float(s)
        return -val if neg_paren else val
    except ValueError:
        return 0.0


def _labels_to_df(labels_raw: Any) -> pd.DataFrame:
    """
    Your labels json format:
        {"target": {"10649266": "No", "23410063": "Yes", ...}}

    Converts to DataFrame columns: id(str), isFraud(int 0/1)
    """
    mapping = labels_raw.get("target", labels_raw) if isinstance(labels_raw, dict) else labels_raw

    def to_int(v: Any) -> int:
        s = str(v).strip().lower()
        return 1 if s in {"yes", "true", "fraud", "1"} else 0

    if isinstance(mapping, dict):
        return pd.DataFrame([{"id": str(k), "isFraud": to_int(v)} for k, v in mapping.items()])

    return pd.DataFrame(columns=["id", "isFraud"])


def load_transactions_enriched() -> pd.DataFrame:
    """
    Load transactions and merge fraud labels to create `isFraud`.
    Cached in memory for performance.
    """
    if "transactions_enriched" in _CACHE:
        return _CACHE["transactions_enriched"]

    _require(FILES["transactions"])
    _require(FILES["fraud_labels"])

    tx = pd.read_csv(FILES["transactions"])

    # Ensure id exists
    if "id" not in tx.columns:
        tx["id"] = tx.index.astype(str)
    tx["id"] = tx["id"].astype(str)

    # Parse date if present (optional but nice)
    if "date" in tx.columns:
        tx["date"] = pd.to_datetime(tx["date"], errors="coerce")

    # Convert amount to float
    if "amount" in tx.columns:
        tx["amount"] = tx["amount"].apply(_parse_amount)

    # Load fraud labels and convert
    with open(FILES["fraud_labels"], "r", encoding="utf-8") as f:
        labels_raw = json.load(f)

    labels = _labels_to_df(labels_raw)

    if labels.empty or "id" not in labels.columns or "isFraud" not in labels.columns:
        tx["isFraud"] = 0
        df = tx
    else:
        labels["id"] = labels["id"].astype(str)
        labels["isFraud"] = labels["isFraud"].astype(int)
        df = tx.merge(labels[["id", "isFraud"]], on="id", how="left")
        df["isFraud"] = df["isFraud"].fillna(0).astype(int)

    _CACHE["transactions_enriched"] = df
    _META["dataset_loaded"] = True
    return df


def load_users() -> pd.DataFrame:
    if "users" in _CACHE:
        return _CACHE["users"]

    _require(FILES["users"])
    df = pd.read_csv(FILES["users"])
    if "id" in df.columns:
        df["id"] = df["id"].astype(str)

    _CACHE["users"] = df
    return df


def load_cards() -> pd.DataFrame:
    if "cards" in _CACHE:
        return _CACHE["cards"]

    _require(FILES["cards"])
    df = pd.read_csv(FILES["cards"])

    if "client_id" in df.columns:
        df["client_id"] = df["client_id"].astype(str)
    if "id" in df.columns:
        df["id"] = df["id"].astype(str)

    _CACHE["cards"] = df
    return df


def dataset_loaded() -> bool:
    return bool(_META.get("dataset_loaded", False))
