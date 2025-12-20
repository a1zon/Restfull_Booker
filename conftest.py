
from  requestor import  CustomRequester
import requests
import constans
from constans import  *
from faker import  Faker
import pytest

faker = Faker()

@pytest.fixture(scope = "session")
def auth_session(requester):
    auth_data = ADMIN

    response = requester.send_request(
        method = "POST",
        endpoint = "/auth",
        data = auth_data,
        expected_status = 200,
    )


    token = response.json().get("token")

    assert token, f"Токен не получен! Ответ: {response.text}"

    requester.session.cookies.set("token", token)

    return requester

@pytest.fixture(scope = "session")
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min = 100, max = 100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture()
def created_booking(auth_session, booking_data):
    """Фикстура создаёт бронь и удаляет после теста
    решил дополнить файл выносом логики создания - так как она отдаелена от сути основных проверок
    в большинстве случаев"""
    requester = auth_session
    response = requester.send_request(
            method = "POST",
            endpoint ='/booking',
            expected_status = 200,
            data= booking_data
        )
    booking_id = response.json()["bookingid"]
    yield booking_id
    # После теста — удаляем
    auth_session.send_request("DELETE", f"/booking/{booking_id}", expected_status = 201)

@pytest.fixture(scope = "session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture
def fresh_update_data():
    """Генерирует новые данные для обновления каждый раз"""
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min = 100, max = 100000),
        "depositpaid": faker.boolean(),
        "bookingdates": {
            "checkin": str(faker.date_between(start_date = "today", end_date = "+30d")),
            "checkout": str(faker.date_between(start_date = "+31d", end_date = "+60d"))
        },
        "additionalneeds": faker.sentence(nb_words = 3)
    }