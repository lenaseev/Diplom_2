import requests
import allure
from urls import Urls


@allure.suite("Изменение данных пользователя")
class TestUserUpdate:

    @allure.title("Изменение email с авторизацией")
    def test_update_email_with_auth(self, create_user, auth_token):
        new_email = f"updated_{create_user['email']}"
        response = requests.patch(
            Urls().EDIT_DATA_USER,
            headers={"Authorization": auth_token},
            json={"email": new_email}
        )

        assert response.status_code == 200
        assert response.json()["user"]["email"] == new_email

    @allure.title("Изменение имени с авторизацией")
    def test_update_name_with_auth(self, create_user, auth_token):
        new_name = f"Updated_{create_user['name']}"
        response = requests.patch(
            Urls().EDIT_DATA_USER,
            headers={"Authorization": auth_token},
            json={"name": new_name}
        )

        assert response.status_code == 200
        assert response.json()["user"]["name"] == new_name

    @allure.title("Изменение пароля с авторизацией")
    def test_update_password_with_auth(self, create_user, auth_token):
        new_password = f"Updated_{create_user['password']}"
        response = requests.patch(
            Urls().EDIT_DATA_USER,
            headers={"Authorization": auth_token},
            json={"password": new_password}
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

        # Дополнительная проверка, что пароль действительно изменился
        login_response = requests.post(
            Urls().LOGIN_USER,
            json={
                "email": create_user["email"],
                "password": new_password
            }
        )
        assert login_response.status_code == 200


    @allure.title("Попытка изменения имени без авторизации")
    def test_update_name_without_auth(self):
        response = requests.patch(
            Urls().EDIT_DATA_USER,
            json={"name": "UnauthorizedUser"}
        )

        assert response.status_code == 401
        assert "You should be authorised" in response.json().get("message")

    @allure.title("Попытка изменения email без авторизации")
    def test_update_email_without_auth(self):
        response = requests.patch(
            Urls().EDIT_DATA_USER,
            json={"email": "unauth@yandex.ru"}
        )

        assert response.status_code == 401
        assert "You should be authorised" in response.json().get("message")

    @allure.title("Попытка изменения пароля без авторизации")
    def test_update_password_without_auth(self):
        response = requests.patch(
            Urls().EDIT_DATA_USER,
            json={"password": "unauthpassword"}
        )

        assert response.status_code == 401
        assert "You should be authorised" in response.json().get("message")