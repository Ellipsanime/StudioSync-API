from typing import Dict

import attr
from box import Box
from datetime import datetime


@attr.s(auto_attribs=True, frozen=True)
class DeleteIngestSourceCommand:
    source_name: str


@attr.s(auto_attribs=True, frozen=True)
class UpsertIngestSourceCommand:
    name: str
    uri: str
    meta: Dict | None

    @staticmethod
    def unbox(data: Box) -> "UpsertIngestSourceCommand":
        return UpsertIngestSourceCommand(
            data.name,
            data.uri,
            data.meta or None,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertClientProjectCommand:
    id: int | None
    origin_id: int
    source: str
    name: str
    code: str | None

    @staticmethod
    def unbox(data: Box) -> "UpsertClientProjectCommand":
        return UpsertClientProjectCommand(
            data.id or None,
            data.origin_id,
            data.source,
            data.name,
            data.code or None,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertProviderProjectCommand:
    origin_id: int
    name: str
    code: str | None

    @staticmethod
    def unbox(data: Box) -> "UpsertProviderProjectCommand":
        return UpsertProviderProjectCommand(
            data.origin_id,
            data.name,
            data.code or None,
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
