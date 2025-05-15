import requests
import allure
from urls import Urls


@allure.suite("Получение заказов пользователя")
class TestUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_user_orders_authorized(self, create_user):
        login_response = requests.post(
            Urls().LOGIN_USER,
            json={"email": create_user["email"], "password": create_user["password"]}
        )
        token = login_response.json()["accessToken"]

        orders_response = requests.get(
            Urls().RECEIVING_ORDERS,
            headers={"Authorization": token}
        )

        assert orders_response.status_code == 200
        orders_data = orders_response.json()
        assert orders_data["success"] is True
        assert "orders" in orders_data


    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_user_orders_unauthorized(self):
        orders_response = requests.get(Urls().RECEIVING_ORDERS)

        assert orders_response.status_code == 401
        assert orders_response.json()["success"] is False
        assert "You should be authorised" in orders_response.json().get("message")