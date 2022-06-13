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
    filter_field: EnhancedVersionChangeSearchableField | None = Field(
        title="Filter field name"
    )
    filter_value: str | None = Field(title="Filter value")
    sort_field: EnhancedVersionChangeSortableField = Field(
        EnhancedVersionChangeSortableField.VERSION_ID,
        title="Sort-by field value",
    )
    sort_order: SortOrder = Field(SortOrder.ASC, title="Sort-by order")


class OriginParams(BaseModel):
    id: int | None
    project_tracker_id: str
    name: str


class VersionChangeParams(BaseModel):
    id: int | None
    project_tracker_id: str
    datetime: datetime
    project_id: int
    entity_type: str
    entity_name: str
    task: str
    status: str
    revision: str
    comment: str


class FileParams(BaseModel):
    id: int | None
    project_tracker_id: str
    code: str
    datetime: datetime
    version_change_id: int
    task: str
    element: str
    extension: str
    path: str
