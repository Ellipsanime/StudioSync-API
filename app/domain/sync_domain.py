from typing import Any

from app.repo import sync_repo


async def synchronize_events() -> Any:
    i = await sync_repo.fetch_last_event_id()
    print(i)
