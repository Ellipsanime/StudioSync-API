from typing import Any

import app.util.db
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

_KEY = "event.last_id"
# CREATE TABLE IF NOT EXISTS object_store (key TEXT PRIMARY KEY, value BLOB);
# INSERT OR REPLACE INTO object_store VALUES ('event.last_id', 0);
_SCRIPT = """
------------------------------------
-------------- PROVIDER ------------
------------------------------------
CREATE TABLE IF NOT EXISTS provider_project (
    id INTEGER PRIMARY KEY NOT NULL, 
    title TEXT NOT NULL,
    code TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS provider_file (
    id INTEGER PRIMARY KEY NOT NULL, 
    code TEXT NOT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    element TEXT NOT NULL,
    extension TEXT NOT NULL,
    path TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project (id)
);
CREATE TABLE IF NOT EXISTS provider_version_change (
    id INTEGER PRIMARY KEY NOT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    entity_type TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    task TEXT NOT NULL,
    status TEXT NOT NULL,
    revision INTEGER NOT NULL,
    comment TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project (id)
);
CREATE TABLE IF NOT EXISTS provider_linked_files (
    file_id INTEGER NOT NULL,
    version_change_id INTEGER NOT NULL,
    PRIMARY KEY (file_id, version_change_id),
    FOREIGN KEY (file_id) REFERENCES file (id),
    FOREIGN KEY (version_change_id) REFERENCES version_change (id)
);
------------------------------------
--------------  CLIENT  ------------
------------------------------------
CREATE TABLE IF NOT EXISTS client_project (
    id INTEGER PRIMARY KEY NOT NULL, 
    title TEXT NOT NULL,
    code TEXT NOT NULL,
    source TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS client_file (
    id INTEGER PRIMARY KEY NOT NULL, 
    code TEXT NOT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    element TEXT NOT NULL,
    extension TEXT NOT NULL,
    path TEXT NOT NULL,
    source TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project (id)
);
CREATE TABLE IF NOT EXISTS client_version_change (
    id INTEGER PRIMARY KEY NOT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    entity_type TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    task TEXT NOT NULL,
    status TEXT NOT NULL,
    revision INTEGER NOT NULL,
    comment TEXT NOT NULL,
    processed INTEGER NOT NULL,
    source TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project (id)
);
CREATE TABLE IF NOT EXISTS client_linked_files (
    file_id INTEGER NOT NULL,
    version_change_id INTEGER NOT NULL,
    PRIMARY KEY (file_id, version_change_id),
    FOREIGN KEY (file_id) REFERENCES file (id),
    FOREIGN KEY (version_change_id) REFERENCES version_change (id)
);
"""


async def db_exists() -> bool:
    try:
        async with app.util.db.connect_file_db("rw") as _:
            return True
    except Exception:
        return False


async def setup_db() -> Any:
    async with app.util.db.connect_file_db() as db:
        await db.executescript(_SCRIPT)
        await db.commit()

