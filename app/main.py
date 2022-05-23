import os

import uvicorn

from app.setup import setup_all

app = setup_all(None)


def start():
    port = int(os.getenv("APP_PORT", 8090))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()
