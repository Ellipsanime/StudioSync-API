from typing import List

from mimesis import Generic
from mimesis.enums import Locale

import app.client.record.dto as client_dto
import app.provider.record.dto as provider_dto


_R = Generic(locale=Locale.DE)


def generate_client_origin(num: int = 5) -> List[client_dto.OriginDto]:
    return [
        client_dto.OriginDto(
            id=x,
            name=_R.person.identifier().split("/")[0],
            uri=_R.internet.uri(),
            crawling_frequency=_R.numeric.increment(),
            connection_info={
                "key": f"{_R.person.full_name()} {_R.person.university()}"
            },
        )
        for x in range(1, num + 1)
    ]


def generate_client_projects(num: int = 5) -> List[client_dto.ProjectDto]:
    return [
        client_dto.ProjectDto(
            id=x,
            name=_R.person.identifier().split("/")[0],
            provider_project_id=x * 2,
        )
        for x in range(1, num + 1)
    ]


def generate_client_version_changes(
    origin_id: int,
    project_id: int,
    num: int = 5,
) -> List[client_dto.VersionChangeDto]:
    return [
        client_dto.VersionChangeDto(
            id=x,
            provider_version_change_id=_R.numeric.increment(),
            origin_id=origin_id,
            datetime=_R.datetime.datetime().timestamp(),
            project_id=project_id,
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
) -> List[client_dto.FileDto]:
    return [
        client_dto.FileDto(
            id=x,
            provider_file_id=_R.numeric.increment(),
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


def generate_provider_projects(
    num: int = 5,
) -> List[provider_dto.ProjectDto]:
    return [
        provider_dto.ProjectDto(
            id=x,
            tracker_project_id=str(_R.person.identifier()),
            name=f"{_R.person.full_name()} {_R.person.university()}",
        )
        for x in range(1, num + 1)
    ]


def generate_provider_version_changes(
    project_id: int,
    num: int = 5,
) -> List[provider_dto.VersionChangeDto]:
    return [
        provider_dto.VersionChangeDto(
            id=x,
            datetime=_R.datetime.datetime().timestamp(),
            project_id=project_id,
            tracker_version_change_id=_R.numeric.increment(),
            entity_type=_R.address.country_code(),
            entity_name=_R.person.surname(),
            task=_R.person.surname(),
            status=_R.person.surname(),
            revision=_R.numeric.increment(),
            comment=_R.text.quote(),
        )
        for x in range(1, num + 1)
    ]


def generate_provider_files(
    num: int = 5, version_id=lambda x: int(x / 10) if int(x / 10) else 1
) -> List[provider_dto.FileDto]:
    return [
        provider_dto.FileDto(
            id=x,
            datetime=_R.datetime.datetime().timestamp(),
            version_change_id=version_id(x),
            code=_R.address.country_code(),
            task=_R.person.surname(),
            element=_R.person.surname(),
            extension=_R.file.extension(),
            path=f"{_R.path.project_dir()}/{_R.file.file_name()}",
            tracker_file_id=_R.person.identifier(),
        )
        for x in range(1, num + 1)
    ]
