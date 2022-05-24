import validators
from box import Box
from pydantic import BaseModel, Field, validator
from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass

from app.util.data import boxify


def boxify_http_model(model: BaseModel) -> Box:
    return boxify(model.dict(exclude_unset=True))


class ClientProject(BaseModel):
    id: int | None = Field(None, title="internal project id")
    origin_id: int = Field(None, title="origin id")
    source: str = Field(None, title="source of project")
    name: str = Field(None, title="project name")
    code: str | None = Field(None, title="project code")


class ClientVersionChange(BaseModel):
    id: int | None = Field(title="internal id")
    origin_id: int = Field(title="origin id")
    datetime = Field(title="date")
    project_id = Field(title="internal project id")
    entity_type = Field(title="related entity type")
    entity_name = Field(title="related entity name")
    task = Field(title="related task")
    status = Field(title="change status")
    revision = Field(title="revision number")
    comment = Field(title="related comment")
    processed = Field(title="processed indicator")


class ClientFile(BaseModel):
    id: int | None = Field(title="internal id")
    origin_id: int = Field(title="origin id")

