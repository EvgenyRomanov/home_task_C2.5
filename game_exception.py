class BoardOutException(Exception):
    """Выход точки за пределы поля."""
    pass


class ShipPositionException(Exception):
    """Когда неправильно располагаем корабль на доске."""
    pass


class RetryException(Exception):
    """При попытке выстрелить в использованную точку."""
    pass

