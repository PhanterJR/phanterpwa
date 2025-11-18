"""
Title: XmlConstructor

Author: PhanterJR<junior.conex@gmail.com>

License: MIT

Coding: utf-8

Send emails
"""
import requests
import json


class SMSSender(object):
    """
    
    """

    def __init__(self, fone_number, identify, text_message, app_name, projectConfig):
        super(SMSSender, self).__init__()
        self.fone_number = fone_number
        self.identify = identify
        self.text_message = text_message
        self.app_name = app_name
        self.projectConfig = projectConfig

    def send(self):
        """
            Mobizon Example
        """
        HEADERS = {
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {
            'recipient': self.fone_number,
            'text': self.text_message
        }
        key = self.projectConfig["BACKEND"][self.app_name].get("mobizen_key", None)
        url = "https://api.mobizon.com.br/service/message/sendSmsMessage?output=json&api=v1&apiKey={0}".format(key)
        response_cl1 = requests.post(url, headers=HEADERS, data=data, timeout=30)
        json_response_cl1 = json.loads(response_cl1.content)
        return json_response_cl1
