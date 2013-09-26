
import requests


class WebAdapter:
    def __init__(self):
        self.cookies = {}

    def get(self, urllike):
        res = requests.get(str(urllike), cookies=self.cookies)
        self.cookies = res.cookies
        return res.text
