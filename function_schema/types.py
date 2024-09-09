from typing import TypedDict, Optional


class ParamSchema(TypedDict):
    """
    Represents the schema for a parameter.
    Attributes:
        type (str): The type of the parameter.
        description (str): The description of the parameter.
        enum (Optional[list[str]]): The list of allowed values for the parameter (optional).
        default (Optional[str]): The default value for the parameter (optional).
    """
    type: str
    description: str
    enum: Optional[list[str]]
    default: Optional[str]


class FunctionSchema(TypedDict):
    """
    Represents the schema of a function.
    Attributes:
        name (str): The name of the function.
        description (str): The description of the function.
        input_schema (ParamSchema): The schema for the input parameters of the function.
    """
    name: str
    description: str
    input_schema: ParamSchema
