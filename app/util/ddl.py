from typing import Any

import app.util.db as db_util
from app.util.logger import get_logger

_LOG = get_logger(__name__.split(".")[-1])

# _KEY = "event.last_id"
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
    FOREIGN KEY (project_id) REFERENCES provider_project (id)
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
    FOREIGN KEY (project_id) REFERENCES provider_project (id)
);
CREATE TABLE IF NOT EXISTS provider_linked_files (
    file_id INTEGER NOT NULL,
    version_change_id INTEGER NOT NULL,
    PRIMARY KEY (file_id, version_change_id),
    FOREIGN KEY (file_id) REFERENCES provider_file (id),
    FOREIGN KEY (version_change_id) REFERENCES provider_version_change (id)
);

CREATE VIEW IF NOT EXISTS provider_version_file_view
AS
    SELECT
           pvc.id as version_id,
           pvc.datetime as version_datetime,
           pp.id as project_id,
           pp.title as project_title,
           pvc.task as version_task,
           pvc.entity_type as version_entity_type,
           pvc.entity_name as version_entity_name,
           pvc.status as version_status,
           pvc.revision as version_revision,
           pvc.comment as version_comment,
           pf.id as file_id,
           pf.code as file_code,
           pf.datetime as file_datetime,
           pf.task as file_task,
           pf.element as file_element,
           pf.extension as file_extension,
           pf.path as file_path
    FROM provider_version_change pvc
             INNER JOIN provider_project pp ON (pp.id = pvc.project_id)
             LEFT OUTER JOIN provider_linked_files plf
                             ON (pvc.id = plf.version_change_id)
             LEFT OUTER JOIN provider_file pf
                             ON (pf.id = plf.file_id);

------------------------------------
--------------  CLIENT  ------------
------------------------------------
CREATE TABLE IF NOT EXISTS client_project (
    id INTEGER NOT NULL,
    origin_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    code TEXT NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS client_file (
    id INTEGER NOT NULL, 
    origin_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    element TEXT NOT NULL,
    extension TEXT NOT NULL,
    path TEXT NOT NULL,
    source TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (project_id) REFERENCES client_project (id)
);
CREATE TABLE IF NOT EXISTS client_version_change (
    id INTEGER NOT NULL,
    origin_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    entity_type TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    task TEXT NOT NULL,
    status TEXT NOT NULL,
    revision INTEGER NOT NULL,
    comment TEXT NOT NULL,
    processed INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (project_id) REFERENCES client_project (id)
);
CREATE TABLE IF NOT EXISTS client_linked_files (
    file_id INTEGER NOT NULL,
    version_change_id INTEGER NOT NULL,
    PRIMARY KEY (file_id, version_change_id),
    FOREIGN KEY (file_id) REFERENCES client_file (id),
    FOREIGN KEY (version_change_id) REFERENCES client_version_change (id)
);
CREATE TABLE IF NOT EXISTS client_source (
    id INTEGER PRIMARY KEY NOT NULL,
    uri TEXT NOT NULL,
    meta TEXT
);

CREATE VIEW IF NOT EXISTS client_version_file_view
AS
    SELECT
           pvc.id as version_id,
           pvc.origin_id as version_origin_id,
           pvc.datetime as version_datetime,
           pvc.status as version_status,
           pvc.source as version_source,
           pp.id as project_id,
           pp.title as project_title,
           pvc.task as version_task,
           pvc.entity_type as version_entity_type,
           pvc.entity_name as version_entity_name,
           pvc.status as version_status,
           pvc.revision as version_revision,
           pvc.comment as version_comment,
           pf.id as file_id,
           pf.origin_id as file_origin_id,
           pf.code as file_code,
           pf.datetime as file_datetime,
           pf.task as file_task,
           pf.element as file_element,
           pf.extension as file_extension,
           pf.path as file_path
    FROM client_version_change pvc
             INNER JOIN client_project pp ON (pp.id = pvc.project_id)
             LEFT OUTER JOIN client_linked_files plf
                             ON (pvc.id = plf.version_change_id)
             LEFT OUTER JOIN client_file pf
                             ON (pf.id = plf.file_id);
"""


async def db_exists() -> bool:
    try:
        db = await db_util.connect_file_db()
        await db.close()
    except Exception:
        return False


async def setup_db() -> Any:
    db = await db_util.connect_file_db()
    await db.executescript(_SCRIPT)
    await db.commit()
    await db.close()

