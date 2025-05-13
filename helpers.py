import requests
import random
import string
from urls import Urls


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def register_new_user_and_return_login_password():
    urls = Urls()
    email = f"test_{generate_random_string(8)}@yandex.ru"
    password = generate_random_string(10)
    name = f"User_{generate_random_string(6)}"

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(
        urls.REGISTRATION_USER,
        json=payload
    )

    # Возвращаем словарь с нужными данными
    return {
        "status_code": response.status_code,
        "email": email,
        "password": password,
        "name": name,
        "response_data": response.json() if response.content else None
    }


def delete_user(email, password):
    urls = Urls()

    # Сначала авторизуемся, чтобы получить токен
    login_response = requests.post(
        urls.LOGIN_USER,
        json={"email": email, "password": password}
    )

    if login_response.status_code == 200:
        # Удаляем пользователя
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token}
        requests.delete(urls.DELETE_USER, headers=headers)
