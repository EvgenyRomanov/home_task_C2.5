from game_exception import *


class Dot:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __setattr__(self, key, value):
        """
        Переопределяем метод: проверяем корректность переданных
        значений в конструктор.
        Если передаем не целое число - выбрасываем исключение.
        """

        if (key == "_Dot__x" or key == "_Dot__y") and type(value) != int:
            raise AttributeError
        else:
            super().__setattr__(key, value)


class Ship:
    """
    Направление корабля будет "hor" или "ver".
    Отрисовка слева-направо и сверху-вниз относительно носа (dot_bow).
    len_ship - длина корабля.
    dot_bow - координата носа корабля.
    direction - направление ("hor" или "ver").
    volume - кол-во жизней, изначально равно длине корабля.
    """

    def __init__(self, len_ship: int, dot_bow: Dot, direction: str):
        self.__len_ship = len_ship
        self.__dot_bow = dot_bow
        self.__direction = direction
        self.__volume = len_ship

    def dots(self):
        """
        Список всех точек корабля.
        """

        if self.__direction == "ver":
            return [Dot(self.__dot_bow.x + i, self.__dot_bow.y) for i in range(0, self.__len_ship)]
        elif self.__direction == "hor":
            return [Dot(self.__dot_bow.x, self.__dot_bow.y + j) for j in range(0, self.__len_ship)]
        else:
            pass

    @property
    def len_ship(self):
        return self.__len_ship

    @property
    def dot_bow(self):
        return self.__dot_bow

    @property
    def direction(self):
        return self.__direction

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, new_volume):
        self.__volume = new_volume

    def __setattr__(self, key, value):
        """
        Переопределяем метод: проверяем корректность переданных
        значений (длина и тип корабля) в конструктор.
        """

        if key == "_Ship__len_ship" and (not (1 <= value <= 3) or type(value) != int):
            raise AttributeError
        elif key == "_Ship__direction" and value not in ["hor", "ver"]:
            raise AttributeError
        else:
            super().__setattr__(key, value)


class Board:
    def __init__(self, hid=True):
        """
        __board_list - двумерный список, в котором хранятся состояния каждой из клеток.
        __list_ship - список кораблей доски.
        __hid - информация о том, нужно ли скрывать корабли на доске.
        __number_living_ships - количество живых кораблей на доске.
        """

        self.__board_list = [["o" for i in range(6)] for j in range(6)]
        self.__list_ship = []
        self.__hid = hid
        self.__number_living_ships = 0

    @property
    def number_living_ships(self):
        return self.__number_living_ships

    @property
    def list_ship(self):
        return self.__list_ship

    def __chek_position_ship(self, ship: Ship):
        # Выходит ли за границы доски?
        for dot in ship.dots():
            if self.__out(dot):
                raise BoardOutException

        # Расстояние между кораблями >=1 клетки?
        for ship_on_board in self.__list_ship:
            for dot in ship.dots():
                if dot in self.__contour(ship_on_board):
                    raise ShipPositionException

        return True

    def add_ship(self, ship: Ship):
        """
        Ставит корабль на доску (если ставить не получается, выбрасываем исключения).
        """

        if self.__chek_position_ship(ship):
            # Пополняем список кораблей доски
            self.__list_ship.append(ship)
            # и кол-во живых кораблей.
            self.__number_living_ships += 1

            for dot in ship.dots():
                # Меняем состояние клеток доски в соответствии точками корабля.
                self.__board_list[dot.x-1][dot.y-1] = "K"

    def __contour(self, ship: Ship):
        """
        Обводит корабль по контуру:
        помечает соседние точки, где корабля по правилам быть не может).
        """

        # Идея вернуть список точек корабля и вокруг корабля,
        # даже которые за границами доски, чтобы проще было.
        dot_in_comtour = []
        dot_in_comtour.extend(ship.dots())

        x = ship.dot_bow.x
        y = ship.dot_bow.y
        len_ship = ship.len_ship

        if ship.direction == "ver":
            # Зона слева от корабля.
            dot_in_comtour.extend([Dot(x+i, y-1) for i in range(0, len_ship)])
            # Зона справа от корабля.
            dot_in_comtour.extend([Dot(x+i, y+1) for i in range(0, len_ship)])
            # Зона над кораблем.
            dot_in_comtour.extend([Dot(x-1, y), Dot(x-1, y-1), Dot(x-1, y+1)])
            # Зона под кораблем.
            dot_in_comtour.extend([Dot(x+len_ship, y), Dot(x+len_ship, y-1), Dot(x+len_ship, y+1)])
        elif ship.direction == "hor":
            # Зона под кораблем.
            dot_in_comtour.extend([Dot(x+1, y+i) for i in range(0, len_ship)])
            # Зона над кораблем.
            dot_in_comtour.extend([Dot(x-1, y+i) for i in range(0, len_ship)])
            # Зона слева от корабля.
            dot_in_comtour.extend([Dot(x, y-1), Dot(x-1, y-1), Dot(x+1, y-1)])
            # Зона справа от корабля.
            dot_in_comtour.extend([Dot(x, y+len_ship), Dot(x+1, y+len_ship), Dot(x-1, y+len_ship)])

        return dot_in_comtour

    def print_board(self):
        """Выводит доску в консоль в зависимости от параметра hid."""

        string = '{:^2}' * 7
        print(string.format('', *range(1, 7)))

        for num_row, cell in enumerate(self.__board_list):
            if not self.__hid:
                print(string.format(num_row + 1, *cell))
            else:
                cell = "".join(cell).replace("K", "o")
                print(string.format(num_row + 1, *cell))

    def __out(self, dot: Dot):
        """
        Для точки (объекта класса Dot) возвращает True,
        если точка выходит за пределы поля, и False, если не выходит.
        """

        if 1<=dot.x<=6 and 1<=dot.y<=6:
            return False

        return True

    def shot(self, dot: Dot):
        """
        Делает выстрел по доске
        (если есть попытка выстрелить за пределы и в использованную точку,
        нужно выбрасывать исключения).
        """

        # За пределы.
        if self.__out(dot):
            raise BoardOutException

        # В использованную точку.
        if self.__board_list[dot.x-1][dot.y-1] in ["X", "T"]:
            raise RetryException

        flag = False

        for ship in self.__list_ship:
            for dot_ship in ship.dots():
                if dot == dot_ship:
                    flag = True
                    ship.volume -= 1
                    if ship.volume == 0:
                        self.__number_living_ships -= 1
                    break
        if flag:
            self.__board_list[dot.x-1][dot.y-1] = "X"
            print("Попадание!")
            # Вернем True, если попали.
            return True
        else:
            self.__board_list[dot.x-1][dot.y-1] = "T"
            print("Промах!")
