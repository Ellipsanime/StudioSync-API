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
    id INTEGER NOT NULL,
    tracker_project_id TEXT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS provider_file (
    id INTEGER PRIMARY KEY NOT NULL, 
    tracker_file_id TEXT NULL,
    code TEXT NOT NULL,
    datetime INTEGER NOT NULL,
    version_change_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    element TEXT NOT NULL,
    extension TEXT NOT NULL,
    path TEXT NOT NULL,
    CONSTRAINT fk_pvc
        FOREIGN KEY (version_change_id)
        REFERENCES provider_version_change (id) 
);

CREATE TABLE IF NOT EXISTS provider_version_change (
    id INTEGER PRIMARY KEY NOT NULL,
    tracker_version_change_id TEXT NULL,
    datetime INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    entity_type TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    task TEXT NOT NULL,
    status TEXT NOT NULL,
    revision INTEGER NOT NULL,
    comment TEXT NOT NULL,
    CONSTRAINT fk_pp
        FOREIGN KEY (project_id)
        REFERENCES provider_project (id) 
);

CREATE TRIGGER IF NOT EXISTS UndeleteProviderOrigins 
BEFORE DELETE ON provider_project
FOR EACH ROW
WHEN EXISTS (
  SELECT 1 
  FROM provider_version_change pvc
  WHERE pvc.project_id = OLD.id
)
BEGIN      
  SELECT 
    RAISE(
        ABORT,
        'Can not delete project when it still has related version changes'
    ); 
END;

CREATE TRIGGER IF NOT EXISTS UndeleteProviderVersionChange 
BEFORE DELETE ON provider_version_change
FOR EACH ROW
WHEN EXISTS (
  SELECT 1 
  FROM provider_file pf
  WHERE pf.version_change_id = OLD.id
)
BEGIN      
  SELECT 
    RAISE(
        ABORT,
        'Can not delete version change when it still has related files'
    ); 
END;

CREATE VIEW IF NOT EXISTS provider_version_file_view
AS
    SELECT
           pvc.id as version_id,
           pvc.datetime as version_datetime,
           pp.id as project_id,
           pp.name as project_name,
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
    INNER JOIN provider_project pp 
        ON (pp.id = pvc.project_id)
    LEFT OUTER JOIN provider_file pf
        ON (pvc.id = pf.version_change_id);
"""


async def setup_db() -> Any:
    db = await db_util.connect_file_db()
    await db.executescript(_SCRIPT)
    await db.commit()
    await db.close()

