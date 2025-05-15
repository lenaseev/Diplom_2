import requests
import allure
from urls import Urls


@allure.suite("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Успешный логин")
    def test_successful_login(self, create_user):
        login_data = {
            "email": create_user["email"],
            "password": create_user["password"]
        }

        response = requests.post(Urls().LOGIN_USER, json=login_data)

        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.title("Логин с неверным email")
    def test_login_with_wrong_email(self, create_user):
        response = requests.post(
            Urls().LOGIN_USER,
            json={"email": "123_" + create_user["email"],
                  "password": create_user["password"]}
        )

        assert response.status_code == 401
        assert "email or password are incorrect" in response.json().get("message")

    @allure.title("Логин с неверным паролем")
    def test_login_with_wrong_password(self, create_user):
        response = requests.post(
            Urls().LOGIN_USER,
            json={"email": create_user["email"], "password": "wrong_" + create_user["password"]}
        )

        assert response.status_code == 401
        assert "email or password are incorrect" in response.json().get("message")