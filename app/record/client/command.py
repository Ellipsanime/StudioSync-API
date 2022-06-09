from typing import Dict

import attr
from box import Box
from datetime import datetime


@attr.s(auto_attribs=True, frozen=True)
class RemoveOriginCommand:
    origin_id: int


@attr.s(auto_attribs=True, frozen=True)
class UpsertOriginCommand:
    id: int | None
    name: str
    code: str

    @staticmethod
    def unbox(data: Box) -> "UpsertOriginCommand":
        return UpsertOriginCommand(
            data.id or None,
            data.name,
            data.code,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertProjectCommand:
    id: int | None
    origin_id: int
    origin_id: int
    name: str
    uri: str
    meta: Dict | None

    @staticmethod
    def unbox(data: Box) -> "UpsertProjectCommand":
        return UpsertProjectCommand(
            data.id or None,
            data.origin_id,
            data.origin_id,
            data.name,
            data.uri,
            data.meta or None,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpdateVersionChangeCommand:
    id: int
    processed: bool

    @staticmethod
    def unbox(data: Box) -> "UpdateVersionChangeCommand":
        return UpdateVersionChangeCommand(
            data.id,
            data.processed,
        )


@attr.s(auto_attribs=True, frozen=True)
class CreateVersionChangeCommand:
    origin_id: int
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    processed: bool

    @staticmethod
    def unbox(data: Box) -> "CreateVersionChangeCommand":
        return CreateVersionChangeCommand(
            data.origin_id,
            data.datetime.timestamp(),
            data.project_id,
            data.entity_type,
            data.entity_name,
            data.task,
            data.status,
            data.revision,
            data.comment,
            data.processed or False,
        )


@attr.s(auto_attribs=True, frozen=True)
class CreateFileCommand:
    origin_id: int
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str

    @staticmethod
    def unbox(data: Box) -> "CreateFileCommand":
        return CreateFileCommand(
            data.origin_id,
            data.code,
            data.datetime.timestamp(),
            data.version_change_id,
            data.task,
            data.element,
            data.extension,
            data.path,
        )


