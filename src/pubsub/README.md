# PubSub embedded

For sure there're alternatives like ZeroMQ but we don't need anything complex and also this it not to make more services, the main idea is to have workers that run all together in one app, without external communication.

So we're going to do a PubSub logic for events using
### How to use it
```py
import asyncio
import time
from pubsub.subscriber import Subscriber
from pubsub.publisher import Publisher

async def subscriber():
    sub = Subscriber("groupA")
    # only consume once
    data = await sub.listening_once("some-topic")
    print("received message", data)

async def publisher():
    pub = Publisher("groupB")
    pub.publish("some-topic", {"data":"one", "v": 1.345, "time": time.time()})
    # This message should not arrive.
    pub.publish("some-topic", {"data":"one", "v": 1.345})

async def main():
    futures = [
        subscriber(),
        publisher(),
    ]
    await asyncio.gather(*futures)

if __name__ == "__main__":
    asyncio.run(main())
```