from typing import Type, Dict, Any

import attr
from returns.curry import curry
from datetime import datetime


@curry
def dto_from_attr(ctor: Type, data: Any) -> Type:
    return ctor(**attr.asdict(data))


@attr.s(auto_attribs=True, frozen=True)
class ClientProjectDto:
    id: int | None
    name: str
    code: str


@attr.s(auto_attribs=True, frozen=True)
class ClientProjectSplitDto:
    id: int | None
    project_id: int
    origin_id: int
    name: str
    uri: str
    meta: Dict | None


@attr.s(auto_attribs=True, frozen=True)
class ClientVersionChangeDto:
    origin_id: int
    datetime: datetime
    project_split_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    id: int | None = None
    processed: bool = False


@attr.s(auto_attribs=True, frozen=True)
class ClientFileDto:
    id: int | None
    origin_id: int
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str


@attr.s(auto_attribs=True, frozen=True)
class ProviderProjectSplitDto:
    id: int | None
    tracker_id: str
    name: str


@attr.s(auto_attribs=True, frozen=True)
class ProviderVersionChangeDto:
    tracker_id: str
    datetime: datetime
    project_split_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    id: int | None = None


@attr.s(auto_attribs=True, frozen=True)
class ProviderFileDto:
    id: int | None
    tracker_id: str
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
