from datetime import datetime

import attr


@attr.s(auto_attribs=True, frozen=True)
class ProjectDto:
    id: int | None
    tracker_project_id: str
    name: str


@attr.s(auto_attribs=True, frozen=True)
class VersionChangeDto:
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


@attr.s(auto_attribs=True, frozen=True)
class FileDto:
    id: int | None
    tracker_file_id: str
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
