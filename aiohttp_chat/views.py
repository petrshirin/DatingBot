from aiohttp import web, WSMsgType
from aiohttp_session import get_session, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from datetime import datetime, timezone, timedelta
import json
import logging
from .models import *


DEFAULT_TIME_ZONE = timezone(timedelta(hours=3))

LOG = logging.getLogger(__name__)


async def websocket_handler(request):
    session = await get_session(request)
    session['last_visit'] = datetime.now(tz=DEFAULT_TIME_ZONE).time()
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                i = 0
                for ws_n in request.app['wslist']:
                    if ws_n['chat_id'] == session['chat_id']:
                        ws_n.pop(i)
                        break
                    i += 1

                await ws.close()
            else:
                json_d = json.loads(msg.data)
                print(json_d)
                if json_d['text'] == '|open|':
                    if not session.get('token'):
                        async with request.app['pool'].acquire() as con:
                            tokens = ChatToken(con)
                            await tokens.get_all()
                            is_valid_token = False
                            for token in tokens.all_tokens:
                                if token.token == json_d['token']:
                                    is_valid_token = True
                                    session['token'] = json_d['token']
                                    if not session.get('chat_id'):
                                        session['chat_id'] = json_d['chat_id']
                                    request.app['wslist'].append({'ws': ws, 'chat_id': json_d['chat_id'], 'partner_id': json_d['partner_id']})
                            if not is_valid_token:
                                await ws.close()
                                return ws

                    answer = {
                        "chat_id": json_d['chat_id'],
                        "text": '|open|',
                    }
                    await ws.send_json(answer)
                else:
                    if not session.get('token'):
                        await ws.close()
                    print(request.app['wslist'])

                    answer = {
                        "chat_id": json_d['chat_id'],
                        'text': json_d['text'],
                        "time": datetime.now(tz=DEFAULT_TIME_ZONE).time().strftime('%H:%M')
                    }
                    async with request.app['pool'].acquire() as con:
                        new_message = ChatMessage(con, session['chat_id'], answer['chat_id'], answer['text'], datetime.now(tz=DEFAULT_TIME_ZONE))
                        await new_message.save()

                    for ws_n in request.app['wslist']:

                        if ws_n['chat_id'] == json_d['chat_id'] and ws_n['partner_id'] == session['chat_id']:
                            await ws_n['ws'].send_json(answer)

        elif msg.type == WSMsgType.ERROR:
            i = 0
            for ws_n in request.app['wslist']:
                if ws_n['chat_id'] == session['chat_id']:
                    ws_n.pop(i)
                    break
                i += 1
            print('ws connection closed with exception %s' %
                      ws.exception())

    print('websocket connection closed')

    return ws
