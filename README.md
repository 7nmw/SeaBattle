SeaBattle
Игра морской бой

Правила игры:
Интерфейс приложения представляет собой консольное окно с двумя полями 6х6 вида Пользователь и компьютер (ИИ) по очереди стреляют по кораблям. Чтобы сделать выстрел нужно ввести 2 координаты, где x - строка, y -столбец На каждой доске (у ИИ и у игрока) находится следующее количество кораблей: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.

Можно выделить две группы классов: Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней. Внешняя логика игры — пользовательский интерфейс, искусственный интеллект, игровой контроллер, который считает побитые корабли. В начале имеет смысл написать классы исключений, которые будет использовать наша программа. Например, когда игрок пытается выстрелить в клетку за пределами поля, во внутренней логике должно выбрасываться соответствующее исключение BoardOutException, а потом отлавливаться во внешней логике, выводя сообщение об этой ошибке пользователю.

Класс Dot — класс точек на поле. Каждая точка описывается параметрами: Координата по оси x. Координата по оси y. Очень удобно будет реализовать в этом классе метод eq, чтобы точки можно было проверять на равенство. Тогда, чтобы проверить, находится ли точка в списке, достаточно просто использовать оператор in, как мы делали это с числами.

Следующим идёт класс Ship — корабль на игровом поле, который описывается параметрами: Длина. Точка, где размещён нос корабля. Направление корабля (вертикальное/горизонтальное). Количеством жизней (сколько точек корабля ещё не подбито). И имеет метод dots, который возвращает список всех точек корабля.

Самый важный класс во внутренней логике — класс Board — игровая доска. Доска описывается параметрами:

Двумерный список, в котором хранятся состояния каждой из клеток. Список кораблей доски. Параметр hid типа bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага) или нет (для своей доски). Количество живых кораблей на доске. И имеет методы:

Метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключения). Метод contour, который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может). Метод, который выводит доску в консоль в зависимости от параметра hid. Метод out, который для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля, и False, если не выходит. Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, нужно выбрасывать исключения). Теперь нужно заняться внешней логикой: класс Player — класс игрока в игру (и AI, и пользователь). Этот класс будет родителем для классов с AI и с пользователем. Игрок описывается параметрами:

Собственная доска (объект класса Board). Доска врага. И имеет следующие методы:

ask — метод, который «спрашивает» игрока, в какую клетку он делает выстрел. Пока мы делаем общий для AI и пользователя класс, этот метод мы описать не можем. Оставим этот метод пустым. Тем самым обозначим, что потомки должны реализовать этот метод. move — метод, который делает ход в игре. Тут мы вызываем метод ask, делаем выстрел по вражеской доске (метод Board.shot), отлавливаем исключения, и если они есть, п ытаемся повторить ход. Метод должен возвращать True, если этому игроку нужен повторный ход (например, если он выстрелом подбил корабль). Теперь нам остаётся унаследовать классы AI и User от Player и переопределить в них метод ask. Для AI это будет выбор случайной точки, а для User этот метод будет спрашивать координаты точки из консоли.

После создаём наш главный класс — класс Game. Игра описывается параметрами:

Игрок-пользователь, объект класса User. Доска пользователя. Игрок-компьютер, объект класса AI. Доска компьютера. И имеет методы:

random_board — метод генерирует случайную доску. Для этого мы просто пытаемся в случайные клетки изначально пустой доски расставлять корабли (в бесконечном цикле пытаемся поставить корабль в случайную доску, пока наша попытка не окажется успешной). Лучше расставлять сначала длинные корабли, а потом короткие. Если было сделано много (несколько тысяч) попыток установить корабль, но это не получилось, значит доска неудачная и на неё корабль уже не добавить. В таком случае нужно начать генерировать новую доску. greet — метод, который в консоли приветствует пользователя и рассказывает о формате ввода. loop — метод с самим игровым циклом. Там мы просто последовательно вызываем метод mode для игроков и делаем проверку, сколько живых кораблей осталось на досках, чтобы определить победу. start — запуск игры.
