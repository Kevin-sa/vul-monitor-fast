import json
import logging

import telebot


class SendTelebot:
    def __init__(self):
        self.token = ""
        self.chat_id = 0

    def send_message(self, text: dict, parse_mode: str):
        logging.info("send message")
        if text.get("rule") in ["sonatype_monitor", "VMware_security_monitor", "list_of_bug_bounty_writeups"]:
            msg = self.covert_msg(text)
        else:
            msg = json.dumps(text)
        tb = telebot.TeleBot(self.token, parse_mode="MARKDOWN")
        return tb.send_message(self.chat_id, text=msg)

    def covert_msg(self, text: dict) -> str:
        msg = f"**规则**```{text.get('rule', 'rule')}``` \n"
        for i in text.get("data", []):
            msg += f"- [{i.get('text', 'text')}]({i.get('href', 'href')}) \n"
        return msg


if __name__ == "__main__":
    msg = '{"data": [{"text": "Vulnerabilities in Online Payment Systems", "href": "https://medium.com/@claudio_moranb/vulnerabilities-in-online-payment-systems-edd2d3c06905"}, {"text": "CVE-2022\u201336635 \u2014 A SQL Injection in ZKSecurityBio to RCE", "href": "https://medium.com/stolabs/cve-2022-36635-a-sql-injection-in-zksecuritybio-to-rce-c5bde2962d47"}, {"text": "Caio Burgardt (@CaioBurgardt)", "href": "https://twitter.com/CaioBurgardt"}, {"text": "Full Company Building Takeover", "href": "https://omar0x01.medium.com/company-building-takeover-10a422385390"}, {"text": "Technical Advisory \u2013 OpenJDK \u2013 Weak Parsing Logic in java.net.InetAddress and Related Classes", "href": "https://research.nccgroup.com/2022/10/06/technical-advisory-openjdk-weak-parsing-logic-in-java-net-inetaddress-and-related-classes/"}, {"text": "Jeff Dileo (@ChaosDatumz)", "href": "https://twitter.com/ChaosDatumz"}, {"text": "SSD Advisory \u2013 pfSense Post Auth RCE", "href": "https://ssd-disclosure.com/ssd-advisory-pfsense-post-auth-rce/"}, {"text": "\uc774\uc608\ub791 (@yelang123x)", "href": "https://twitter.com/yelang123x"}, {"text": "Mr. Robot: Self Xss from Informative to high 1200$ ,csrf, open redirect,self xss to stored", "href": "https://ahmadaabdulla.medium.com/mr-robot-self-xss-from-informative-to-high-1200-csrf-open-redirect-self-xss-to-stored-92f371ba3da1"}, {"text": "Exploit Disclosure: Turning Thunderbird into a Decryption Oracle", "href": "https://pseudorandom.resistant.tech/disclosing-security-and-privacy-issues-in-thunderbird.html"}, {"text": "Sarah Jamie Lewis (@SarahJamieLewis)", "href": "https://twitter.com/SarahJamieLewis"}, {"text": "Trenches of IT (@TrenchesofIT)", "href": "https://twitter.com/TrenchesofIT"}, {"text": "Exploiting URL Parsers: The Good, Bad, And Inconsistent", "href": "https://claroty.com/wp-content/uploads/2022/01/Exploiting-URL-Parsing-Confusion.pdf"}, {"text": "Raul Onitza-Klugman (@supriza0)", "href": "https://twitter.com/supriza0"}, {"text": "Kirill Efimov (@byte89)", "href": "https://twitter.com/byte89"}], "rule": "list_of_bug_bounty_writeups"}'
    print(SendTelebot().send_message(json.loads(msg), ""))

