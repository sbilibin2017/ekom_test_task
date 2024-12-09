from typing import Any

from pydantic import Field, RootModel


class FormRequest(RootModel):
    root: dict[str, Any] = Field(
        title="Form",
        description="Form data dictionary with fields and values",
        alias="request",
    )


class FormFieldTypesResponse(RootModel):
    root: dict[str, Any] = Field(
        title="Form field types",
        description="Form field types only",
    )


class FormTemplateResponse(RootModel):
    root: str = Field(
        title="Form template name",
        description="Form template name",
    )
