from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes_defects import router as defects_router
from api.routes_economics import router as economics_router
from api.routes_secure import router as secure_router
from api.routes_tools import router as tools_router
from api.routes_simulation import router as simulation_router

from audit.audit import log_action   # ← ИСПРАВЛЕНО

app = FastAPI(
    title="Pipeline AI Decision Support System",
    version="1.0.0"
)

# ===============================
# API ROUTES
# ===============================

app.include_router(
    defects_router,
    prefix="/api/defects",
    tags=["Defects"]
)

app.include_router(
    economics_router,
    prefix="/api/economics",
    tags=["Economics"]
)

app.include_router(
    secure_router,
    prefix="/api/security",
    tags=["Security"]
)

app.include_router(
    tools_router,
    prefix="/api/tools",
    tags=["Tools"]
)

app.include_router(
    simulation_router,
    prefix="/api/sim",
    tags=["Sim"]
)
# ===============================
# FRONTEND
# ===============================

app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)

# ===============================
# AUDIT LOGGING
# ===============================

@app.middleware("http")
async def audit_middleware(request, call_next):
    response = await call_next(request)

    log_action(
        user=request.client.host if request.client else "unknown",
        action=request.url.path
    )

    return response
