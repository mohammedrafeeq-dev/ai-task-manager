import logging
import os
from logging.handlers import RotatingFileHandler
from queue import Queue
from threading import Thread


class AsyncQueueHandler(logging.Handler):
    def __init__(self, handler: logging.Handler):
        super().__init__()
        self.queue = Queue()
        self.handler = handler
        thread = Thread(target=self._process, daemon=True)
        thread.start()

    def emit(self, record):
        self.queue.put_nowait(record)

    def _process(self):
        while True:
            record = self.queue.get()
            self.handler.emit(record)


def setup_logging(app):
    log_dir = os.path.join(app.root_path, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"), maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
    )
    async_handler = AsyncQueueHandler(file_handler)
    async_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    app.logger.addHandler(async_handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
