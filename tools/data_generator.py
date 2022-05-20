from typing import List

from box import Box
from mimesis import Generic
from mimesis.enums import Locale

from app.util.data import boxify

_R = Generic(locale=Locale.DE)


def generate_client_projects(source: str, num: int = 5) -> List[Box]:
    return [
        boxify(
            {
                "id": x,
                "origin_id": _R.numeric.increment(),
                "source": source,
                "title": f"{_R.person.full_name()} {_R.person.university()}",
                "code": _R.person.identifier(),
            }
        )
        for x in range(1, num + 1)
    ]


def generate_client_version_changes(
    source: str,
    project_id: int,
    num: int = 5,
) -> List[Box]:
    return [
        boxify(
            {
                "id": x,
                "origin_id": _R.numeric.increment(),
                "source": source,
                "datetime": _R.datetime.datetime().timestamp(),
                "project_id": project_id,
                "entity_type": _R.address.country_code(),
                "entity_name": _R.person.surname(),
                "task": _R.person.surname(),
                "status": _R.person.surname(),
                "revision": _R.numeric.increment(),
                "comment": _R.text.quote(),
                "processed": 0,
            }
        )
        for x in range(1, num + 1)
    ]


def generate_client_files(
    source: str,
    project_id: int,
    num: int = 5,
) -> List[Box]:
    return [
        boxify(
            {
                "id": x,
                "origin_id": _R.numeric.increment(),
                "source": source,
                "datetime": _R.datetime.datetime().timestamp(),
                "project_id": project_id,
                "code": _R.address.country_code(),
                "task": _R.person.surname(),
                "element": _R.person.surname(),
                "extension": _R.file.extension(),
                "path": f"{_R.path.project_dir()}/{_R.file.file_name()}",
            }
        )
        for x in range(1, num + 1)
    ]

