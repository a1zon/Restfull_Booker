import  pytest
from pygments.util import get_bool_opt
import copy
from constans import  BASE_URL

class TestBook:

    def test_create_booking(self,auth_session,booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking",json= booking_data)
        assert create_booking.status_code == 200 , "ошибка при бронировании"


    def test_update_booking(self,auth_session,booking_data):

        booking_update_data = {
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

        create_booking = auth_session.post(f"{BASE_URL}/booking",json= booking_data)
        assert create_booking.status_code == 200 , "ошибка при бронировании"
        booking_id = create_booking.json().get("bookingid")
        update_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_update_data)
        assert  update_booking.status_code == 200, "ошибка при обновлении данных"
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert  get_booking.json() == booking_update_data

    def test_PartialUpdateBooking(self,auth_session,booking_data):

        booking_data.update({"firstname" : "James","lastname": "Brown"} )


        create_booking = auth_session.post(f"{BASE_URL}/booking",json= booking_data)
        assert create_booking.status_code == 200 , "ошибка при бронировании"
        booking_id = create_booking.json().get("bookingid")
        part_update_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=booking_data)

        assert part_update_booking.status_code == 200, "ошибка при частичном изменении данных"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json().get("firstname") == "James"
        assert get_booking.json().get("lastname") == "Brown"
        assert get_booking.json() == booking_data


    def test_negative(self,auth_session,booking_data):

        booking_data_negative = copy.deepcopy(booking_data)
        booking_data_negative.clear()
        create_booking_negative = auth_session.post(f"{BASE_URL}/booking",json= booking_data_negative)
        assert create_booking_negative.status_code == 500


        get_booking_negative = auth_session.get(f"{BASE_URL}/booking/823957453846719280")
        assert  get_booking_negative.status_code == 404

        booking_data_negative = copy.deepcopy(booking_data)
        booking_data_negative.clear()
        create_booking = auth_session.post(f"{BASE_URL}/booking",json= booking_data)
        booking_id = create_booking.json().get("booking_id")
        create_booking_negative = auth_session.patch(f"{BASE_URL}/booking/{booking_id}",json= booking_data_negative)
        assert create_booking_negative.status_code == 405 # странно что отдает именно 405 )

        booking_data_negative = copy.deepcopy(booking_data)
        booking_data_negative.clear()
        create_booking = auth_session.post(f"{BASE_URL}/booking",json= booking_data)
        booking_id = create_booking.json().get("booking_id")
        create_booking_negative = auth_session.put(f"{BASE_URL}/booking/{booking_id}",json= booking_data_negative)
        assert create_booking_negative.status_code == 400 # странно что отдает именно 405 )



