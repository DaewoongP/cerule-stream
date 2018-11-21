from aiohttp import web
import json

async def hello(request):
    return web.Response(text="Hello, world")

async def variable_handler(request):
    return web.Response(
        text="Hello, {}".format(request.match_info['name'])
    )

class Handler:
    def __init__(self):
        pass

    async def handle_intro(self, request):
        return web.Response(text="Hello, world")

    async def handle_greeting(self, request):
        name = request.match_info.get('name', "Anonymous")
        txt = "Hello, {}".format(name)
        return web.Response(text=txt)



handler = Handler()
app = web.Application()
app.add_routes([web.get('/intro', handler.handle_intro),
                web.get('/greet/{name}', handler.handle_greeting)
                ])


async def handle_get(request):
    return web.json_response(json.dumps(request.data))


async def handle_post(request):
    return web.json_response(json.dumps(request))

app.router.add_routes([web.get('/get', handle_get),
                       web.post('/post', handle_post)])

web.run_app(app)
