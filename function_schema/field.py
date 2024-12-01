from dataclasses import dataclass, field
from typing import Optional, Literal, Union, List

Numeric = Union[int, float]
AlphaNumeric = Union[str, Numeric, None]


@dataclass
class FieldInfo:
    """
    A class to represent the schema of a field with various attributes.
    Not all attributes that exist in the JSON schema are included here (yet).
    Attributes:
    ----------
    type : Optional[Literal["object", "array", "string", "number", "integer", "boolean"]]
        The type of the field.
    description : Optional[str]
        A brief description of the field.
    enum : Optional[List[AlphaNumeric]]
        A list of allowed values for the field.
    required : Optional[bool]
        Indicates if the field is required.
    minimum : Optional[Numeric]
        The minimum value for the field.
    maximum : Optional[Numeric]
        The maximum value for the field.
    exclusive_minimum : Optional[Numeric]
        The exclusive minimum value for the field.
    exclusive_maximum : Optional[Numeric]
        The exclusive maximum value for the field.
    max_length : Optional[int]
        The maximum length of the field.
    min_length : Optional[int]
        The minimum length of the field.
    pattern : Optional[str]
        A regex pattern that the field value must match.
    """

    type: Optional[Literal["object", "array", "string",
                           "number", "integer", "boolean"]] = None
    description: Optional[str] = None
    enum: Optional[List[AlphaNumeric]] = None
    required: Optional[bool] = None
    minimum: Optional[Numeric] = None
    maximum: Optional[Numeric] = None
    exclusive_minimum: Optional[Numeric] = None
    exclusive_maximum: Optional[Numeric] = None
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None

    def __ge__(self, value: Numeric):
        self.minimum = value
        return self

    def __gt__(self, value: Numeric):
        self.exclusive_minimum = value
        return self

    def __le__(self, value: Numeric):
        self.maximum = value
        return self

    def __lt__(self, value: Numeric):
        self.exclusive_maximum = value
        return self

    def __rlshift__(self, value: Numeric):
        self.minimum = value
        return self

    def to_dict(self):
        result = {
            "type": self.type,
            "description": self.description,
            "enum": self.enum,
            "required": self.required,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "exclusiveMinimum": self.exclusive_minimum,
            "exclusiveMaximum": self.exclusive_maximum,
            "maxLength": self.max_length,
            "minLength": self.min_length,
            "pattern": self.pattern,
        }
        return {k: v for k, v in result.items() if v is not None}


F = FieldInfo()
