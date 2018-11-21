import aiohttp
import asyncio
import json
from aiortc import (RTCPeerConnection, RTCSessionDescription, RTCIceCandidate,
                    VideoStreamTrack)
from aiortc.contrib.media import MediaRecorder
from aiortc.contrib.signaling import object_from_string, object_to_string

WEBSOCKET_URI = 'ws://localhost:8080/stream/webrtc'

pc = RTCPeerConnection()
# prefare media
pc.addTrack(VideoStreamTrack)


async def websocket_coroutine():
    session = aiohttp.ClientSession()
    async with session.ws_connect(WEBSOCKET_URI) as ws:
        print("websocket connected")
        request = json.dumps({
            "what": "call"
        })
        await ws.send_str(request)

        async for msg in ws:
            print(msg)
            if msg.type == aiohttp.WSMsgType.TEXT:
                params = json.loads(msg.data)
                print(params)
                if params["what"] == "offer":
                    print("offer received")
                    uv4l_sdp = object_from_string(params["data"])
                    await pc.setRemoteDescription(uv4l_sdp)
                    await pc.setLocalDescription(await pc.createAnswer())
                    local_sdp = object_to_string(pc.localDescription)
                    print(local_sdp)
                    print(type(local_sdp))
                    await ws.send_str(json.dumps({
                        "what": "answer",
                        "data": local_sdp
                    }))

                elif params['what'] == 'hangup':
                    print("hangup received")
                    await ws.close()
                    break
                else:
                    print(msg)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

loop = asyncio.get_event_loop()
loop.run_until_complete(websocket_coroutine())
loop.run_forever()