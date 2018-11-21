import aiohttp
import asyncio

WEBSOCKET_URI = 'ws://localhost:8080/ws'


async def websocket_coroutine():
    session = aiohttp.ClientSession()
    async with session.ws_connect(WEBSOCKET_URI) as ws:
        print("websocket connected")
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close cmd':
                    await ws.close()
                    break
                else:
                    await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

loop = asyncio.get_event_loop()
loop.run_until_complete(websocket_coroutine())
loop.run_forever()