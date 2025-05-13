import pytest
import requests
from urls import Urls
from helpers import register_new_user_and_return_login_password  # Если используете helpers.py

@pytest.fixture
def create_user():
    user_data = register_new_user_and_return_login_password()  # Используем функцию из helpers.py
    assert user_data["status_code"] == 200, f"Ошибка при регистрации пользователя: {user_data['status_code']}"
    return user_data


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