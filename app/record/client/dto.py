from typing import Dict

import attr
from datetime import datetime


@attr.s(auto_attribs=True, frozen=True)
class OriginDto:
    id: int | None
    name: str
    code: str


@attr.s(auto_attribs=True, frozen=True)
class ProjectDto:
    id: int | None
    origin_id: int
    origin_id: int
    name: str
    uri: str
    meta: Dict | None


@attr.s(auto_attribs=True, frozen=True)
class VersionChangeDto:
    origin_id: int
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    id: int | None = None
    processed: bool = False


@attr.s(auto_attribs=True, frozen=True)
class FileDto:
    origin_id: int
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
    id: int | None = None
