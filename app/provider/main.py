import os
from typing import Any

import uvicorn

from app.provider.setup import setup_all


def start() -> Any:
    app = setup_all(None)
    port = int(os.getenv("APP_PORT", 8092))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()
