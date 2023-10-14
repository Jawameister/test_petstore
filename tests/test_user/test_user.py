import requests
import json
import pytest
import random
from config import baseurl
from datetime import datetime
from faker import Faker
fake = Faker()

username = fake.word()
expected_user_data = {
          "id": None,
          "username": f"{username}",
          "firstName": f"{fake.first_name()}",
          "lastName": f"{fake.last_name()}",
          "email": f"{fake.email()}",
          "password": f"{fake.word()}",
          "phone": f"{fake.phone_number()}",
          "userStatus": 1
        }
class Test_user:
    @pytest.fixture(autouse=True)
    def test_add_user(self):
        url = f"{baseurl}/user"
        payload = json.dumps(expected_user_data)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        assert response.status_code == 200, f"Assertion error: f'{response.json()}'"


    def test_get_user(self):
        url = f"{baseurl}/user/{username}"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        for key, value in list(expected_user_data.items())[1:]: # мы преобразовали dict в list, и пропустили первое ключ значение, как как в body создания юзера мы передает id,
            # но он не учитывается, и в ответе передается автоматически созданный id
            assert response.json().get(key) == value, f"Key '{key}' has unexpected value"
        print(response.text)

    def test_delete_user(self):
        url = f"https://petstore.swagger.io/v2/user/{username}"

        response = requests.request("DELETE", url)
        assert response.status_code == 200, f"Assertion error: f'{response.json()}'"



class Test_user_invalid:
    def test_add_user_0(self):
        url = f"{baseurl}/user"

        payload = json.dumps({
            "sdf": 12
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        assert response.json().get('message') == '0', f"Assertion error: '{response.json()}'"

    def test_add_user_400(self):
        url = f"{baseurl}/user"

        payload = "{sad}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        assert response.status_code == 400, f"Assertion error: '{response.json()}'"
        assert response.json().get('message') == "bad input", f"Assertion error: '{response.json()}'"


    def test_get_user_404(self):
        url = f"{baseurl}/user/5"

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        assert response.json().get('message') == "User not found", f"Assertion error: '{response.json()}'"
        assert response.status_code == 404

    def test_user_delete_404(self):
        url = f"{baseurl}/user/5"
        response = requests.request("DELETE", url)
        assert response.status_code == 404