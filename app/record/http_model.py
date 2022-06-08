from pydantic import BaseModel, Field


class PagingParams(BaseModel):
    skip: int = Field(0, title="Count of rows to be skipped")
    limit: int = Field(500, title="Amount of rows to return(max: 25)")
