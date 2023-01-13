from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел за пределами сетки"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Уже стреляли в эту цель"


class BoardWrongShipException(BoardException):
    pass


# параметры корабля
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    # проверка попадания в корабль
    def shooten(self, shot):
        return shot in self.dots


# игровое поле
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]  # содержит сетку

        self.busy = []  # занятые точки кораблем или точки после выстрела
        self.ships = []  # список кораблей на доске

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]  # все точки около выстрела
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)  # сдвигаем исх точку на dx dy, пройдем все точки которые содествуют с кораблем
                if not (self.out(cur)) and cur not in self.busy:  # если точка не выходит и не занята еще
                    if verb:
                        self.field[cur.x][cur.y] = "."  # ставим на месте выстрела точку
                    self.busy.append(cur)  # добавляем в список занятых точек

    # вывод корабля на доску
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"  # сетка
        # нужно ли скрывать корабли доски
        if self.hid:
            res = res.replace("■", "O")
        return res

    # проверка находится ли точка за пределами доски
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))  # координаты лежат в диапазоне или не лежат

    # стрельба по доске
    def shot(self, d):
        if self.out(d):  # выходит ди выстрел за границы
            raise BoardOutException()

        if d in self.busy:  # проверка занята ли точка
            raise BoardUsedException()

        self.busy.append(d)  # делаем ее занятой если таково не было

        # проверка принадлежности точки к какаму-либо кораблю
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1  # если было попадание, то уменьшаем кол-во жизней
                self.field[d.x][d.y] = "X"  # ставим в эту точку X, что корабль поражен
                if ship.lives == 0:  # если у корабля кончились жизни
                    self.count += 1  # то прибавляем к счетку убытых кораблей 1
                    self.contour(ship, verb=True)  # обводим его контуром
                    print("Корабль потоплен")
                    return False  # дальше ход не нужно делать
                else:
                    print("Корабль подбит")  # если кол-во жизней не 0, то вывод сообщения
                    return True  # дальше нам нужно повторить ход

        self.field[d.x][d.y] = "."  # если не было попадания, мы ставим точку в месте выстрела
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []  # обнуления


# класс игрока
class Player:
    def __init__(self, board, enemy):  # две доски
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):  # пытаемся сделать выстрел
        while True:
            try:
                target = self.ask()  # спршиваем координаты выстела
                repeat = self.enemy.shot(target)  # выполняем выстрел
                return repeat  # если попали в корбль, то повторяем ход
            except BoardException as e:  # если мимо то печатается и
                print(e)


# игрок и ИИ
class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))  # случайно генерируем 2 точки
        print(f"Ход ИИ: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()  # запрос координат

            if len(cords) != 2:  # проверка двух координат
                print(" Введите 2 координаты: ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):  # проверка что это числа
                print(" Введите Числа: ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)  # вычитаем 1 так как индексация с 0


# игра и генерация досок
class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()  # генерируем доску
        co = self.random_board()  # генерируем 2 доску
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):  # создаем доску
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]  # длины колраблей
        board = Board(size=self.size)  # создаем доску
        attempts = 0  # количесво попыток поставить корабли
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("Игра морской бой")
        print("Введите x и y")
        print("где x - строка, y -столбец")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска ИИ:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь")
                repeat = self.us.move()  # вызываем метод ход игрока
            else:
                print("-" * 20)
                print("Ходит ИИ")
                repeat = self.ai.move()
            if repeat:  # нужно ли повторить ход
                num -= 1

            if self.ai.board.count == 7:  # кол-во пораженных кораблей
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("ИИ выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()