

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

# @pytest.fixture(scope="session")
# def get_id():
#