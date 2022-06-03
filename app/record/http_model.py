from datetime import datetime
from typing import Dict

from box import Box
from pydantic import BaseModel, AnyUrl, Field

from app.record.enumeration import (
    SearchableVersionChangeField,
    SortOrder,
    SortableVersionChangeField,
)
from app.util.data import boxify


def boxify_params(model: BaseModel) -> Box:
    return boxify(model.dict(exclude_unset=True))


class VersionChangeQueryParams(BaseModel):
    filter_field: SearchableVersionChangeField | None = Field(
        title="Filter field name"
    )
    filter_value: str | None = Field(title="Filter value")
    sort_field: SortableVersionChangeField = Field(
        SortableVersionChangeField.VERSION_ID, title="Sort-by field value"
    )
    sort_order: SortOrder = Field(SortOrder.ASC, title="Sort-by order")
    skip: int = Field(0, title="Count of rows to be skipped")
    limit: int = Field(500, title="Amount of rows to return(max: 25)")


class ClientProjectParams(BaseModel):
    id: int | None
    name: str
    code: str
    uri: AnyUrl
    meta: Dict | None


class ClientProjectSplitParams(BaseModel):
    id: int | None
    origin_id: int
    project_id: int
    name: str


class ProviderProjectParams(BaseModel):
    id: int | None
    name: str


class VersionChangeParams(BaseModel):
    id: int | None
    origin_id: int
    datetime: datetime
    project_split_id: int
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
