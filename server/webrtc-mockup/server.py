import aiohttp
from aiohttp import web
import json

from aiortc import (RTCPeerConnection, RTCIceCandidate, RTCSessionDescription,
                    VideoStreamTrack)

from aiortc.contrib.media import MediaPlayer
from aiortc.contrib.signaling import object_from_string, object_to_string

pc = RTCPeerConnection()


async def WebRTCSignalingService(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            params = json.loads(msg.data)
            print(type(params))
            print(params)

            if params["what"] == "call":
                print("call received")
                # prepare media
                pc.addTrack(VideoStreamTrack)
                await pc.setLocalDescription(await pc.createOffer())
                uv4l_sdp = object_to_string(pc.localDescription)
                print(type(uv4l_sdp))
                await ws.send_str(json.dumps({
                    "what": "offer",
                    "data": uv4l_sdp
                }))

            elif params["what"] == "answer":
                print("answer received")
                local_sdp = object_from_string(params["data"])
                await pc.setRemoteDescription(local_sdp)
                print('setRemoteDescription(<local_sdp>)')
                # await pc.setRemoteDescription(local_sdp)

            elif params["what"] == "addIceCandidate":
                print("addIceCandidate received")
            elif params['what'] == 'hangup':
                print("hangup received")
                await ws.close()
            else:
                await ws.send_json(msg.data + '\n received.')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

app = web.Application()
app.add_routes([web.get('/stream/webrtc', WebRTCSignalingService)])
web.run_app(app)