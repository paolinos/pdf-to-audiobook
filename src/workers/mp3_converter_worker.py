from ffmpeg.join import merge_and_convert_mp3
from ffmpeg.speed import change_speed
from helpers.file import delete_file
from models import Mp3ConverterPayload
from utils.logging import Logger
from workers.base import BaseWorker, WorkerTopic


class Mp3ConverterWorker(BaseWorker):
    def __init__(self, logger: Logger):
        super().__init__(logger)

    async def run(self):
        self._logger.debug("listening for PROCESS_MP3_CONVERTER")

        payload = await self._sub.listening_once(
            WorkerTopic.PROCESS_MP3_CONVERTER, Mp3ConverterPayload
        )
        self._logger.debug("listening for PROCESS_MP3_CONVERTER payload", payload)

        # TODO: speed??
        output_path = merge_and_convert_mp3(payload.audio_files, payload.input_path)

        # TODO: we should move this
        for audio_file in payload.audio_files:
            delete_file(audio_file)

        if payload.audio_speed != 1.0:
            change_speed(output_path, payload.audio_speed)

        self._pub.publish(WorkerTopic.PROCESS_COMPLETED, output_path)

    def stop(self):
        pass
