from typing import Type, Dict, Any

import attr
from returns.curry import curry
from datetime import datetime


@curry
def dto_from_attr(ctor: Type, data: Any) -> Type:
    return ctor(**attr.asdict(data))


@attr.s(auto_attribs=True, frozen=True)
class ClientIngestSourceDto:
    name: str
    uri: str
    meta: Dict | None


@attr.s(auto_attribs=True, frozen=True)
class ProjectDto:
    id: int | None
    origin_id: int
    name: str
    code: str | None


@attr.s(auto_attribs=True, frozen=True)
class ClientProjectDto(ProjectDto):
    source: str


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
    id: int | None
    origin_id: int
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
