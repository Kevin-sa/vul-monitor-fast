import logging
import json

import telebot


class SendTelebot:
    def __init__(self):
        self.token = "5062609907:AAHaQ6QE3omoQiz15YdBjKKj13TUWG9fzaQ"
        self.chat_id = 773295023

    def send_message(self, text, parse_mode):
        logging.info("send message")
        tb = telebot.TeleBot(self.token)
        tb.send_message(self.chat_id, text=json.dumps(text))
