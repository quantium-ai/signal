import json
import os
import re
import signal
from typing import List

from aiosmtpd.controller import Controller
from cloudscraper import create_scraper


class Signal:
    IDENTIFIER_PATH = None

    def __init__(self, identifier: str, webhook_url: str):
        if not self.IDENTIFIER_PATH:
            raise NotImplementedError("IDENTIFIER_PATH must be set in subclass")

        self.identifier = identifier
        self.webhook_url = webhook_url

    @staticmethod
    def jpath(query: str, data: dict, default=None):
        for key in query.split("."):
            if isinstance(data, dict):
                data = data.get(key, default)
        return data

    def verify_identifier(self, data: dict):
        return self.jpath(self.IDENTIFIER_PATH, data) == self.identifier

    def send_signal(self, message: str, headers: dict = None):
        return create_scraper().post(self.webhook_url, data=message, headers=headers or {})

    @staticmethod
    def run(signals: List["Signal"], smtp_host: str = None, smtp_port: int = None):
        class smtp_handler:
            async def handle_DATA(self, _, __, envelope):
                try:
                    message = re.search(r"^\{.+}", envelope.content.decode("utf-8"), re.M).group()
                    for strategy in filter(lambda s: s.verify_identifier(json.loads(message)), signals):
                        strategy.send_signal(message)
                except (AttributeError, Exception):
                    return "500 Error"
                return "250 OK"

        host = str(os.getenv("QUANTIUM_SIGNAL_SMTP_HOST", smtp_host))
        port = int(os.getenv("QUANTIUM_SIGNAL_SMTP_PORT", smtp_port))
        controller = Controller(
            smtp_handler(),
            hostname=host,
            port=port,
        )
        controller.start()
        try:
            signal.sigwait([
                signal.SIGINT,
                signal.SIGKILL,
                signal.SIGQUIT,
                signal.SIGTERM,
            ])
        finally:
            controller.stop()
