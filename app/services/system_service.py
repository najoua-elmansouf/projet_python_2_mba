from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

START_TIME = datetime.now(timezone.utc)


def health(dataset_loaded: bool) -> dict[str, Any]:
    uptime = datetime.now(timezone.utc) - START_TIME
    return {"status": "ok", "uptime": str(uptime), "dataset_loaded": dataset_loaded}


def metadata(version: str) -> dict[str, str]:
    return {"version": version, "last_update": datetime.now(timezone.utc).isoformat()}
