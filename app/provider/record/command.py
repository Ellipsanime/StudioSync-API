from datetime import datetime

import attr
from box import Box
from returns.curry import curry


@attr.s(auto_attribs=True, frozen=True)
class UpsertProjectCommand:
    id: int | None
    name: str
    tracker_project_id: str

    @staticmethod
    @curry
    def unbox(id_: int | None, data: Box) -> "UpsertProjectCommand":
        return UpsertProjectCommand(
            id_,
            data.name,
            data.tracker_project_id
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertVersionChangeCommand:
    id: int | None
    tracker_version_change_id: str
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str

    @staticmethod
    @curry
    def unbox(id_: int | None, data: Box) -> "UpsertVersionChangeCommand":
        return UpsertVersionChangeCommand(
            id_,
            data.tracker_version_change_id,
            data.datetime.timestamp(),
            data.project_id,
            data.entity_type,
            data.entity_name,
            data.task,
            data.status,
            data.revision,
            data.comment,
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertFileCommand:
    id: int | None
    tracker_file_id: str
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str

    @staticmethod
    @curry
    def unbox(id_: int | None, data: Box) -> "UpsertFileCommand":
        return UpsertFileCommand(
            id_,
            data.tracker_file_id,
            data.code,
            data.datetime.timestamp(),
            data.version_change_id,
            data.task,
            data.element,
            data.extension,
            data.path,
        )
