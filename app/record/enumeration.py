from enum import Enum


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


class SearchableVersionChangeField(Enum):
    VERSION_ID = "version_id"
    VERSION_ORIGIN_ID = "version_origin_id"
    VERSION_SOURCE = "version_source"
    VERSION_TASK = "version_task"
    VERSION_ENTITY_TYPE = "version_entity_type"
    VERSION_ENTITY_NAME = "version_entity_name"
    VERSION_STATUS = "version_status"
    VERSION_REVISION = "version_revision"
    VERSION_PROCESSED = "version_processed"
    VERSION_COMMENT = "version_comment"
    PROJECT_SPLIT_NAME = "project_split_name"
    FILE_ID = "file_id"
    FILE_ORIGIN_ID = "file_origin_id"
    FILE_CODE = "file_code"
    FILE_TASK = "file_task"
    FILE_ELEMENT = "file_element"
    FILE_EXTENSION = "file_extension"


class SortableVersionChangeField(Enum):
    VERSION_ID = "version_id"
    VERSION_ORIGIN_ID = "version_origin_id"
    VERSION_SOURCE = "version_source"
    VERSION_TASK = "version_task"
    VERSION_DATETIME = "version_datetime"
    VERSION_ENTITY_TYPE = "version_entity_type"
    VERSION_ENTITY_NAME = "version_entity_name"
    VERSION_STATUS = "version_status"
    VERSION_REVISION = "version_revision"
    VERSION_PROCESSED = "version_processed"
