import requests
import json
import logging
info_logger = logging.getLogger("通知")


class Info(object):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=700af0fa23467b530f7fa75edad09ff42812d1e597e167f289c9e2897fb4b123'
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    payload = {
        "msgtype": "text",
        "text": {
            "content": "..."
        },
        "at": {
            "atMobiles": [
                ""
            ],
            "isAtAll": False
        }
    }

    @classmethod
    def send_info(self, msg="爬虫程序需要手动干预"):
        self.payload['text']['content'] = msg
        r = requests.post(self.url, data=json.dumps(
            self.payload), headers=self.headers)
        info_logger.info(r.text)

