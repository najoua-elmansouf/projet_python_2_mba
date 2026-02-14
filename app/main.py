from fastapi import FastAPI

from app.routers.transactions import router as transactions_router
from app.routers.stats import router as stats_router
from app.routers.fraud import router as fraud_router
from app.routers.customers import router as customers_router
from app.routers.system import router as system_router

app = FastAPI(title="Banking Transactions API", version="1.0.0")

app.include_router(transactions_router)
app.include_router(stats_router)
app.include_router(fraud_router)
app.include_router(customers_router)
app.include_router(system_router)
