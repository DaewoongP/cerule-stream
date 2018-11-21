import asyncio


async def hello():
    print('Hello, async.io!')

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()