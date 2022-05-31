from typing import Any

from app.repo import sync_repo, client_repo


async def synchronize_events() -> Any:
    return
    # await client_repo.fetch_version_changes_per_project(1)
