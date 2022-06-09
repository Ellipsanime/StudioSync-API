from datetime import datetime

import attr


@attr.s(auto_attribs=True, frozen=True)
class ProjectDto:
    id: int | None
    project_tracker_id: str
    name: str


@attr.s(auto_attribs=True, frozen=True)
class VersionChangeDto:
    project_tracker_id: str
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    id: int | None = None


@attr.s(auto_attribs=True, frozen=True)
class FileDto:
    id: int | None
    project_tracker_id: str
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
