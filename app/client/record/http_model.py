import sys
from datetime import datetime
from typing import Dict

from pydantic import BaseModel, AnyUrl, Field

from app.client.record.enumeration import (
    EnhancedVersionChangeSearchableField,
    EnhancedVersionChangeSortableField,
    VersionChangeField,
    FileField,
)
from app.record.enumeration import SortOrder
from app.record.http_model import PagingParams


class FileFetchParams(PagingParams):
    sort_field: FileField = Field(
        FileField.ID,
        title="Sort-by field value",
    )
    sort_order: SortOrder = Field(SortOrder.ASC, title="Sort-by order")


class VersionChangeFetchParams(PagingParams):
    sort_field: VersionChangeField = Field(
        VersionChangeField.ID,
        title="Sort-by field value",
    )
    sort_order: SortOrder = Field(SortOrder.ASC, title="Sort-by order")


class EnhancedVersionChangeFetchParams(PagingParams):
    datetime_min: datetime | None = Field(
        datetime.fromtimestamp(0),
        title="Datetime min",
    )
    datetime_max: datetime | None = Field(
        datetime.fromtimestamp(32536799999-1),
        title="Datetime max",
    )
    project_name: str | None = Field(None, title="Project name")
    sort_field: EnhancedVersionChangeSortableField = Field(
        EnhancedVersionChangeSortableField.VERSION_ID,
        title="Sort-by field value",
    )
    sort_order: SortOrder = Field(SortOrder.ASC, title="Sort-by order")


class OriginParams(BaseModel):
    id: int | None
    name: str
    code: str


class ProjectParams(BaseModel):
    id: int | None
    origin_id: int
    origin_id: int
    name: str
    uri: AnyUrl
    meta: Dict | None


class VersionChangeParams(BaseModel):
    id: int | None
    origin_id: int
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str
    processed: bool = False


class UpdateVersionChangeParams(BaseModel):
    processed: bool


class FileParams(BaseModel):
    id: int | None
    origin_id: int
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
