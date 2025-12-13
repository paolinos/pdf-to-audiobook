from abc import ABC, abstractmethod
from enum import Enum

from pubsub.publisher import Publisher
from pubsub.subscriber import Subscriber
from utils.logging import Logger


class BaseWorker(ABC):
    _logger: Logger
    _sub: Subscriber
    _pub: Publisher

    def __init__(self, logger: Logger):
        self._logger = logger
        self._sub = Subscriber(self.__class__.__name__)
        self._pub = Publisher(self.__class__.__name__)
        self._logger.info(f"Init {self.__class__.__name__} worker")

    @abstractmethod
    async def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class WorkerTopic(str, Enum):
    PROCESS_PDF_TO_MARKDOWN = "process-pdf-to-markdown"
    PROCESS_MARKDOWN_AUDIO = "process-markdown-to-audio"
    PROCESS_MP3_CONVERTER = "process-mp3-converter"
    PROCESS_COMPLETED = "process-completed"
