from typing import Any

from returns.pipeline import flow

from app.repo import sync_repo, client_repo


async def synchronize_origin() -> Any:
    raw_splits = await client_repo.fetch_projects()
    flow(
        raw_splits
    )

    return
    # await client_repo.fetch_version_changes_per_origin(1)
