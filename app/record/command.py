from typing import Dict

import attr
from box import Box
from datetime import datetime


@attr.s(auto_attribs=True, frozen=True)
class RemoveProjectCommand:
    project_id: int


@attr.s(auto_attribs=True, frozen=True)
class UpsertClientProjectCommand:
    id: int | None
    name: str
    code: str

    @staticmethod
    def unbox(data: Box) -> "UpsertClientProjectCommand":
        return UpsertClientProjectCommand(
            data.id or None,
            data.name,
            data.code,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertClientProjectSplitCommand:
    id: int | None
    origin_id: int
    project_id: int
    name: str
    uri: str
    meta: Dict | None

    @staticmethod
    def unbox(data: Box) -> "UpsertClientProjectSplitCommand":
        return UpsertClientProjectSplitCommand(
            data.id or None,
            data.origin_id,
            data.project_id,
            data.name,
            data.uri,
            data.meta or None,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpdateClientVersionChangeCommand:
    id: int
    processed: bool

    @staticmethod
    def unbox(data: Box) -> "UpdateClientVersionChangeCommand":
        return UpdateClientVersionChangeCommand(
            data.id,
            data.processed,
        )


@attr.s(auto_attribs=True, frozen=True)
class CreateClientVersionChangeCommand:
    origin_id: int
    datetime: datetime
    project_split_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    processed: bool

    @staticmethod
    def unbox(data: Box) -> "CreateClientVersionChangeCommand":
        return CreateClientVersionChangeCommand(
            data.origin_id,
            data.datetime.timestamp(),
            data.project_split_id,
            data.entity_type,
            data.entity_name,
            data.task,
            data.status,
            data.revision,
            data.comment,
            data.processed or False,
        )


@attr.s(auto_attribs=True, frozen=True)
class CreateClientFileCommand:
    origin_id: int
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str

    @staticmethod
    def unbox(data: Box) -> "CreateClientFileCommand":
        return CreateClientFileCommand(
            data.origin_id,
            data.code,
            data.datetime.timestamp(),
            data.version_change_id,
            data.task,
            data.element,
            data.extension,
            data.path,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertProviderProjectSplitCommand:
    id: int | None
    name: str
    tracker_id: str

    @staticmethod
    def unbox(data: Box) -> "UpsertProviderProjectSplitCommand":
        return UpsertProviderProjectSplitCommand(
            data.id or None,
            data.name,
            data.tracker_id
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertProviderVersionChangeCommand:
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

    @staticmethod
    def unbox(data: Box) -> "UpsertProviderVersionChangeCommand":
        return UpsertProviderVersionChangeCommand(
            data.tracker_id,
            data.datetime.timestamp(),
            data.project_split_id,
            data.entity_type,
            data.entity_name,
            data.task,
            data.status,
            data.revision,
            data.comment,
            data.id or None,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertProviderFileCommand:
    tracker_id: str
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
    id: int | None = None

    @staticmethod
    def unbox(data: Box) -> "UpsertProviderFileCommand":
        return UpsertProviderFileCommand(
            data.tracker_id,
            data.code,
            data.datetime.timestamp(),
            data.version_change_id,
            data.task,
            data.element,
            data.extension,
            data.path,
            data.id or None,
        )
