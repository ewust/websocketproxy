

import asyncio
import websockets
import json
import urllib.parse

@asyncio.coroutine
def get_content(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        connect = asyncio.open_connection(url.hostname, 443, ssl=True)
    else:
        connect = asyncio.open_connection(url.hostname, 80)
    reader, writer = yield from connect
    query = ('GET {path} HTTP/1.0\r\n'
             'Host: {hostname}\r\n'
             '\r\n').format(path=url.path or '/', hostname=url.hostname)
    writer.write(query.encode('utf8'))
    buf = b''
    while True:
        tmp = yield from reader.read()
        if not tmp:
            break
        buf += tmp

    # Ignore the body, close the socket
    writer.close()
    return buf


@asyncio.coroutine
def hello(websocket, path):

    while True:
        msg = yield from websocket.recv()
        if msg is None:
            break
        obj = json.loads(msg)
        url = obj['url']

        resp = yield from get_content(url)

        yield from websocket.send(resp)


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
