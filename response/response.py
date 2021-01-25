import urllib, json, re
from jinja2 import Template
import requests

class Response():
    def __init__(self, senderId, responseType): 
        self.senderId = senderId
        self.data = {}
        self.type = responseType

    def loadData(self, result):
        self.data['results'] = result['result']
        self.data['engine'] = result['engine']
        return True

    def loadTemplate(self):
        template = Template(open('response/templates/' + self.type + '.jinja', 'r').read())
        
        rendered = template.render(data=self.data, senderId=self.senderId)

        return json.loads(rendered)

    def sendResponse(self):
        data = self.loadTemplate()

        headers = {
            'Content-Type': 'application/json',
        }

        requests.post('https://graph.facebook.com/104215895009543/messages?access_token=123', headers=headers, json=data)

        return 'ok'
