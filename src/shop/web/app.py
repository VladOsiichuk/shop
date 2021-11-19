from typing import Callable

from fastapi import FastAPI

from src.shop.containers import Container, bootstrap
from src.shop.orders.views import router as order_router
from src.shop.products.views import router as product_router


def create_app(container_bootstrap: Callable[[], Container] = bootstrap) -> FastAPI:
    container = container_bootstrap()
    app = FastAPI(debug=container.config.debug)
    app.include_router(router=product_router, prefix="/api/products")
    app.include_router(router=order_router, prefix="/api/orders")
    return app
