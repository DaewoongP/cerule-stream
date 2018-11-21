from time import time
from urllib.request import Request, urlopen

urls = ['https://www.google.co.kr/search?q=' + i
        for i in ['apple', 'pear', 'grape', 'pineapple', 'orange', 'strawberry']]

begin = time()
result = []
for url in urls:
    request = Request(url,
                      headers={
                          'User-Agent': 'Mozilla/5.0',
                          'referer': 'https://www.google.co.kr/'
                      })
    # Having 403 Errors, without UA
    response = urlopen(request)
    page = response.read()
    result.append(len(page))

print(result)
end = time()
print('execution time: {0:.3f}sec'.format(end-begin))
