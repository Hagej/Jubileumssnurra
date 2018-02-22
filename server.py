#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
import asyncio as aio
import websockets
import serial
import json

import sys
import functools


# Serial
# s = serial.Serial('')

DEVICE = '/dev/cu.usbmodem1421'

# ser = serial.Serial(DEVICE, timeout=1)  # open serial port with 1s timeout
# print(ser.name)         # check which port was really used

class Prompt:
    def __init__(self, loop=None):
        self.loop = loop or aio.get_event_loop()
        self.q = aio.Queue(loop=self.loop)
        self.loop.add_reader(sys.stdin, self.got_input)

    def got_input(self):
        aio.ensure_future(self.q.put(sys.stdin.readline()), loop=self.loop)

    async def __call__(self, msg, end='\n', flush=False):
        print(msg, end=end, flush=flush)
        return (await self.q.get()).rstrip('\n')

prompt = Prompt()
raw_input = functools.partial(prompt, end='', flush=True)



# # WebSockets server

connected = set()

# async def handler(websocket, path):
    # global connected
    # # Register.
    # connected.add(websocket)
    # try:
        # # Implement logic here.
        # await aio.wait([ws.send("Hello!") for ws in connected])
        # await aio.sleep(10)
    # finally:
        # # Unregister.
        # connected.remove(websocket)

async def wshandler(websocket, path):
    global connected
    connected.add(websocket)
    print(connected)

    while True:
        await prompt("press enter")
        msg = json.dumps({'action': 'Forward\r\n'})
        for client in connected:
            try:
                await client.send(msg)
            except websockets.exceptions.ConnectionClosed:
                pass
        # pass
        # websocket.send("Hej")
        # x = ser.readline()          # read one line
        # msg = json.dumps({'action': x.decode('ascii')})
        # if (x != b''):
            # for ws in connected:
                # await ws.send(msg)
            # print(x)

async def main():
    global connected
    while True:
        await prompt("press enter")
        msg = json.dumps({'action': 'Forward\r\n'})
        for client in connected:
            try:
                await client.send(msg)
            except websockets.exceptions.ConnectionClosed:
                pass

start_server = websockets.serve(wshandler, 'localhost', 8765)

aio.ensure_future(start_server)
aio.get_event_loop().run_until_complete(main())
# aio.get_event_loop().run_until_complete(start_server)
print("hellp")
aio.get_event_loop().run_forever()


# HTTP server
# PORT = 8000

# def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    # server_address = ('localhost', 8000)
    # httpd = server_class(server_address, handler_class)
    # httpd.serve_forever()


# run()
