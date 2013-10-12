import io

import requests


class WebAdapter:
    def __init__(self):
        self.cookies = {}

    def get(self, urllike):
        res = requests.get(str(urllike), cookies=self.cookies)
        self.cookies = res.cookies
        return res

    def get_text(self, urllike):
        res = self.get(urllike)
        return res.text

    def open(self, urllike):
        res = self.get(urllike)
        return io.BytesIO(res.content)
