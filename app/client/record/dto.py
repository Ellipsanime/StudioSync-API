from typing import Dict

import attr
from datetime import datetime


@attr.s(auto_attribs=True, frozen=True)
class OriginDto:
    id: int | None
    name: str
    uri: str
    crawling_frequency: int
    connection_info: Dict | None


@attr.s(auto_attribs=True, frozen=True)
class ProjectDto:
    id: int | None
    provider_project_id: int
    name: str


@attr.s(auto_attribs=True, frozen=True)
class VersionChangeDto:
    id: int | None
    datetime: datetime
    provider_version_change_id: int
    origin_id: int
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    processed: bool = False


@attr.s(auto_attribs=True, frozen=True)
class FileDto:
    id: int | None
    provider_file_id: int
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
