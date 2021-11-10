import argparse
import asyncio
import logging
import sys

from aiohttp import web
from shop.web.app import create_app

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    logging.warning("Uvloop is not available")

parser = argparse.ArgumentParser(
    description="Microservice server",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("--migrate", action="store_true", help="Migrate database")
parser.add_argument(
    "--revision", action="store_true", help="Create new migration revision"
)
args = parser.parse_args()


if args.migrate:
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    sys.exit(0)


if args.revision:
    import sys

    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    message = input("Comment revision: ")
    command.revision(alembic_cfg, message, autogenerate=True)
    sys.exit(0)

app = create_app()

if __name__ == "__main__":
    web.run_app(app)
