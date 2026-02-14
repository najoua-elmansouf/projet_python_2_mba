from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.core.dataset import dataset_loaded
from app.services import system_service as sys_svc

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/health")
def health() -> dict[str, Any]:
    return sys_svc.health(dataset_loaded())


@router.get("/metadata")
def metadata() -> dict[str, str]:
    return sys_svc.metadata("1.0.0")
