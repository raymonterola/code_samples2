import inspect
from marshmallow import validate, fields, Schema as MarshmallowSchema
from marshmallow.utils import EXCLUDE

from src.classes import validators
from src import strings
from configs import config


class Schema(MarshmallowSchema):
    """Schema to exclude unknown properties by default."""

    class Meta:
        unknown = EXCLUDE


def get_int_field(name: str, strict=True, required=True, extra_validators=None, allow_none=False, **kwargs) -> fields.Integer:
    """Generate Integer field.

    Args:
        name (str): Field name.
        strict (bool, optional): If input value should strictly be int,
            defaults to True.
        required (bool, optional): If field is required, defaults to True.
        extra_validators (list, optional): Extra validators for field.
        allow_none (bool, optional): If None is valid value for field.
        **kwargs: Other parameters for Field constructor.

    Returns:
        :class:`marshmallow.fields.Integer`: Integer field.

    """
    if extra_validators is None:
        extra_validators = []
    return fields.Integer(
        required=required, strict=strict, allow_none=allow_none,
        error_messages={"invalid": strings.must_be_positive_integer % name,
                        "required": strings.missing_required_field % name,
                        "null": strings.field_may_not_be_null % name},
        validate=extra_validators,
        **kwargs
    )


def get_positive_int_field(name: str, strict=True, required=True, extra_validators=None, allow_none=False, **kwargs) -> fields.Integer:
    """Generate positive Integer field.

    Args:
        name (str): Field name.
        strict (bool, optional): If input value should strictly be int,
            defaults to True.
        required (bool, optional): If field is required, defaults to True.
        extra_validators (list, optional): Extra validators for field.
        allow_none (bool, optional): If None is valid value for field.
        **kwargs: Other parameters for Field constructor.

    Returns:
        :class:`marshmallow.fields.Integer`: Integer field.

    """
    if extra_validators is None:
        extra_validators = []
    return fields.Integer(
        required=required, strict=strict, allow_none=allow_none,
        error_messages={"invalid": strings.must_be_positive_integer % name,
                        "required": strings.missing_required_field % name,
                        "null": strings.field_may_not_be_null % name },
        validate=[validate.Range(min=1, error=strings.must_be_positive_integer % name),
                  *extra_validators],
        **kwargs
    )


def get_non_negative_int_field(name: str, strict=True, required=True, allow_none=False,
                               extra_validators=None, **kwargs) -> fields.Integer:
    """Generate Integer field. Value must be positive integer or zero.

    Args:
        name (str): Field name.
        strict (bool, optional): If input value should strictly be int,
            defaults to True.
        required (bool, optional): If field is required, defaults to True.
        extra_validators (list, optional): Extra validators for field.
        allow_none (bool, optional): If None is valid value for field.
        **kwargs: Other parameters for Field constructor.

    Returns:
        :class:`marshmallow.fields.Integer`: Integer field.

    """
    if extra_validators is None:
        extra_validators = []
    return fields.Integer(
        required=required, strict=strict, allow_none=allow_none,
        error_messages={"invalid": strings.must_be_integer % name,
                        "required": strings.missing_required_field % name,
                        "null": strings.field_may_not_be_null % name },
        validate=[validate.Range(min_inclusive=0, error=strings.must_be_non_negative_integer % name),
                  *extra_validators],
        **kwargs
    )


def get_string_field(name, strict=True, required=True, extra_validators=None, allow_empty=False, allow_none=False) -> fields.String:
    """Generate String field.

    Args:
        name (str): Field name.
        strict (bool, optional): If input value should strictly be int,
            defaults to True.
        required (bool, optional): If field is required, defaults to True.
        extra_validators (list, optional): Extra validators for field.
        allow_empty (bool, optional): If empty strings should be allowed,
            defaults to False.
        allow_none (bool, optional): If None is valid value for field.

    Returns:
        :class:`marshmallow.fields.String`: String field.

    """
    validators_ = [validators.non_empty_string(name)]
    if allow_empty:
        validators_ = []
    if extra_validators is not None and isinstance(extra_validators, list):
        validators_.extend(extra_validators)

    return fields.String(
        required=required, strict=strict,
        validate=validators_,
        allow_none=allow_none,
        error_messages={
            "required": strings.missing_required_field % name,
            "invalid": strings.must_be_string % name,
            "null": strings.field_may_not_be_null % name,
        },
        allow_empty=True
    )


