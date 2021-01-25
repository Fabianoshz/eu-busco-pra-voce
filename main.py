import tornado.ioloop
import tornado.web
import tornado.log
import json
from response.response import Response
from search.search import Search
from intent.intent import Intent
from download.download import Download


class WebhookHandler(tornado.web.RequestHandler):
    def post(self):
        self.intent = Intent()
        self.failed = True

        body = json.loads(self.request.body)

        input = body['entry'][0]['messaging'][0]['message']['text'].split()
        senderId = body['entry'][0]['messaging'][0]['sender']['id']

        self.write('')  # Return 200 so the request don't get stuck.

        if self.intent.getIntent(input[0]) == 'search':
            self.failed = False

            search = Search()
            result = search.search(input[1])

            response = Response(senderId, 'search')
            response.loadData(result)

        if self.intent.getIntent(input[0]) == 'download':
            self.failed = False

            download = Download(input[1])
            result['file'] = download.save()

            response = Response(senderId, 'download')
            response.loadData(result)

        if self.intent.getIntent(input[0]) == 'summary':
            self.failed = False

        if self.failed:
            response = Response(senderId, 'failed')

        response.sendResponse()

    def get(self):
        # hubVerifyToken = self.get_argument('hub.verify_token')
        # hubMode = self.get_argument('hub.mode')
        hubChallenge = self.get_argument('hub.challenge')

        self.write(hubChallenge)


def make_app():
    return tornado.web.Application([
        (r"/webhook", WebhookHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
