import asyncio
import aiohttp
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from .views import *
from envparse import env
from asyncpg import create_pool
import os

env.read_envfile('.env')

routes = [
    web.get('/', handler),
    web.get('/ws', websocket_handler)
]


async def init():
    app = web.Application()
    setup(app, EncryptedCookieStorage(bytes(os.environ.get('ENCRYPTED_COOKIE_STORAGE_KEY'))))
    app.add_routes(routes)
    app['wslist'] = []
    app['pool'] = await create_pool(f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASS")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}')
    return app


async def run_app():
    web.run_app(init(), host='127.0.0.1', port=8081)