def get_email_field(name, strict=True, required=True, allow_none=False) -> fields.Email:
    """Generate Email field. Same as String field but with Email validation.

    Args:
        name (str): Field name.
        strict (bool, optional): If input value should strictly be int,
            defaults to True.
        required (bool, optional): If field is required, defaults to True.
        allow_none (bool, optional): If None is valid value for field.

    Returns:
        :class:`marshmallow.fields.Email`: Email field.

    """
    return fields.Email(
        strict=strict, required=required, validate=(validators.non_empty_string(name)),
        allow_none=allow_none,
        error_messages={"invalid": strings.not_valid_email,
                        "null": strings.field_may_not_be_null % name}
    )


def get_list_field(name, schema_or_field, required=True, allow_empty=False, allow_none=False, **kwargs) -> fields.List:
    """Generate List field containing specific field type or schema.

    Args:
        name (str): Field name.
        schema_or_field (:class:`marshmallow.Field`, :class:`marshmallow.Schema`):
            Type of list items. Field or Schema instance are valid.
        required (bool, optional): If field is required, defaults to True.
        allow_empty (bool, optional): If empty strings should be allowed,
            defaults to False.
        allow_none (bool, optional): If None is valid value for field.
        **kwargs: Other parameters for Field constructor.

    Returns:
        :class:`marshmallow.fields.List`: List field.

    """
    is_nested = isinstance(schema_or_field, Schema) or (
        inspect.isclass(schema_or_field) and issubclass(schema_or_field, Schema))
    validators_ = []
    if not allow_empty:
        validators_.append(validate.Length(min=1, error=strings.list_must_be_non_empty % name))
    return fields.List(
        fields.Nested(schema_or_field) if is_nested else schema_or_field,
        allow_none=allow_none,
        error_messages={"type": strings.must_be_list % name,
                        "invalid": strings.must_be_list % name,
                        "required": strings.missing_required_field % name,
                        "null": strings.field_may_not_be_null % name},
        required=required, validate=validators_,
        **kwargs
    )


def get_boolean_field(name, required=True):
    """Generate Boolean field.

    Args:
        name (str): Field name.
        required (bool, optional): If field is required.

    Returns:
        :class:`marshmallow.fields.Boolean`: Boolean field.

    """
    return fields.Boolean(
        required=required,
        error_messages={"invalid": strings.must_be_boolean % name,
                        "required": strings.missing_required_field % name}
    )


def get_raw_field(name, required=True, allow_none=False):
    """Generate Raw field. Does not modify input value.

    Args:
        name (str): Field name.
        required (bool, optional): If field is required, defaults to True.
        allow_none (bool, optional): If NoneType should be valid, defaults
            to False.

    Returns:
        :class:`marshmallow.fields.Raw`: Raw field.

    """
    return fields.Raw(
        required=required, allow_none=allow_none,
        error_messages={
            "required": strings.missing_required_field % name,
            "null": strings.field_may_not_be_null % name,
        }
    )


# shared schemas

class WorkspaceSchema(Schema):
    workspaceId = get_non_negative_int_field("workspaceId", strict=False)

class GenericWorkspaceSchema(Schema):
    workspaceId = get_raw_field("workspaceId")


class ZohoWorkspaceSchema(Schema):
    workspaceId = get_string_field("workspaceId", strict=False, allow_empty=False)


class ZohoOrgSchema(Schema):
    orgId = get_string_field("orgId", strict=False, allow_empty=False)

class ZohoViewSchema(Schema):
    orgId = get_string_field("orgId", strict=False, allow_empty=False)
    workspaceId = get_string_field("workspaceId", strict=False, allow_empty=False)


class PropertySchema(Schema):
    propertyValue = fields.Raw(required=True)
    error_messages = {"type": "'properties' value must be an object."}


class DeviceGroupSchema(Schema):
    workspaceId = get_non_negative_int_field("workspaceId", strict=False)
