from datetime import datetime

import attr
from box import Box


@attr.s(auto_attribs=True, frozen=True)
class CreateProjectCommand:
    name: str
    project_tracker_id: str

    @staticmethod
    def unbox(data: Box) -> "CreateProjectCommand":
        return CreateProjectCommand(
            data.name,
            data.project_tracker_id
        )


@attr.s(auto_attribs=True, frozen=True)
class CreateVersionChangeCommand:
    project_tracker_id: str
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str

    @staticmethod
    def unbox(data: Box) -> "CreateVersionChangeCommand":
        return CreateVersionChangeCommand(
            data.project_tracker_id,
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
class CreateFileCommand:
    project_tracker_id: str
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
            data.project_tracker_id,
            data.code,
            data.datetime.timestamp(),
            data.version_change_id,
            data.task,
            data.element,
            data.extension,
            data.path,
        )
