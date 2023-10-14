import pytest
import requests
import json
from config import baseurl
from faker import Faker

fake = Faker()


@pytest.fixture(scope='module')
def add_pet():
    url = f"{baseurl}/pet"

    payload = json.dumps({
        "name": fake.name(),
        "photoUrls": [],
        "id": 5,
        "category": {
            "id": 1,
            "name": fake.name()
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
    assert not response.status_code != 200
    get_id = response.json().get('id')
    return get_id


@pytest.fixture(scope='module')
def pet_id(add_pet):
    return add_pet
