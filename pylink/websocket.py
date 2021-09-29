"""
MIT License

Copyright (c) 2021-present Aspect1103

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import aiohttp
from typing import Dict


class Websocket:
    def __init__(self, host: str, port: int, password: str, userID: str):
        self.host = host
        self.port = port
        self.password = password
        self.userID = userID
        self._session = aiohttp.ClientSession()
        self._connection = None
        asyncio.create_task(self.connect())

    async def connect(self):
        headers = {
            "Authorization": self.password,
            "User-Id": self.userID,
            "Client-Name": "Pylink"
        }
        self._connection = await self._session.ws_connect(f"ws://{self.host}:{self.port}", headers=headers, heartbeat=60)

    async def get(self, destination: str, headers: Dict[str, str]):
        return await self._session.get(destination, headers=headers)

    async def send(self, payload):
        await self._connection.send_json(payload)
