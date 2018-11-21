from time import time
from urllib.request import Request, urlopen
import asyncio

urls = ['https://www.google.co.kr/search?=q' + i
        for i in ['apple', 'pear', 'grape', 'pineapple', 'orange', 'strawberry']]


async def fetch(url):
    request = Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'referer': 'https://www.google.co.kr/'
    })
    response = await loop.run_in_executor(None, urlopen, request)
    page = await loop.run_in_executor(None, response.read)
    return len(page)


async def main():
    # Make asyncio.Task Object Array
    futures = [asyncio.ensure_future(fetch(url)) for url in urls]
    result = await asyncio.gather(*futures)
    print(result)

begin = time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
end = time()
print('execution time: {0:.3f}sec'.format(end-begin))
