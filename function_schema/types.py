from typing import TypedDict, Literal

try:
    from typing import NotRequired
except ImportError:
    try:
        from typing_extensions import NotRequired
    except ImportError:
        from typing import Optional as NotRequired

try:
    from typing import Doc
except ImportError:
    try:
        from typing_extensions import Doc
    except ImportError:

        class Doc:
            def __init__(self, documentation: str, /):
                self.documentation = documentation


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


class FunctionSchema(TypedDict):
    """
    Represents the schema of a function.
    Attributes:
        name (str): The name of the function.
        description (str): The description of the function.
        parameters (RootProperty): The schema for the function parameters.
        input_schema (ParamSchema): The schema for the function parameters if format is "claude".
    """

    name: str
    description: str
    parameters: NotRequired[RootProperty]
    input_schema: NotRequired[RootProperty]
