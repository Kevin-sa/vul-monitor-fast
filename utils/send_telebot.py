import logging
import json

import telebot


class SendTelebot:
    def __init__(self):
        self.token = ""
        self.chat_id = 0

    def send_message(self, text, parse_mode):
        logging.info("send message")
        tb = telebot.TeleBot(self.token)
        tb.send_message(self.chat_id, text=json.dumps(text), parse_mode=parse_mode)
