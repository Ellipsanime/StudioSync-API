from typing import List

from box import Box
from mimesis import Generic
from mimesis.enums import Locale

from app.record.dto import (
    ClientProjectDto,
    ClientProjectSplitDto,
    VersionChangeDto,
    FileDto,
)

_R = Generic(locale=Locale.DE)


def generate_client_project(num: int = 5) -> List[ClientProjectDto]:
    return [
        ClientProjectDto(
            x,
            f"project_{_R.person.identifier()}_{x}",
            _R.person.identifier().split("/")[0],
            _R.internet.uri(),
            {"key": f"{_R.person.full_name()} {_R.person.university()}"},
        )
        for x in range(1, num + 1)
    ]


def generate_client_project_splits(
    project_id: int, num: int = 5
) -> List[ClientProjectSplitDto]:
    return [
        ClientProjectSplitDto(
            id=x,
            origin_id=_R.numeric.increment(),
            project_id=project_id,
            name=f"{_R.person.full_name()} {_R.person.university()}",
        )
        for x in range(1, num + 1)
    ]


def generate_client_version_changes(
    project_split_id: int,
    num: int = 5,
) -> List[VersionChangeDto]:
    return [
        VersionChangeDto(
            id=x,
            origin_id=_R.numeric.increment(),
            datetime=_R.datetime.datetime().timestamp(),
            project_split_id=project_split_id,
            entity_type=_R.address.country_code(),
            entity_name=_R.person.surname(),
            task=_R.person.surname(),
            status=_R.person.surname(),
            revision=_R.numeric.increment(),
            comment=_R.text.quote(),
            processed=False,
        )
        for x in range(1, num + 1)
    ]


def generate_client_files(
    num: int = 5, version_id=lambda x: int(x / 10) if int(x / 10) else 1
) -> List[FileDto]:
    return [
        FileDto(
            id=x,
            origin_id=_R.numeric.increment(),
            datetime=_R.datetime.datetime().timestamp(),
            version_change_id=version_id(x),
            code=_R.address.country_code(),
            task=_R.person.surname(),
            element=_R.person.surname(),
            extension=_R.file.extension(),
            path=f"{_R.path.project_dir()}/{_R.file.file_name()}",
        )
        for x in range(1, num + 1)
    ]
