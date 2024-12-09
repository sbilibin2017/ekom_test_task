from http import HTTPStatus

from httpx import Client
from pymongo import MongoClient

from app.core.settings import Settings, settings

FORM_TEMPLATE_DATA = [
    {
        "name": "UserRegistration",
        "email": "email",
        "phone_number": "phone",
        "signup_date": "date",
    },
    {
        "name": "OrderForm",
        "customer_email": "email",
        "order_phone": "phone",
        "order_date": "date",
        "address": "text",
    },
]


FORM_TEST_DATA = [
    {
        "request": {
            "email": "user@example.com",
        },
        "actual_response": "UserRegistration",
        "actual_status_code": HTTPStatus.OK,
        "expected_response": "UserRegistration",
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {
            "phone_number": "+7 111 222 33 44",
        },
        "actual_response": "UserRegistration",
        "actual_status_code": HTTPStatus.OK,
        "expected_response": "UserRegistration",
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {
            "signup_date": "01-02-2000",
        },
        "actual_response": "UserRegistration",
        "actual_status_code": HTTPStatus.OK,
        "expected_response": "UserRegistration",
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {
            "signup_date": "2000-01-02",
        },
        "actual_response": "UserRegistration",
        "actual_status_code": HTTPStatus.OK,
        "expected_response": "UserRegistration",
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {
            "signup_date": "01/02/2000",
        },
        "actual_response": "UserRegistration",
        "actual_status_code": HTTPStatus.OK,
        "expected_response": "UserRegistration",
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {
            "signup_date": "41/02/2000",
        },
        "actual_response": "UserRegistration",
        "actual_status_code": HTTPStatus.OK,
        "expected_response": "UserRegistration",
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {
            "signup_date": "141022000",
        },
        "actual_response": {"signup_date": "phone"},
        "actual_status_code": HTTPStatus.OK,
        "expected_response": {"signup_date": "phone"},
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {
            "email": "user@example.com",
            "phone_number": "+7 111 222 33 44",
            "signup_date": "09.12.2024",
        },
        "actual_response": "UserRegistration",
        "actual_status_code": HTTPStatus.OK,
        "expected_response": "UserRegistration",
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {
            "address": "Some Street, 123",
        },
        "actual_response": "UserRegistrationExtended",
        "actual_status_code": HTTPStatus.OK,
        "expected_response": "UserRegistrationExtended",
        "expected_status_code": HTTPStatus.OK,
    },
    {
        "request": {},
        "actual_response": {"detail": "Form data is empty"},
        "actual_status_code": HTTPStatus.BAD_REQUEST,
        "expected_response": {"detail": "Form data is empty"},
        "expected_status_code": HTTPStatus.BAD_REQUEST,
    },
]


def _prepare_mongo(settings: Settings = settings):
    mongo: MongoClient = MongoClient(
        host="localhost",
        port=settings.MONGO_PORT,
        username=settings.MONGO_INITDB_ROOT_USERNAME,
        password=settings.MONGO_INITDB_ROOT_PASSWORD,
        authSource=settings.MONGO_INITDB_DATABASE,
    )
    db = mongo["ecom_test_task"]
    c = db["form_templates"]
    c.insert_many(
        [
            {
                "name": "UserRegistration",
                "email": "email",
                "phone_number": "phone",
                "signup_date": "date",
            },
            {
                "name": "UserRegistrationExtended",
                "email": "email",
                "phone_number": "phone",
                "signup_date": "date",
                "address": "text",
            },
        ]
    )
    return c


def _make_post_request(
    request_body: dict,
    settings: Settings = settings,
) -> tuple[int, dict]:
    with Client() as client:
        actual_response = client.post(
            url=f"http://localhost:{settings.APP_PORT}/get_form/",
            json=request_body,
        )
    return actual_response.status_code, actual_response.json()


def main():
    c = _prepare_mongo()
    for test_case in FORM_TEST_DATA:
        status_code, actual_response = _make_post_request(
            request_body=test_case["request"],
        )
        assert status_code == test_case["actual_status_code"]
        assert actual_response == test_case["expected_response"]
    c.drop()
    print("All tests finished successfully")


if __name__ == "__main__":
    main()
