import asyncio
import tornado
from tornado.options import define, options
from currency_observer import CurrencyObserver, CurrencyWebSocketHandler

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

async def main():
    tornado.options.parse_command_line()
    observer = CurrencyObserver()

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/ws", CurrencyWebSocketHandler, {"observer": observer}),
        ],
        template_path="templates",
        static_path="static",
    )

    app.listen(options.port)
    asyncio.create_task(observer.fetch_currencies(['USD', 'EUR', 'GBP']))
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())