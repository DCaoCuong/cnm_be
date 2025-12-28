from fastapi import FastAPI
from app.core.middleware import AuthMiddleware,TraceIdMiddleware
from app.routers.v1.vouchers import router as vouchers_router
# from app.routers.v1.auth import router as auth_router

app = FastAPI(
    title="WebMyPham API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# middleware
app.add_middleware(TraceIdMiddleware) 
app.add_middleware(AuthMiddleware)

# routers
# app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(vouchers_router, prefix="/api/v1/vouchers", tags=["vouchers"])


@app.get("/")
def health_check():
    return {"status": "ok"}
