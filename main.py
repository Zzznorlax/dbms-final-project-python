import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.users import router as user_router
from app.api.v1.products import router as product_router
from app.api.v1.orders import router as order_router
from app.api.v1.images import router as image_router
from app.utils.config import get_settings
from app.database.base import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user_router, prefix="/users")
app.include_router(product_router, prefix="/products")
app.include_router(order_router, prefix="/orders")
app.include_router(image_router, prefix="/images")


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
