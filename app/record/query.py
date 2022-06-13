from datetime import datetime
from typing import List, Tuple

import attr
from box import Box


@attr.s(auto_attribs=True, frozen=True)
class SimpleFetchQuery:
    sort_field: str
    sort_order: str
    skip: int
    limit: int

    @staticmethod
    def unbox(data: Box) -> "SimpleFetchQuery":
        return SimpleFetchQuery(
            data.sort_field.value,
            data.sort_order.value,
            data.skip,
            data.limit,
        )


@attr.s(auto_attribs=True, frozen=True)
class VersionChangeQuery:
    datetime_min: int
    datetime_max: int
    project_name: str | None
    sort_field: str
    sort_order: str
    skip: int
    limit: int

    def param_tuple(self: "VersionChangeQuery") -> Tuple:
        return tuple(
            x
            for x in [
                self.datetime_min,
                self.datetime_max,
                self.project_name,
                self.limit,
                self.skip,
            ]
            if x is not None
        )

    @staticmethod
    def unbox(data: Box) -> "VersionChangeQuery":
        return VersionChangeQuery(
            data.datetime_min.timestamp(),
            data.datetime_max.timestamp(),
            data.project_name,
            data.sort_field.value,
            data.sort_order.value,
            data.skip,
            data.limit,
        )
