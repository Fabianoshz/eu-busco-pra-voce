# https://stackoverflow.com/a/62207356/5562289

import os
import sys
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
import uuid
import shutil


class Download():
    def __init__(self, url):
        self.url = url
        self.id = str(uuid.uuid4())
        self.outputDir = '/tmp/' + self.id + '/'

        self.session = requests.Session()
        self.soup = BeautifulSoup(self.session.get(url).text, features="lxml")

    def save(self):
        if not os.path.exists(self.outputDir):  # create only once
            os.mkdir(self.outputDir)

        soup = self.soupfindnSave('img', 'src')
        soup = self.soupfindnSave('script', 'src')

        with open(self.outputDir + 'page.html', 'wb') as file:
            file.write(soup.prettify('utf-8'))

        shutil.make_archive('/tmp/' + self.id + '.zip', 'zip', self.outputDir)
        shutil.rmtree(self.outputDir)

        return '/tmp/' + self.id + '.zip'

    def soupfindnSave(self, tag2find, inner='src'):
        for res in self.soup.findAll(tag2find):   # images, css, etc..
            try:
                # check if inner tag (file object) exists
                if not res.has_attr(inner):
                    continue  # may or may not exist

                # clean special chars
                filename = re.sub('\W+', '', os.path.basename(res[inner]))
                fileurl = urljoin(self.url, res.get(inner))
                filepath = os.path.join(self.outputDir, filename)

                # rename html ref so can move html and folder of files anywhere
                res[inner] = os.path.join(
                    os.path.basename(self.outputDir),
                    filename
                )

                if not os.path.isfile(filepath):  # was not downloaded
                    with open(filepath, 'wb') as file:
                        filebin = self.session.get(fileurl)
                        file.write(filebin.content)

            except Exception as exc:
                print(exc, file=sys.stderr)

        return self.soup