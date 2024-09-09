from typing import (TypedDict, Literal, TypeVar, Union, NotRequired, Generic)


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
    enum: NotRequired[list[str]]
    default: NotRequired[str]


class RootProperty(TypedDict):
    """
    Represents the schema for a parameter.
    Attributes:
        type (str): Root property can only be "object".
        properties (dict[str, ParamSchema]): The properties of the object.
    """
    type: Literal["object"]
    properties: dict[str, ParamSchema]


T = TypeVar('T', bound=Union['WithParameters', 'WithInputSchema'])


class WithParameters(TypedDict):
    parameters: RootProperty


class WithInputSchema(TypedDict):
    input_schema: RootProperty


class FunctionSchemaBase(TypedDict):
    name: str
    description: str


class FunctionSchema(FunctionSchemaBase, Generic[T]):
    """
    Represents the schema of a function.
    Attributes:
        name (str): The name of the function.
        description (str): The description of the function.
        parameters (RootProperty): The schema for the function parameters.
        input_schema (ParamSchema): The schema for the function parameters if format is "claude".
    """
    pass


OpenAIFunctionSchema = FunctionSchema[WithParameters]
ClaudeFunctionSchema = FunctionSchema[WithInputSchema]
