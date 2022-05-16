from typing import Any

from app.util import connectivity
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

_KEY = "event.last_id"

_SCRIPT = """
CREATE TABLE IF NOT EXISTS object_store (key TEXT PRIMARY KEY, value BLOB);
CREATE TABLE IF NOT EXISTS project (
    id INTEGER PRIMARY KEY NOT NULL, 
    title TEXT NOT NULL,
    code TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS file (
    id INTEGER PRIMARY KEY NOT NULL, 
    code TEXT NOT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    revision INTEGER NOT NULL,
    file_path TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS task_change (
    id INTEGER PRIMARY KEY NOT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    entity_type TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    task TEXT NOT NULL,
    status TEXT NOT NULL,
    comment TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS linked_files (
    file_id INTEGER NOT NULL,
    task_change_id INTEGER NOT NULL,
    PRIMARY KEY (file_id, task_change_id)
);
INSERT OR REPLACE INTO object_store VALUES ('event.last_id', 0);
"""


async def db_exists() -> bool:
    try:
        async with connectivity.connect_file_db("rw") as _:
            return True
    except Exception:
        return False


async def setup_db() -> Any:
    async with connectivity.connect_file_db() as db:
        await db.executescript(_SCRIPT)
        await db.commit()

