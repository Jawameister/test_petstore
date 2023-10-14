import requests
import json

from config import baseurl

from faker import Faker
fake = Faker()


class Test_pets:
  def test_get_pet(self, pet_id):
    url = f"{baseurl}/pet/{pet_id}"
    payload = {}
    headers = {
      'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 200, f"Assertion error: f'{response.json()}'"
    print(response.json())

  def test_delete_pet(self, pet_id):
    url = f"{baseurl}/pet/{pet_id}"
    payload = {}
    headers = {}
    response = requests.request("DELETE", url, headers=headers, data=payload)
    assert response.status_code == 200, f"Assertion error: f'{response.json()}'"


class Test_pets_negative:
  def test_add_pet_invalid(self):
    url = f"{baseurl}/pet"
    payload = json.dumps({

      "name": None,
      "category": {
        "id": 1,
        "name": None,
      },
      "tags": [
        {
          "id": 1,
          "name": "<string>"
        }
      ],
      "status": "available"
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    assert not response.status_code != 200, f"Assertion error: f'{response.json()}'"



  def test_get_pet_404(self):

    url = f"{baseurl}/pet/0"

    payload = {}
    headers = {
      'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    assert response.status_code == 404, f"Assertion error: f'{response.json()}'"
    print(response.json())

  def test_delete_pet_404(self):
    url = f"{baseurl}/pet/0"
    response = requests.request("DELETE", url)
    assert response.status_code == 404

  def test_delete_valiation_err(self):
    invalid_data = fake.name()
    url = f"{baseurl}/pet/{invalid_data}"
    response = requests.request("DELETE", url)
    assert response.status_code == 404
    assert response.json().get('message') == f'java.lang.NumberFormatException: For input string: "{invalid_data}"'
