import requests

from impl.paper.intigriti_bug_bytes import IntigritoBugBytes
from impl.paper.list_of_bug_bounty_writeups import BugBountyWriteups
from impl.vulnerability.github_commit_monitor import GithubCommitMonitor
from impl.vulnerability.github_issue_monitor import GithubIssueMonitor
import logging

from impl.vulnerability.github_security_monitor import GithubSecurityMonitor
from impl.vulnerability.jira_apache_monitor import JiraApacheMonitor
from impl.vulnerability.oracle_monitor import OracleMonitor
from impl.vulnerability.sonatype_security_monitor import SonatypeMonitor
from impl.vulnerability.vmware_security_monitor import VMwareSecurityMonitor


def main():
    """
    检查网络连接
    执行实现类
    :return:
    """
    logging.info("Threat intelligence start")
    if check_target_network is False:
        return
    monitor_temp = [GithubCommitMonitor, GithubIssueMonitor, GithubSecurityMonitor, JiraApacheMonitor,
                    OracleMonitor, VMwareSecurityMonitor, SonatypeMonitor, IntigritoBugBytes, BugBountyWriteups]
    for temp in monitor_temp:
        try:
            temp().execute()
        except Exception as e:
            logging.error(f"{temp.__name__} execute error: {e}")
    logging.info("Threat intelligence end")


def check_target_network():
    try:
        target_uri = ['https://api.github.com']
        for temp in target_uri:
            requests.get(temp, timeout=3)
        return True
    except Exception as e:
        logging.error("error {}".format(e))
        return False


if __name__ == "__main__":
    log_path = __file__[:-7] + 'log/main.log'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s',
                        datefmt='%y-%m-%d %H:%M',
                        filename=log_path
                        )
    main()
