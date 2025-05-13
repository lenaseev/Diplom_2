import requests
import allure
from helpers import register_new_user_and_return_login_password
from urls import Urls


@allure.suite("Регистрация пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    def test_create_user(self):
        result = register_new_user_and_return_login_password()

        assert result["status_code"] == 200, (
            f"Ожидался статус 200, получен {result['status_code']}. "
            f"Ответ сервера: {result['response_data']}"
        )

    @allure.title("Создание двух одинаковых пользователей")
    def test_create_two_identical_users(self):
        first_user = register_new_user_and_return_login_password()

        payload = {
            "email": first_user["email"],
            "password": first_user["password"],
            "name": first_user["name"]
        }

        response = requests.post(Urls().REGISTRATION_USER, json=payload)

        assert response.status_code == 403
        assert "User already exists" in response.json().get("message")

    @allure.title("Регистрация без email")
    def test_register_without_email(self):
        response = requests.post(
            Urls().REGISTRATION_USER,
            json={"password": "testpassword",
                  "name": "User"}
        )

        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.json().get("message")

    @allure.title("Регистрация без пароля")
    def test_register_without_password(self):
        response = requests.post(
            Urls().REGISTRATION_USER,
            json={"email": "test@yandex.ru",
                  "name": "User"}
        )

        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.json().get("message")

    @allure.title("Регистрация без имени")
    def test_register_without_name(self):
        response = requests.post(
            Urls().REGISTRATION_USER,
            json={"email": "test@yandex.ru",
                  "password": "testpassword"}
        )

        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.json().get("message")