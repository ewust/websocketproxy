

import asyncio
import websockets
import json
import aiohttp

@asyncio.coroutine
def get_content(url):
    response = yield from aiohttp.request('GET', url)

    data = yield from response.read()

    headers = {k: response.headers[k] for k in response.headers.keys()}
    return headers, data

@asyncio.coroutine
def hello(websocket, path):

    while True:
        msg = yield from websocket.recv()
        if msg is None:
            break
        obj = json.loads(msg)
        url = obj['url']

        headers, data = yield from get_content(url)
        ret_obj = {'headers': headers, 'data': str(data,'utf8')}

        yield from websocket.send(json.dumps(ret_obj))


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
