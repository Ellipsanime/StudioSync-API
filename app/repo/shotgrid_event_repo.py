from datetime import datetime, timedelta
from typing import Any, List, Dict, Union, Iterator, Optional

from app.util.connectivity import shotgrid
from app.util.logger import get_logger

Map = Dict[str, Any]

_LOG = get_logger(__name__)

_LIMIT = 500
_TYPE = "EventLogEntry"
_ORDER = [{"column": "created_at", "direction": "asc"}]
_FIELDS = [
    "id",
    "event_type",
    "attribute_name",
    "meta",
    "entity",
    "user",
    "project",
    "session_uuid",
    "created_at",
]
_FILTERS = [
    {
        "filter_operator": "all",
        "filters": [
            ["project", "is_not", None],
            ["entity", "is_not", None],
        ],
    }
]
_MIN_SHIFT = timedelta(minutes=15)
_IGNORED_EVENT_TYPE = {"Shotgun_Attachment_View"}


def _filters_with_id(last_id: int) -> List[Dict[str, Any]]:
    return [
        *_FILTERS,
        {
            "filter_operator": "all",
            "filters": [["id", "greater_than", last_id]],
        },
    ]


def _filters_with_created_at(date: datetime) -> List[Dict[str, Any]]:
    return [
        *_FILTERS,
        {
            "filter_operator": "all",
            "filters": [["created_at", "greater_than", date]],
        },
    ]


def _is_valid_meta(meta: Optional[Map]) -> bool:
    if not meta:
        return False
    if meta.get("field_data_type") != "status_list":
        return False
    return meta.get("attribute_name", "").startswith("sg_status_")


def _post_filter_events(events: List[Map]) -> Iterator[Map]:
    for x in events:
        if not _is_valid_meta(x.get("meta")):
            continue
        if x.get("event_type") in _IGNORED_EVENT_TYPE:
            continue
        yield x


def _fetch_events(
    filters: List[Union[List[Any], Dict[str, str]]]
) -> List[Dict[str, Any]]:
    client = shotgrid()
    raw_events = client.find(_TYPE, filters, _FIELDS, _ORDER, _LIMIT)
    return list(_post_filter_events(raw_events))


def find_latest_events_by_id(last_id: int) -> List[Dict[str, Any]]:
    _LOG.info(f"find latest events with id: {last_id}")
    return _fetch_events(_filters_with_id(last_id))


def find_latest_events_by_date(
    raw_date: datetime = datetime.utcnow() - _MIN_SHIFT,
) -> List[Dict[str, Any]]:
    date_time = raw_date.replace(microsecond=0, second=0)
    _LOG.info(f"find latest events with date_time: {date_time}")
    return _fetch_events(_filters_with_created_at(date_time))
