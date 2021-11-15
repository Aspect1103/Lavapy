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

from typing import TYPE_CHECKING, Optional, Union, List, Dict, Type, Any

if TYPE_CHECKING:
    from .node import Node


__all__ = ("Playable",
           "PartialResource",
           "Track",
           "MultiTrack",
           "YoutubeTrack",
           "YoutubeMusicTrack",
           "SoundcloudTrack",
           "YoutubePlaylist")


class Playable:
    """
    The base class for all Lavapy resources. This supports both query searches and identifier searches.

    .. warning::
        This class should not be created manually. Instead use a subclass of :class:`Track` or :class:`MultiTrack`.
    """
    _searchType: str
    _trackCls: Optional[Type[Track]]

    @classmethod
    async def search(cls, query: str, node: Node = None, search: bool = True, returnFirst: bool = True, partial: bool = False) -> Optional[Union[Track, List[Track], PartialResource, MultiTrack]]:
        """|coro|

        Performs a search to Lavalink for a specific resource.

        Parameters
        ----------
        query: str
            The query to search for.
        node: Node
            The Lavapy Node to use for searching. If this is not supplied, a random one from the node pool will be retrieved.
        search: bool
            Whether to use a query search or an identifier search.
        returnFirst: bool
            Whether to return only the first result or not.
        partial: bool
            Whether to return a Lavapy partial resource or not.

        Returns
        -------
        Optional[Union[Track, List[Track], PartialResource, MultiTrack]]
            A Lavapy resource or a list of resources which can be used to play music.
        """
        if node is None:
            # Avoid a circular dependency with node.buildTrack()
            from .pool import NodePool
            node = NodePool.getNode()
        if search:
            query = f"{cls._searchType}:{query}"
        if partial:
            return PartialResource(cls, query, search)
        tracks = await node.getTracks(cls, query)
        if tracks is not None:
            if search and returnFirst:
                return tracks[0]
            return tracks

    def __init__(self, *data: Any) -> None:
        """This is just here to stop :meth:`Node.getTracks()` being upset about unexpected arguments."""


class PartialResource:
    """
    A class which searches for the given query at playtime.

    .. warning::
        It is advised not to create this manually, however, it is possible to do so.

    Parameters
    ----------
    cls: Type[Playable]
        The resource to create a instance of at playtime.
    query: str
        The query to search for at playtime.
    search: bool
        Whether the query is a query search or an identifier search.

    .. warning::
        This object will only search for the given query at playtime. Full resource information will be missing until it has been searched. It is advised not to create this manually, however, it is possible to do so.
    """
    def __init__(self, cls: Type[Playable], query: str, search: bool) -> None:
        self._cls = cls
        self._query: str = query
        self._search: bool = search

    def __repr__(self) -> str:
        return f"<Lavapy PartialResource (Cls={self.cls}) (Query={self.query})>"

    @property
    def cls(self) -> Type[Playable]:
        """Returns the resource which will be created at playtime."""
        return self._cls

    @property
    def query(self) -> str:
        """Returns the query which will be searched for at playtime."""
        return self._query

    @property
    def search(self) -> bool:
        """Returns whether the query is a query search or an identifier search."""
        return self._search


class Track:
    """
    The base class for all Lavapy Track objects.

    .. warning::
        It is advised not to create this manually, however, it is possible to do so.

    Parameters
    ----------
    id: str
        The unique base64 track ID which can be used to rebuild a track.
    info: Dict[str, Any]
        The raw track info.
    """
    def __init__(self, id: str, info: Dict[str, Any]) -> None:
        self._id: str = id
        self._info: Dict[str, Any] = info
        self._identifier: str = info["identifier"]
        self._isSeekable: bool = info["isSeekable"]
        self._author: str = info["author"]
        self._length: int = info["length"]
        self._isStream: bool = info["isStream"]
        self._type: str = info["sourceName"]
        self._title: str = info["title"]
        self._uri: str = info["uri"]

    def __repr__(self) -> str:
        return f"<Lavapy Track (Identifier={self.identifier}) (Type={self.type})>"

    @property
    def id(self) -> str:
        """Returns the base64 track ID."""
        return self._id

    @property
    def identifier(self) -> str:
        """Returns the track's unique identifier."""
        return self._identifier

    @property
    def isSeekable(self) -> bool:
        """Returns whether a track is seekable or not."""
        return self._isSeekable

    @property
    def author(self) -> str:
        """Returns the author of the track."""
        return self._author

    @property
    def length(self) -> int:
        """Returns the duration of the track in seconds."""
        return self._length

    @property
    def isStream(self) -> bool:
        """Returns whether the track is a stream or not."""
        return self._isStream

    @property
    def type(self) -> str:
        """Returns the source site of the track."""
        return self._type

    @property
    def title(self) -> str:
        """Returns the title of the track."""
        return self._title

    @property
    def uri(self) -> str:
        """Returns the URI of the track."""
        return self._uri


class MultiTrack:
    """
    The base class for all Lavapy MultiTrack resources. These could be playlists or albums.

    .. warning::
        It is advised not to create this manually, however, it is possible to do so.

    Parameters
    ----------
    name: str
        The name of the playlist.
    tracks: List[Track]
        The playlist's tracks as a list of Lavapy Track objects.
    """
    def __init__(self, name: str, tracks: List[Track]) -> None:
        self._name: str = name
        self._tracks: List[Track] = tracks

    def __repr__(self) -> str:
        return f"<Lavapy MultiTrack (Name={self.name}) (Track count={len(self.tracks)})>"

    @property
    def name(self) -> str:
        """Returns the name of the playlist."""
        return self._name

    @property
    def tracks(self) -> List[Track]:
        """Returns the playlist's tracks."""
        return self._tracks


class YoutubeTrack(Track, Playable):
    """A track created using a search to Youtube."""
    _searchType: str = "ytsearch"

    def __repr__(self) -> str:
        return f"<Lavapy YoutubeTrack (Identifier={self.identifier})>"


class YoutubeMusicTrack(Track, Playable):
    """A track created using a search to Youtube Music."""
    _searchType: str = "ytmsearch"

    def __repr__(self) -> str:
        return f"<Lavapy YoutubeMusicTrack (Identifier={self.identifier})>"


class SoundcloudTrack(Track, Playable):
    """A track created using a search to Soundcloud."""
    _searchType: str = "scsearch"

    def __repr__(self) -> str:
        return f"<Lavapy SoundcloudTrack (Identifier={self.identifier})>"


class YoutubePlaylist(MultiTrack, Playable):
    """A playlist created using a search to Youtube."""
    _trackCls: Track = YoutubeTrack

    def __repr__(self) -> str:
        return f"<Lavapy YoutubePlaylist (Name={self.name}) (Track count={len(self.tracks)})>"
