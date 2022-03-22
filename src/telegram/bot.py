import telegram
import logging
from telegram.error import RetryAfter

import time

logger = logging.getLogger(__name__)


class Bot(telegram.bot.Bot):

    def send_message(self, chat_id, text):

        try:
            return super().send_message(chat_id, text)
        except RetryAfter:
            logger.info('請求超時等待60s後重試')
            time.sleep(60)
            return self.send_message(chat_id, text)
        except Exception as e:
            logger.error(str(e))
            return ''

    def forward_message(self, chat_id, from_chat_id, message_id):

        try:
            super(Bot, self).forward_message(chat_id, from_chat_id, message_id)
        except RetryAfter as e:
            logger.info('請求超時等待60s後重試')
            time.sleep(60)
            return self.send_message(chat_id, from_chat_id, message_id)
        except Exception as e:
            logger.error(str(e))
            return ''
