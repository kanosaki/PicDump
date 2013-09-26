
import urllib.request


class WebAdapter:
    def get(self, urllike):
        url = self.mk_url(urllike)
        try:
            res = urllib.request.urlopen(url)
            return res.read()
        except Exception as e:
            raise e

    def open(self, urllike):
        url = self.mk_url(urllike)
        try:
            return urllib.request.urlopen(url)
        except Exception as e:
            raise e

    def mk_url(self, urllike):
        return str(urllike)
