import pytest

from testapp.models import Record, Configuration
from pydantic_django import PydanticDjangoModel


@pytest.mark.django_db
def test_custom_field():
    """
    Test a model using custom field subclasses.
    """

    class RecordSchema(PydanticDjangoModel):
        class Config:
            model = Record
            include = ["id", "title", "items"]

    assert RecordSchema.schema() == {
        "description": "A generic record model.",
        "properties": {
            "id": {"title": "Id", "type": "integer"},
            "items": {
                "anyOf": [
                    {"format": "json-string", "type": "string"},
                    {"type": "object"},
                    {"items": {}, "type": "array"},
                ],
                "title": "Items",
            },
            "title": {"maxLength": 20, "title": "Title", "type": "string"},
        },
        "required": ["title"],
        "title": "RecordSchema",
        "type": "object",
    }


@pytest.mark.django_db
def test_postgres_json_field():
    """
    Test generating a schema for multiple Postgres JSON fields.
    """

    class ConfigurationSchema(PydanticDjangoModel):
        class Config:
            model = Configuration
            include = ["permissions", "changelog", "metadata"]

    assert ConfigurationSchema.schema() == {
        "title": "ConfigurationSchema",
        "description": "A configuration container.",
        "type": "object",
        "properties": {
            "permissions": {
                "title": "Permissions",
                "anyOf": [
                    {"type": "string", "format": "json-string"},
                    {"type": "object"},
                    {"type": "array", "items": {}},
                ],
            },
            "changelog": {
                "title": "Changelog",
                "anyOf": [
                    {"type": "string", "format": "json-string"},
                    {"type": "object"},
                    {"type": "array", "items": {}},
                ],
            },
            "metadata": {
                "title": "Metadata",
                "anyOf": [
                    {"type": "string", "format": "json-string"},
                    {"type": "object"},
                    {"type": "array", "items": {}},
                ],
            },
        },
    }


@pytest.mark.django_db
def test_lazy_choice_field():
    """
    Test generating a dynamic enum choice field.
    """

    class RecordSchema(PydanticDjangoModel):
        class Config:
            model = Record
            include = ["record_type", "record_status"]

    assert RecordSchema.schema() == {
        "definitions": {
            "RecordStatusEnum": {
                "description": "An enumeration.",
                "enum": [0, 1, 2],
                "title": "RecordStatusEnum",
            },
            "RecordTypeEnum": {
                "description": "An enumeration.",
                "enum": ["NEW", "OLD"],
                "title": "RecordTypeEnum",
            },
        },
        "description": "A generic record model.",
        "properties": {
            "record_status": {"$ref": "#/definitions/RecordStatusEnum"},
            "record_type": {"$ref": "#/definitions/RecordTypeEnum"},
        },
        "title": "RecordSchema",
        "type": "object",
    }
