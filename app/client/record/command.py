from typing import Dict

import attr
from box import Box
from datetime import datetime

from returns.curry import curry


@attr.s(auto_attribs=True, frozen=True)
class RemoveOriginCommand:
    origin_id: int


@attr.s(auto_attribs=True, frozen=True)
class UpsertOriginCommand:
    name: str
    uri: str
    crawling_frequency: int
    connection_info: Dict | None
    id: int | None = None

    @staticmethod
    @curry
    def unbox(id_: int | None, data: Box) -> "UpsertOriginCommand":
        return UpsertOriginCommand(
            data.name,
            data.uri,
            data.crawling_frequency,
            data.connection_info,
            id_,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertProjectCommand:
    name: str
    provider_project_id: str | None
    id: int | None = None

    @staticmethod
    @curry
    def unbox(id_: int | None, data: Box) -> "UpsertProjectCommand":
        return UpsertProjectCommand(
            data.name,
            data.provider_project_id,
            id_,
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
    provider_version_change_id: str | None

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
            data.provider_version_change_id,
        )


@attr.s(auto_attribs=True, frozen=True)
class CreateFileCommand:
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
    provider_version_change_id: str | None

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


