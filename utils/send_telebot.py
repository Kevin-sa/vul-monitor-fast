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
        tb.config['api_key'] = self.token
        return tb.send_message(self.chat_id, text=json.dumps(text))


if __name__ == "__main__":
    print(SendTelebot().send_message({'text': 'test'}, None))
