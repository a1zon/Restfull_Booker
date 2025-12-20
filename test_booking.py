from constans import  BASE_URL
import  pytest
import  requests

class TestBook:

    def test_update_booking(self,auth_session,fresh_update_data,created_booking):
        booking_id = created_booking
        update_data = fresh_update_data

        response = auth_session.send_request(
            method= "PUT",
            endpoint= f"/booking/{booking_id}",
            data= update_data,
            expected_status= 200
        )
        assert response.status_code == 200, "ошибка при обновлении данных"

        get_response = auth_session.send_request(
            method= "GET",
            endpoint= f"/booking/{booking_id}",
            expected_status= 200
        )
        updated_booking = get_response.json()

        # проверка обязательных полей (хз надо ли в каждом тесте)
        for key in ["firstname", "lastname", "totalprice", "additionalneeds"]:
            assert updated_booking[key] == update_data[key]

        assert updated_booking["bookingdates"]["checkin"] == update_data["bookingdates"]["checkin"]
        assert updated_booking["bookingdates"]["checkout"] == update_data["bookingdates"]["checkout"]

    def test_partial_update_booking(self,auth_session,booking_data,created_booking):

        booking_id = created_booking

        updated_data = booking_data.copy()
        updated_data.update({"firstname": "James", "lastname": "Brown"})

        response = auth_session.send_request(
            method= "PATCH",
            endpoint=f"/booking/{booking_id}",
            expected_status= 200,
            data= updated_data
        )

        assert  response.status_code == 200 , "Ошибка при частичном обновлении данных"

        get_response = auth_session.send_request(
            method= "GET",
            endpoint= f"/booking/{booking_id}",
            expected_status= 200
        )
        updated_booking = get_response.json()

        for key in ["firstname", "lastname", "totalprice", "additionalneeds"]:
            assert updated_booking[key] == updated_data[key]

        assert updated_booking["bookingdates"]["checkin"] == updated_data["bookingdates"]["checkin"]
        assert updated_booking["bookingdates"]["checkout"] == updated_data["bookingdates"]["checkout"]


class TestNegativeScenarios:
    """Отдельный класс для негативных тестов"""

    @pytest.mark.parametrize("invalid_data, expected_status", [
        ({}, 500),  # пустой объект
        ({"firstname": "OnlyName"}, 500),
        ({"totalprice": "not_a_number"}, 500),
    ])
    def test_create_booking_invalid_data(self, auth_session, invalid_data, expected_status):

        response = auth_session.send_request(
            method="POST",
            endpoint="/booking",
            data= invalid_data,
            expected_status = 500
        )
        assert response.status_code == expected_status

    def test_update_nonexistent_booking(self, auth_session):

        response = auth_session.send_request(
            method = "PUT",
            endpoint ="/booking/999999999999",
            data = {"firstname": "Test"},
            expected_status= 400
        )
        assert response.status_code == 400

    def test_delete_without_auth(self):

        session = requests.Session()  # типа без токена гуляем
        response = session.delete(f"{BASE_URL}/booking/1")
        assert response.status_code in [403, 401]
