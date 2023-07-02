import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..app.database import Base
from ..app.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# @pytest.fixture
# def house_payload():
#     return {
#         "date": "2023-06-30",
#         "price": 1000000.0,
#     }


@pytest.fixture
def house_payload():
    return [
        {
            "date": "2023-06-30",
            "price": 1000000.0,
        },
        {
            "date": "2000-01-01",
            "price": 5000000.0,
        },
    ]


def test_create_house(house_payload):
    house_payload = house_payload[0]
    response = client.post(
        "/houses",
        json=house_payload,
    )
    assert response.status_code == 200
    assert response.json()["date"] == house_payload["date"]
    assert response.json()["price"] == house_payload["price"]


def test_get_houses(house_payload):
    house_payload = house_payload
    client.post(
        "/houses",
        json=house_payload[0],
    )
    client.post(
        "/houses",
        json=house_payload[1],
    )

    response = client.get("/houses")
    response_json = [
        {k: v for k, v in item.items() if k != "id"} for item in response.json()
    ]  # drop id

    assert response.status_code == 200
    assert response_json == house_payload


def test_update_house(house_payload):
    # Create a house to update
    house_payload = house_payload[0]
    response = client.post(
        "/houses",
        json=house_payload,
    )
    assert response.status_code == 200
    house_id = response.json()["id"]

    # Update the house
    updated_house_payload = {
        "date": "2023-07-01",
        "price": 1500000.0,
    }
    response = client.put(
        f"/houses/{house_id}",
        json=updated_house_payload,
    )
    assert response.status_code == 200


def test_delete_house(house_payload):
    # Create a house to delete
    house_payload = house_payload[0]
    response = client.post(
        "/houses",
        json=house_payload,
    )
    assert response.status_code == 200
    house_id = response.json()["id"]

    # Delete the house
    response = client.delete(f"/houses/{house_id}")
    assert response.status_code == 200


#
# def test_index(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"data": "houses list"}
#
#
# def test_get_all_houses(client):
#     response = client.get("/houses")
#     assert response.status_code == 404
#
#
# def test_create_house(client, house_payload):
#     response = client.post(
#         "/houses",
#         json=house_payload,
#     )
#     assert response.status_code == 200
#     assert response.json()["date"] == house_payload["date"]
#     assert response.json()["price"] == house_payload["price"]
#
#
# def test_update_house(client, house_payload):
#     # Create a house to update
#     response = client.post(
#         "/houses",
#         json=house_payload,
#     )
#     assert response.status_code == 200
#     house_id = response.json()["id"]
#
#     # Update the house
#     house_payload["date"] = "2023-07-01"
#     house_payload["price"] = 1500000
#     response = client.put(
#         f"/houses/{house_id}",
#         json=house_payload,
#     )
#     assert response.status_code == 200
#     assert response.text == "Updated successfully"
#
#
# def test_delete_house(client, house_payload):
#     # Create a house to delete
#     response = client.post(
#         "/houses",
#         json=house_payload,
#     )
#     assert response.status_code == 200
#     house_id = response.json()["id"]
#
#     # Delete the house
#     response = client.delete(f"/houses/{house_id}")
#     assert response.status_code == 200
#     assert response.text == "Deleted successfully"
