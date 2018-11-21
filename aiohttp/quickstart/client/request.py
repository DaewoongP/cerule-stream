import aiohttp
import asyncio


async def getcor():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get') as response:
            print(response.status)
            print(await response.text())


async def postcor():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://httpbin.org/post', data=b'data') as response:
            print(response.status)
            print(await response.text())

loop = asyncio.get_event_loop()
loop.run_until_complete(getcor())
loop.run_until_complete(postcor())
loop.close()