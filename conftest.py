import pytest
import requests
from urls import Urls
from helpers import register_new_user_and_return_login_password, delete_user

@pytest.fixture
def create_user():
    user_data = register_new_user_and_return_login_password()
    yield user_data
    delete_user(user_data["email"], user_data["password"])


@pytest.fixture
def auth_token(create_user): # Фикстура для получения токена
    user_data = create_user
    response = requests.post(
        Urls().LOGIN_USER,
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert response.status_code == 200, f"Ошибка при авторизации: {response.status_code}"
    return response.json()["accessToken"]

@pytest.fixture
def valid_ingredients():
    response = requests.get(Urls().INGREDIENTS_ORDERS)
    assert response.ok, f"Ошибка при получении ингредиентов: {response.status_code}"
    ingredients = response.json().get("data", [])
    assert len(ingredients) >= 2, "Недостаточно ингредиентов для теста"
    return [ingredients[0]["_id"], ingredients[1]["_id"]]