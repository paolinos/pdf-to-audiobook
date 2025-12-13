import asyncio
import signal

from models import ProcessOptions
from pubsub import Publisher, Subscriber
from utils import Logger
from validators import parse_args
from workers import (
    MarkdownAudioCoquiTTSWorker,
    Mp3ConverterWorker,
    PdfMarkdownWorker,
    WorkerTopic,
)


async def run_workers(group: asyncio.TaskGroup, logger: Logger):
    logger.debug("Init workers")
    pdf_md_worker = PdfMarkdownWorker(logger)
    md_audio_worker = MarkdownAudioCoquiTTSWorker(logger)
    mp3_worker = Mp3ConverterWorker(logger)

    group.create_task(pdf_md_worker.run())
    group.create_task(md_audio_worker.run())
    group.create_task(mp3_worker.run())

    await asyncio.sleep(1)
    logger.debug("workers ready")


async def main_async():
    options = parse_args()
    logger = Logger(False if options.debug is None else True)

    pub = Publisher("main")
    sub = Subscriber("main")

    async with asyncio.TaskGroup() as group:
        await run_workers(group, logger)

        logger.debug("publishing WorkerTopic.PROCESS_PDF_TO_MARKDOWN")
        pub.publish(
            WorkerTopic.PROCESS_PDF_TO_MARKDOWN,
            ProcessOptions(
                input_path=options.input_path,
                audio_speed=options.audio_speed,
                tmp_folder=options.tmp_folder,
            ),
        )
        logger.debug("listening for PROCESS_COMPLETED")
        mp3_output = await sub.listening_once(WorkerTopic.PROCESS_COMPLETED, str)
        logger.info(
            f"Successfully conversion from pdf to audiobook (mp3 file) in path:{mp3_output}"
        )


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, loop.stop)

    try:
        loop.run_until_complete(main_async())
    except RuntimeError as err:
        print("RuntimeError received, shutting down...", err)
    except KeyboardInterrupt as err:
        print("KeyboardInterrupt received, shutting down...", err)
    finally:
        # Cancel all running tasks
        tasks = asyncio.all_tasks(loop)
        for t in tasks:
            t.cancel()
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        loop.close()


if __name__ == "__main__":
    main()
