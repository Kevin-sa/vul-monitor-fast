import json
import logging
import re

from impl.monitor import Monitor


class JiraApacheMonitor(Monitor):
    """
    监控jira相关安全性issue
    """

    def __init__(self):
        super().__init__()
        self.url = "https://issues.apache.org/jira/secure/AjaxIssueAction!default.jspa?issueKey={issueKey}"
        self.rule = "jira_issue"
        self.temp_file_path = "temp/jira_monitor.json"

    def do_business(self):

        logging.info("do_business start")

        with open(self.project_file + self.temp_file_path) as file:
            primary_conf = json.load(file)
            file.close()
        warn_result = {'rule': self.rule}
        for temp in primary_conf.keys():
            for i in range(1, 1000):
                value = primary_conf.get(temp)
                issue_key = "{}-{}".format(temp, value.get("id") + i)
                resp = self.request.request(self.url.format(issueKey=issue_key), headers=self.headers)
                if resp.status_code != 200:
                    primary_conf[temp]['id'] += i - 1
                    logging.error("resp.status_code error:{}".format(resp.status_code))
                    break
                result = resp.json()
                summary = result.get('issue', {}).get('summary', '')
                pattern = self.black_pattern.get('common') if self.black_pattern.get(
                    value.get('language')) is None else self.black_pattern.get(value.get('language'))
                if re.search(pattern, summary, re.IGNORECASE):
                    result['issue_key'] = issue_key
                    result['project'] = value.get("project")
                    warn_result[issue_key] = self.get_warn_param(result)
        with open(self.project_file + self.temp_file_path, "w") as file:
            json.dump(primary_conf, file)
            file.close()

        return warn_result

    def get_warn_param(self, temp):
        return {'summary': temp.get('issue', {}).get('summary', ''),
                'url':
                    'https://issues.apache.org/jira/projects/{project}/issues/{issue_key}?filter=allopenissues&orderby=created+DESC%2C+priority+DESC%2C+updated+DESC'.format(
                        project=temp.get('project', ''), issue_key=temp.get('issue_key', ''))}


if __name__ == "__main__":
    JiraApacheMonitor().execute()