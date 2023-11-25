import asyncio
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

import cv2


class AsyncLastFrameBuffer:
    def __init__(self, url):
        self.__cap = cv2.VideoCapture(url)

        if not self.__cap.isOpened():
            raise cv2.error(f'Unable to access the camera at the specified address {url}')

        self.__frame_single_queue = asyncio.Queue()
        self.__stop_event = asyncio.Event()
        self.__read_task = self.__start()

    async def __read(self):
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        while not self.__stop_event.is_set():
            ret, frame = await loop.run_in_executor(
                executor,
                self.__cap.read
            )
            if not self.__frame_single_queue.empty():
                try:
                    self.__frame_single_queue.get_nowait()
                except queue.Empty:
                    pass
            await self.__frame_single_queue.put((ret, frame))
            await asyncio.sleep(0)  # Yield control to the event loop

        executor.shutdown()

    def __start(self):
        self.__stop_event.clear()
        return asyncio.create_task(self.__read())

    async def __stop(self):
        self.__stop_event.set()
        self.__read_task.cancel()
        self.__frame_single_queue.put_nowait((False, None))  # Signal the queue to release any waiting consumers

    async def read(self):
        return self.__frame_single_queue.get()

    def release(self):
        self.__stop()
        self.__cap.release()


class LastFrameBuffer:
    def __init__(self, url):
        self.__cap = cv2.VideoCapture(url)

        if not self.__cap.isOpened():
            raise cv2.error(f'Unable to access the camera at the specified address {url}')

        self.__frame_single_queue = queue.Queue()
        self.__stop_event = threading.Event()
        self.__daemon = threading.Thread(target=self.__read)
        self.__daemon.daemon = True

    def __read(self):
        while self.__cap.isOpened() and not self.__stop_event.is_set():
            ret, frame = self.__cap.read()
            if not self.__frame_single_queue.empty():
                try:
                    self.__frame_single_queue.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.__frame_single_queue.put((ret, frame))

    def start(self):
        self.__stop_event.clear()
        self.__daemon.start()

    def __stop(self):
        self.__stop_event.set()
        self.__frame_single_queue.put((False, None))

    def read(self):
        return self.__frame_single_queue.get()

    def release(self):
        self.__stop()
        self.__daemon.join()
        self.__cap.release()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
