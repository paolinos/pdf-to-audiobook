
from pubsub.base import _BasePubSub


class Publisher:

    def __init__(self, group:str):
        self._group = group

    def publish(self, topic:str, data:dict):
        _BasePubSub()._publish(topic, data)