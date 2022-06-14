from datetime import datetime
from typing import List, Dict, Any

from box import Box

from app.util.data import boxify


def convert_datetime(entity: Box | Dict, field: Any = "datetime") -> Box:
    if field not in entity:
        return entity
    return boxify({**entity, field: datetime.fromtimestamp(entity[field])})


def get_subdict(entity: Dict[str, Any], key: str) -> Dict[str, Any]:
    return {
        k.replace(key, ""): v for k, v in entity.items() if k.startswith(key)
    }


def map_group(group: List[Box]) -> Box:
    version = convert_datetime(get_subdict(group[0], "version_"))
    project = get_subdict(group[0], "project_")
    linked_files = [
        convert_datetime(get_subdict(x, "file_")) for x in group if x.file_id
    ]
    return boxify(
        {
            **version,
            "project": project,
            "linked_files": linked_files,
        }
    )
