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
from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node

__all__ = ("Stats",)


class Stats:
    """
    Stores useful information sent by Lavalink about this :class:`Node`.

    Attributes
    ----------
    node: Node
        The Lavapy Node these stats are about.
    uptime: int
        How long this node has been up for.
    players: int
        How many players are connected to this node.
    playingPlayers: int
        How many players that are connected to this node are playing tracks.
    memoryReservable: int
        How much memory is reserved by the system.
    memoryUsed: int
        How much memory is used by the system.
    memoryFree: int
        How much memory is free in the system.
    memoryAllocated: int
        How much memory is allocated to Lavalink.
    cpuCores: int
        How many cpu cores the system has.
    systemLoad: float
        The load on the system as a percentage.
    lavalinkLoad: float
        The load on the Lavalink server as a percentage.
    framesSent: int
        to do
    framesDeficit: int
        to do
    framesNulled: int
        to do
    """
    def __init__(self, node: Node, data: Dict[str, Any]) -> None:
        self.node: Node = node
        self.uptime: int = data["uptime"]
        self.players: int = data["players"]
        self.playingPlayers: int = data["playingPlayers"]

        memory: Dict[str, Any] = data["memory"]
        self.memoryReservable: int = memory["reservable"]
        self.memoryUsed: int = memory["used"]
        self.memoryFree: int = memory["free"]
        self.memoryAllocated: int = memory["allocated"]

        cpu: Dict[str, Any] = data["cpu"]
        self.cpuCores: int = cpu["cores"]
        self.systemLoad: float = cpu["systemLoad"]
        self.lavalinkLoad: float = cpu["lavalinkLoad"]

        frameStats: Dict[str, Any] = data.get("frameStats", {})
        self.framesSent: int = frameStats.get("sent", -1)
        self.framesDeficit: int = frameStats.get("deficit", -1)
        self.framesNulled: int = frameStats.get("nulled", -1)

    def __repr__(self) -> str:
        return f"<Lavapy Stats (Node={self.node})>"
