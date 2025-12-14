import requests
from requests import session
import constans
from constans import BASE_URL,headers,json
import conftest


class TestBookings():
    BASE_URL = constans.BASE_URL
    headers = constans.headers
    json = constans.json


    def get_token(self):
        response  = requests.post(f"{self.BASE_URL}/auth", headers= self.headers,json= self.json)
        if response.status_code == 200:
            token = response.json().get("token")
            assert token is not None , "В ответе нет токена"
            return  token
        else :
           return response.status_code, "ошибка авторизации"

    def create_booking(self):
        session = requests.Session()
        session.headers.update(self.headers)

        token = self.get_token()
        session.headers.update({"Cookie": f"token={token}"})

        booking_data = {
            "firstname": "Ryan",
            "lastname": "Gosling",
            "totalprice": 150000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Piano"
        }

        create_booking = session.post(f"{self.BASE_URL}/booking",json = booking_data,
        headers={"Content-Type" : 'application/json'})
        assert create_booking.status_code == 200 , "ошибка создания бука"
        book_id = create_booking.json().get("bookingid")
        assert book_id is not None

        get_booking = session.get(f"{self.BASE_URL}/booking/{book_id}")

        assert  get_booking.status_code == 200, "бронь не найдена"
        assert  get_booking.json().get("firstname") == booking_data["firstname"]


        delete_booking = session.delete(f"{self.BASE_URL}/booking/{book_id}")

        assert  delete_booking.status_code == 201, "ошибка при удалении брони"

        get_booking = session.get(f"{self.BASE_URL}/booking/{book_id}")

        assert get_booking.status_code == 404 , "Бронь не удалилась"

        return "все четко)"


booking = TestBookings()

print(booking.get_token())
print(booking.create_booking())