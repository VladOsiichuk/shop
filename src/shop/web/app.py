from typing import Callable

from aiohttp.web import Application
from shop.containers import  bootstrap
from shop.containers import Container


async def create_app(bootstrap: Callable[[], Container] = bootstrap) -> Application:
    container = bootstrap()
    app = Application(debug=container.config.debug)
    return app
