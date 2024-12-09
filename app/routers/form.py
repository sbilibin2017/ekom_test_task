from fastapi import APIRouter, Depends

from app.schemas.form import FormFieldTypesResponse, FormRequest, FormTemplateResponse
from app.services.form_template import FormTemplateService, get_form_template_service

router = APIRouter(
    tags=["Form"],
)


@router.post(
    path="/get_form/",
    response_model=FormTemplateResponse | FormFieldTypesResponse,
)
async def get_form(
    form_data_request: FormRequest, form_template_service: FormTemplateService = Depends(get_form_template_service)
):
    return await form_template_service.get_form(
        form_data_request=form_data_request,
    )
