import validators
from box import Box
from pydantic import BaseModel, Field, validator
from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass
from datetime import datetime

from app.util.data import boxify


def boxify_http_model(model: BaseModel) -> Box:
    return boxify(model.dict(exclude_unset=True))


class IngestSourceHttpModel(BaseModel):
    name: str = Field(title="source name")
    uri: str = Field(title="queryable source uri")
    meta: str | None = Field(title="related meta data")


class ClientProjectHttpModel(BaseModel):
    id: int | None = Field(title="internal project id")
    origin_id: int = Field(title="origin id")
    source: str = Field(title="source of project")
    name: str = Field(title="project name")
    code: str | None = Field(title="project code")


class ProviderProjectHttpModel(BaseModel):
    id: int | None = Field(title="internal project id")
    origin_id: int = Field(title="origin id")
    name: str = Field(title="project name")
    code: str | None = Field(title="project code")


class VersionChangeHttpModel(BaseModel):
    id: int | None = Field(title="internal id")
    origin_id: int = Field(title="origin id")
    datetime: datetime = Field(title="date")
    project_id: int = Field(title="internal project id")
    entity_type: str = Field(title="related entity type")
    entity_name: str = Field(title="related entity name")
    task: str = Field(title="related task")
    status: str = Field(title="change status")
    revision: str = Field(title="revision number")
    comment: str = Field(title="related comment")
    processed: bool = Field(title="processed indicator")


class FileHttpModel(BaseModel):
    id: int | None = Field(title="internal id")
    origin_id: int = Field(title="origin id")
    code: str = Field(title="file code")
    datetime: datetime = Field(title="file date")
    version_change_id: int = Field(title="related version change id")
    task: str = Field(title="related task")
    element: str = Field(title="nature of the file")
    extension: str = Field(title="file extension")
    path: str = Field(title="physical path")


