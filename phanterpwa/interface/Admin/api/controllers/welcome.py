from tornado import (
    web
)
from core import (
    projectConfig
)

class Welcome(web.RequestHandler):
    def get(self, *args):
        self.write({
            "status": "OK",
            "message": "Hello World!",
            "project": projectConfig["PROJECT"]
        })
