import logging
from abc import ABCMeta, abstractmethod

from utils.requests_utils import Request
from utils.send_telebot import SendTelebot
from os.path import dirname


class Monitor(metaclass=ABCMeta):

    def __init__(self):
        self.github_repos = [{'user': 'apache', 'repo': 'kafka', 'language': 'java'},
                             {'user': 'FasterXML', 'repo': 'jackson-core', 'language': 'java'},
                             {'user': 'FasterXML', 'repo': 'jackson-databind', 'language': 'java'},
                             {'user': 'FasterXML', 'repo': 'jackson-bom', 'language': 'java'},
                             {'user': 'mybatis', 'repo': 'mybatis-3', 'language': 'java'},
                             {'user': 'spring-projects', 'repo': 'spring-boot', 'language': 'java'},
                             {'user': 'spring-projects', 'repo': 'spring-framework', 'language' : 'java'},
                             {'user': 'spring-cloud', 'repo': 'spring-cloud-function', 'language': 'java'},
                             {'user': 'qos-ch', 'repo': 'logback', 'language': 'java'},
                             {'user': 'qos-ch', 'repo': 'slf4j', 'language': 'java'},
                             {'user': 'google', 'repo': 'guava', 'language': 'java'},
                             {'user': 'apache', 'repo': 'commons-io', 'language': 'java'},
                             {'user': 'apache', 'repo': 'tomcat', 'language': 'java'},
                             {'user': 'apache', 'repo': 'commons-logging', 'language': 'java'},
                             {'user': 'apache', 'repo': 'commons-compress', 'language': 'java'},
                             {'user': 'google', 'repo': 'gson', 'language': 'java'},
                             {'user': 'apache', 'repo': 'commons-lang', 'language': 'java'},
                             {'user': 'apache', 'repo': 'commons-collections', 'language': 'java'},
                             {'user': 'googleapis', 'repo': 'google-oauth-java-client', 'language': 'java'},
                             {'user': 'apache', 'repo': 'commons-beanutils', 'language': 'java'},
                             {'user': 'apache', 'repo': 'beam', 'language': 'java'},
                             {'user': 'h2database', 'repo': 'h2database', 'language': 'java'},
                             {'user': 'protocolbuffers', 'repo': 'protobuf', 'language': 'java'},
                             {'user': 'sonatype', 'repo': 'nexus-public', 'language': 'java'}
                             ]
        self.github_authorization = ""
        self.black_pattern = {
            'common': '(security| cve- |vulnerabilities|security)',
            'java': '(security|cve-| jndi | ldap |injection| xxe |sqli| rce | ssrf |vulnerabilities| spel )'
        }
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
        self.project_file = dirname(__file__)[:-4]
        self.request = Request()

    @abstractmethod
    def do_business(self):
        return

    @staticmethod
    def after_business(warn_result):
        if warn_result is None or len(warn_result) == 1 or warn_result == {}:
            return
        logging.info("get warn_result:{}".format(warn_result))
        send = SendTelebot()
        send.send_message(warn_result, None)

    @abstractmethod
    def get_warn_param(self, temp):
        return

    def execute(self):
        warn_info = self.do_business()
        self.after_business(warn_info)
