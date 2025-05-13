class Urls:
    BASE = 'https://stellarburgers.nomoreparties.site/api'

    # Регистрация и вход
    REGISTRATION_USER = f"{BASE}/auth/register"
    LOGIN_USER = f"{BASE}/auth/login"

    # Удаление пользователя
    DELETE_USER = f"{BASE}/auth/user"

    # Получение и обновление информации о пользователе
    EDIT_DATA_USER = f"{BASE}/auth/user"

    # Создание заказов
    CREATE_ORDERS = f"{BASE}/orders"

    # Получение заказов конкретного пользователя
    RECEIVING_ORDERS = f"{BASE}/orders"

    INGREDIENTS_ORDERS = f"{BASE}/ingredients"
