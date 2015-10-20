import asyncio
import websockets
import json

@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://localhost:8765/')
    obj = {'url': 'http://google.com/'}
    yield from websocket.send(json.dumps(obj))
    result = yield from websocket.recv()
    print("server: {}".format(result))
    yield from websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
