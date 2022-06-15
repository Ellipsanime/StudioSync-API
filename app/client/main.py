import os
from typing import Any

import uvicorn

from app.client.setup import setup_all

app = setup_all(None)


def start() -> Any:
    port = int(os.getenv("APP_PORT", 8091))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()
