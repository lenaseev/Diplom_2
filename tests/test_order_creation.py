import requests
from urls import Urls
import allure

@allure.suite("Создание заказов")
class TestOrderCreation:

    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_authorized(self, create_user, valid_ingredients, auth_token):
        order_response = requests.post(
            Urls().CREATE_ORDERS,
            headers={"Authorization": auth_token},
            json={"ingredients": valid_ingredients}
        )

        assert order_response.status_code == 200
        order_data = order_response.json()
        assert order_data["success"] is True
        assert "order" in order_data
        assert "number" in order_data["order"]

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_unauthorized(self, valid_ingredients):
        order_response = requests.post(
            Urls().CREATE_ORDERS,
            json={"ingredients": valid_ingredients}
        )

        assert order_response.status_code == 401
        assert order_response.json()["success"] is False

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, create_user, auth_token):
        order_response = requests.post(
            Urls().CREATE_ORDERS,
            headers={"Authorization": auth_token},
            json={"ingredients": []}
        )

        assert order_response.status_code == 400
        assert "must be provided" in order_response.json().get("message")

    @allure.title("Создание заказа с неверными ингредиентами")
    def test_create_order_invalid_ingredients(self, create_user, auth_token):
        order_response = requests.post(
            Urls().CREATE_ORDERS,
            headers={"Authorization": auth_token},
            json={"ingredients": ["invalid_hash1", "invalid_hash2"]}
        )

        assert order_response.status_code == 500
        assert "Internal Server Error" in order_response.text