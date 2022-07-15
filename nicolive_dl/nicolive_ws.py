#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import asyncio
import logging
import websockets

# wslogger = logging.getLogger('websockets')
# wslogger.setLevel(logging.DEBUG)
# wslogger.addHandler(logging.StreamHandler())
# wslogger.addHandler(logging.FileHandler('log.txt'))
# LogLevelをDEBUGにすると通信情報を表示

class WebSocketApp:
    def __init__(self, uri, **kwargs):
        self.ws = None
        self.uri = uri
        self.option = kwargs

    async def connect(self):
        async with websockets.connect(self.uri, **self.option) as self.ws:
            await self.on_open()
            async for msg in self.ws:
                await self.on_recv(msg)

    async def send(self, data):
        msg = json.dumps(data)
        await self.ws.send(msg)
        await self.on_send(data)

    async def close(self):
        await self.on_close()
        await self.ws.close()

    async def on_open(self): pass
    async def on_send(self, data): pass
    async def on_recv(self, msg): pass
    async def on_close(self): pass


class NicoLiveWS(WebSocketApp):
    def __init__(self, uri, **kwargs):
        super().__init__(uri, **kwargs)
        self.keep_interval_sec = None
        self.stream_uri = None
        self.recv_stream_event = asyncio.Event()
        self.room = None
        self.recv_room_event = asyncio.Event()

    async def on_open(self):
        start_watching = {
            "type": "startWatching",
            "data": {
                "stream": {
                    "quality": "super_high",
                    "protocol": "hls",
                    "latency": "low",
                    "chasePlay": False
                },
                "room": {
                    "protocol": "webSocket",
                    "commentable": True
                },
                "reconnect": True
            }
        }
        await self.send(start_watching)

    async def on_recv(self, msg):
        data = json.loads(msg)
        if not isinstance(data, dict):
            return
        t = data.get('type')
        if t == 'ping':
            asyncio.create_task(self.pong())
        elif t == 'seat':
            asyncio.create_task(self.heart_start(data))
        elif t == 'stream':
            asyncio.create_task(self.recv_stream(data))
        elif t == 'room':
            asyncio.create_task(self.recv_room(data))

    async def pong(self):
        await self.send({"type": "pong"})

    async def heart_start(self, data):
        if self.keep_interval_sec:
            return
        self.keep_interval_sec = data['data']['keepIntervalSec']
        next_time = time.time()
        while True:
            await self.send({"type": "keepSeat"})
            next_time += self.keep_interval_sec
            await asyncio.sleep(max(next_time - time.time(), 0))

    async def recv_stream(self, data):
        self.stream_uri = data['data']['uri']
        self.recv_stream_event.set()

    async def wait_for_stream(self):
        await self.recv_stream_event.wait()
        return self.stream_uri
    
    async def recv_room(self, data):
        self.room = data
        self.recv_room_event.set()

    async def wait_for_room(self):
        await self.recv_room_event.wait()
        return self.room

class NicoLiveCommentWS(WebSocketApp):
    def __init__(self, room_event, comment_path, **kwargs):
        uri = room_event['data']['messageServer']['uri']
        super().__init__(uri, **kwargs)
        self.roomEvent = room_event
        self.commentPath = comment_path
        asyncio.create_task(self.heart_start())

    async def on_open(self):
        message = [{"ping": {"content": "rs:0"}}, {"ping": {"content": "ps:0"}}, {
            "thread": {"thread": self.roomEvent['data']['threadId'], "version": "20061206", "user_id": "10000",
                       "res_from": -150, "with_global": 1, "scores": 1, "nicoru": 0,
                       "threadkey": self.roomEvent['data']['yourPostKey']}},
                   {"ping": {"content": "pf:0"}}, {"ping": {"content": "rf:0"}}]
        await self.send(message)

    async def heart_start(self):
        await asyncio.sleep(60)
        next_time = time.time()
        while True:
            await self.send('')
            next_time += 60
            await asyncio.sleep(max(next_time - time.time(), 0))

    async def on_recv(self, msg):
        open(self.commentPath, 'a', encoding='utf-8').write(msg + '\n')
