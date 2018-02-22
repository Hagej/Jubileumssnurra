#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
import asyncio as aio
import websockets
import serial
import json
import serial_asyncio

import sys
import functools
from concurrent.futures import ThreadPoolExecutor


# DEVICE = '/dev/cu.usbmodem1421' # Maskinen
DEVICE = '/dev/cu.usbserial-A6004b7d' # Hemma

ser = serial.Serial(DEVICE, timeout=1)  # open serial port with 1s timeout
print(ser.name)         # check which port was really used

# Test function when not using aruino
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

async def serInput():
    global connected
    while True:
        await aio.sleep(0)
        x = ser.readline()          # read one line
        msg = json.dumps({'action': x.decode('ascii')})
        if (x != b''):
            return msg
            # print(x)
            # for ws in connected:
                # ws.send(msg)

executor = ThreadPoolExecutor(2)

# Async Serial
# class Output(aio.Protocol):
    # def connection_made(self, transport):
        # self.transport = transport
        # print('port opened', transport)
        # # transport.serial.rts = False  # You can manipulate Serial object via transport
        # # transport.write(b'Hello, World!\n')  # Write serial data via transport

    # def data_received(self, data):
        # print('data received', repr(data))
        # if b'\r\n' in data:
            # return data
            # # self.transport.close()

    # def connection_lost(self, exc):
        # print('port closed')
        # self.transport.loop.stop()


# # WebSockets server

connected = set()

async def wshandler(websocket, path):
    global connected
    connected.add(websocket)
    print(connected)

    while True:
        msg = await serInput()
        print(msg)
        # msg = json.dumps({'action': 'Forward\r\n'})
        for client in connected:
            try:
                await client.send(msg)
            except websockets.exceptions.ConnectionClosed:
                pass

    # while True:
        # await prompt("press enter")
        # msg = json.dumps({'action': 'Forward\r\n'})
        # for client in connected:
            # try:
                # await client.send(msg)
            # except websockets.exceptions.ConnectionClosed:
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
        msg = await serInput()
        print(msg)
        # msg = json.dumps({'action': 'Forward\r\n'})
        for client in connected:
            try:
                await client.send(msg)
            except websockets.exceptions.ConnectionClosed:
                pass

start_server = websockets.serve(wshandler, 'localhost', 8765)

loop = aio.get_event_loop()

# ser = (loop.run_in_executor(executor, serInput))

# coro = serial_asyncio.create_serial_connection(loop, Output, DEVICE,
        # baudrate=9600)

# loop.run_until_complete(coro)
# loop.run_forever()

# aio.ensure_future(start_server)
# loop.run_until_complete(serInput())
# loop.run_until_complete(main())

aio.get_event_loop().run_until_complete(start_server)
aio.get_event_loop().run_forever()

