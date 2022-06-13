from enum import Enum


class OriginField(Enum):
    ID = "id"
    NAME = "name"
    CODE = "code"


class ProjectField(Enum):
    ID = "id"
    ORIGIN_ID = "origin_id"
    PROJECT_ID = "origin_id"
    NAME = "name"
    URI = "uri"
    META = "meta"


class VersionChangeField(Enum):
    ID = "id"
    ORIGIN_ID = "origin_id"
    DATETIME = "datetime"
    PROJECT_SPLIT_ID = "project_id"
    ENTITY_TYPE = "entity_type"
    ENTITY_NAME = "entity_name"
    TASK = "task"
    STATUS = "status"
    REVISION = "revision"
    COMMENT = "comment"
    PROCESSED = "processed"


class FileField(Enum):
    ID = "id"
    ORIGIN_ID = "origin_id"
    CODE = "code"
    DATETIME = "datetime"
    VERSION_CHANGE_ID = "version_change_id"
    TASK = "task"
    ELEMENT = "element"
    EXTENSION = "extension"
    PATH = "path"


class EnhancedVersionChangeSearchableField(Enum):
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
    PROJECT_SPLIT_NAME = "project_name"
    FILE_ID = "file_id"
    FILE_ORIGIN_ID = "file_origin_id"
    FILE_CODE = "file_code"
    FILE_TASK = "file_task"
    FILE_ELEMENT = "file_element"
    FILE_EXTENSION = "file_extension"


class EnhancedVersionChangeSortableField(Enum):
    VERSION_ID = "version_id"
    VERSION_DATETIME = "version_datetime"
    PROJECT_ID = "project_id"
    PROJECT_NAME = "project_name"
    VERSION_TASK = "version_task"
    VERSION_ENTITY_TYPE = "version_entity_type"
    VERSION_ENTITY_NAME = "version_entity_name"
    VERSION_STATUS = "version_status"
    VERSION_REVISION = "version_revision"
    VERSION_COMMENT = "version_comment"
