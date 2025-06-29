import random
from http import HTTPStatus

import dashscope

from utils.logger import logger


class LLMutils(object):

    def __init__(self):
        # api key
        dashscope.api_key = ""
        self.logger = logger

    """
    调用通义千问
    """

    def dashscope_call_msg(self, content: str, prompt: str):
        try:
            messages = [{'role': 'system',
                         'content': prompt},
                        {'role': 'user', 'content': content}]
            response = dashscope.Generation.call(
                dashscope.Generation.Models.qwen_turbo,
                messages=messages,
                seed=random.randint(1, 10000),
                result_format='message',
            )
            if response.status_code == HTTPStatus.OK:
                self.logger.info(f"dashscope_call_msg: response:{response}")
                return response
            else:
                self.logger.info('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))
                return None
        except Exception as e:
            self.logger.error(f"dashscope_call_msg error:{e}")
            return None


if __name__ == "__main__":
    print(LLMutils().dashscope_call_msg(content="你是谁？", prompt="A"))