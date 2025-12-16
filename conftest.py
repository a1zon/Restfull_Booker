

import requests
import constans
from constans import  BASE_URL, headers, json
from faker import  Faker
import pytest

faker = Faker()

@pytest.fixture(scope = "session")
def auth_session():
    session = requests.Session()
    session.headers.update(constans.headers)

    response  = requests.post(f"{BASE_URL}/auth", headers= headers,json= json)
    assert  response.status_code == 200 , "ошибка авторизации"
    token = response.json().get('token')
    session.headers.update({"Cookie" : f"token={token}"})
    return session

@pytest.fixture(scope="session")
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
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
    response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    booking_id = response.json()["bookingid"]
    yield booking_id
    # После теста — удаляем
    auth_session.delete(f"{BASE_URL}/booking/{booking_id}")