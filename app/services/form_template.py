from http import HTTPStatus
from typing import Literal

from fastapi import HTTPException

from app.repositories.form_template import FormTemplateRepository, form_template_repository
from app.schemas.form import FormFieldTypesResponse, FormRequest, FormTemplateResponse


class FormTemplateService:
    def __init__(
        self,
        form_template_repository: FormTemplateRepository = form_template_repository,
    ):
        self.form_template_repository = form_template_repository

    async def get_form(
        self,
        form_data_request: FormRequest,
    ) -> FormTemplateResponse | FormFieldTypesResponse:
        form_data: dict = form_data_request.model_dump()
        if not form_data:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Form data is empty",
            )

        best_template_match_count: int = 0
        best_template_name: str = ""

        async for template in self.form_template_repository.generate_form_template():
            if not (template_name := template.get("name")):
                continue

            current_match_count = 0
            for template_key, template_field_type in template.items():
                if (
                    (template_key != "name")
                    and (template_key in form_data)
                    and (template_field_type == self._get_field_actual_type(form_data[template_key]))
                ):
                    current_match_count += 1

            if current_match_count and (current_match_count > best_template_match_count):
                best_template_match_count = current_match_count
                best_template_name = template_name

        if not best_template_name:
            return FormFieldTypesResponse(
                {
                    form_field_name: self._get_field_actual_type(form_field_value)
                    for form_field_name, form_field_value in form_data.items()
                }
            )

        return FormTemplateResponse(best_template_name)

    def _get_field_actual_type(
        self,
        value: str,
    ) -> Literal["email", "phone", "date", "text"]:
        import re

        value = value.replace(" ", "").strip()
        if re.match(
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            string=value,
        ):
            actual_type = "email"
        elif re.match(
            pattern=r"^\+?1?\d{9,15}$",
            string=value,
        ):
            actual_type = "phone"
        elif any(
            re.match(
                pattern=pattern,
                string=value,
            )
            for pattern in (
                "^\\d{4}-\\d{2}-\\d{2}$",
                "^\\d{2}/\\d{2}/\\d{4}$",
                "^\\d{2}-\\d{2}-\\d{4}$",
                "^\\d{4}\\s\\d{2}\\s\\d{2}$",
                "^\\d{2}\\.\\d{2}\\.\\d{4}$",
                "^\\d{2}/\\d{2}/\\d{4}$",
            )
        ):
            actual_type = "date"
        else:
            actual_type = "text"
        return actual_type  # type: ignore


form_template_service: FormTemplateService = FormTemplateService()


def get_form_template_service() -> FormTemplateService:
    return form_template_service
