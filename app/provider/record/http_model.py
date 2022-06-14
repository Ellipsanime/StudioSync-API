from datetime import datetime

from pydantic import BaseModel, Field

from app.provider.record.enumeration import (
    EnhancedVersionChangeSearchableField,
    EnhancedVersionChangeSortableField,
    VersionChangeField,
    FileField,
)
from app.record.enumeration import SortOrder
from app.record.http_model import PagingParams


class CreateProjectParams(BaseModel):
    tracker_project_id: str
    name: str


class CreateVersionChangeParams(BaseModel):
    tracker_version_change_id: str
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: int
    comment: str


class CreateFileParams(BaseModel):
    tracker_file_id: str
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
