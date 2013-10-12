import io

import requests


class WebAdapter:
    def __init__(self):
        self.cookies = {}

    def get(self, urllike, referer=None):
        if referer is not None:
            res = requests.get(str(urllike),
                               cookies=self.cookies,
                               headers={'Referer': referer})
        else:
            res = requests.get(str(urllike), cookies=self.cookies)
        self.cookies = res.cookies
        return res

    def get_text(self, urllike, **kw):
        res = self.get(urllike, **kw)
        return res.text

    def open(self, urllike, **kw):
        res = self.get(urllike, **kw)
        return io.BytesIO(res.content)
