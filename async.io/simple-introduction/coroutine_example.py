import asyncio


# definition of a coroutine
async def coroutine_1():
    print('coroutine_1 is active on the event loop')

    print('coroutine_1 yielding control. Goint to be blocked for 4 seconds')
    await asyncio.sleep(4)

    print('coroutine_1 resumed. coroutine_1 exiting')


async def coroutine_2():
    print('coroutine_2 is active on the event loop')

    print('coroutine_2 yielding control. Goint to be blocked for 2 seconds')
    await asyncio.sleep(2)

    print('coroutine_2 resumed. coroutine_2 exiting')

task1 = asyncio.ensure_future(coroutine_1())
task2 = asyncio.ensure_future(coroutine_2())

loop = asyncio.get_event_loop()
loop.run_until_complete(task1)
loop.run_until_complete(task2)
loop.close()

