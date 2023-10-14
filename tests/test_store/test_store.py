import requests
import json
import pytest
from config import baseurl
from datetime import datetime
from faker import Faker
fake = Faker()

def get_datetime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return formatted_datetime

class Test_store:
    @pytest.fixture(autouse=True)
    def test_place_order(self, pet_id):
        url = f"{baseurl}/store/order"
        ship_data = get_datetime()
        payload = json.dumps({
            "petId": f"{pet_id}",
            "quantity": 5,
            "shipDate": f"{ship_data}",
            "status": "delivered",
            "complete": True
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        assert response.status_code == 200, f"Assertion error: f'{response.json()}'"
        order_id = response.json().get('id')
        self.order_id = order_id
        return order_id

    def test_get_order(self):
        url = f"{baseurl}/store/order/{self.order_id}"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        assert response.status_code == 200, f"Assertion error: f'{response.json()}'"
        print(response.json())

    def test_delete_order(self):
        url = f"{baseurl}/store/order/{self.order_id}"
        response = requests.request("DELETE", url)

        print(response.json())


class Test_store_invalid:
    def test_place_order_500(self):
        url = f"{baseurl}/store/order"
        payload = json.dumps({
            "petId": 1,
            "quantity": 5,
            "shipDate": f'{datetime.now()}',
            "status": "delivered",
            "complete": True
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        assert response.status_code == 500, response.json()

    def test_get_order_404(self):
        url = f"{baseurl}/store/order/0"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        assert response.status_code == 404
        print(response.json())

    def test_delete_order_404(self):
        url = f"{baseurl}/store/order/0"
        response = requests.request("DELETE", url)
        assert response.status_code == 404
        assert response.json().get('message') == 'Order Not Found'
        print(response.text)

    def test_delete_order_format_exc(self):
        invalid_data = fake.name()
        url = f"{baseurl}/store/order/{invalid_data}"
        response = requests.request("DELETE", url)
        assert response.status_code == 404
        assert response.json().get('message') == f'java.lang.NumberFormatException: For input string: "{invalid_data}"'
