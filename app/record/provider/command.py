from datetime import datetime

import attr
from box import Box


@attr.s(auto_attribs=True, frozen=True)
class UpsertProjectSplitCommand:
    id: int | None
    name: str
    tracker_id: str

    @staticmethod
    def unbox(data: Box) -> "UpsertProjectSplitCommand":
        return UpsertProjectSplitCommand(
            data.id or None,
            data.name,
            data.tracker_id
        )


@attr.s(auto_attribs=True, frozen=True)
class UpsertVersionChangeCommand:
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
    def unbox(data: Box) -> "UpsertVersionChangeCommand":
        return UpsertVersionChangeCommand(
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
class UpsertFileCommand:
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
    def unbox(data: Box) -> "UpsertFileCommand":
        return UpsertFileCommand(
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
