#!/usr/bin/env python3

import asyncio as aio
import websockets
import serial
import json

# import sys
# import functools


DEVICE = '/dev/cu.usbmodem1421' # Maskinen
# DEVICE = '/dev/cu.usbserial-A6004b7d' # Hemma

ser = serial.Serial(DEVICE, timeout=1)  # open serial port with 1s timeout
print(ser.name)         # check which port was really used

# Test function when not using aruino
# class Prompt:
    # def __init__(self, loop=None):
        # self.loop = loop or aio.get_event_loop()
        # self.q = aio.Queue(loop=self.loop)
        # self.loop.add_reader(sys.stdin, self.got_input)

    # def got_input(self):
        # aio.ensure_future(self.q.put(sys.stdin.readline()), loop=self.loop)

    # async def __call__(self, msg, end='\n', flush=False):
        # print(msg, end=end, flush=flush)
        # return (await self.q.get()).rstrip('\n')

# prompt = Prompt()
# raw_input = functools.partial(prompt, end='', flush=True)

@aio.coroutine
def serInput():
    while True:
        yield from aio.sleep(0)
        x = ser.readline()          # read one line
        msg = json.dumps({'action': x.decode('ascii')})
        if (x != b''):
            return msg


# # WebSockets server

connected = set()

@aio.coroutine
def wshandler(websocket, path):
    global connected
    connected.add(websocket)
    print(connected)

    while True:
        msg = yield from serInput()
        print(msg)
        for client in connected:
            try:
                yield from client.send(msg)
            except websockets.exceptions.ConnectionClosed:
                pass



start_server = websockets.serve(wshandler, 'localhost', 8765)

loop = aio.get_event_loop()


aio.get_event_loop().run_until_complete(start_server)
aio.get_event_loop().run_forever()

