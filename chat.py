from aiohttp_chat.main import init
import asyncio
from aiohttp import web


web.run_app(init(), host='127.0.0.1', port=8081)
