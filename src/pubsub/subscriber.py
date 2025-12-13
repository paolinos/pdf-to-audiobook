import asyncio
from typing import Callable, TypeVar
from pubsub.base import _BasePubSub, _GroupSubscriber

T = TypeVar("T")


class Subscriber:

    _group:str
    _subscriber:dict[str, _GroupSubscriber] = {}
    _run: bool = True

    def __init__(self, group:str):
        self._group = group


    def __subscribe(self, topic:str):
        if topic not in self._subscriber:
            self._subscriber[topic] = _BasePubSub()._add_subscriber(self._group, topic)


    async def listening_once(self, topic:str, c:Callable[[], T]) -> T:
        """
        Listening until receive a message
        if not message received, will not produce error and continue waiting
        """
        self.__subscribe(topic)

        while self._run:
            try:
                data = self._subscriber[topic].q.get(True, 5)
                return data
            except Exception:
                pass
            finally:
                await asyncio.sleep(1)