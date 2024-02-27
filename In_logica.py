import random

class Dot:
    def __init__(self, y , x):
        self.y = y
        self.x = x
    def __eq__(self, other):
       return self.x == int(other.x) and self.y == int(other.y)


class Ship:
    def __init__(self, width, live, start = Dot(0,0), direct = None):
        self.width = width
        self.start = start
        self.direct = direct # значение 1 - вертикально, 2 - горизонтально
        self.live = live


class Board:
    def __init__(self, pole_free, pole_busy, doska_pl, ships, dots_sh, hid, ships_live):
        self.pole_free = pole_free # свободный точки без кораблей
        self.pole_busy = pole_busy # точки с кораблями с кораблями
        self.doska = doska_pl # доска для вывода
        self.ships = ships # корабли установленные на поле
        self.dots_sh = dots_sh # точки с кораблями
        self.hid = hid # идентификато доски
        self.ships_live = ships_live # живые корабли на доске не знаю как использовать

    def add_ship(self, ship):
        """устанавливает переданный корабль на поле"""
        while True:
            try:
                if len(list(self.pole_free)) == 0:
                    raise ImportWarning
                ship.start = random.choice(list(self.pole_free))
                ship.direct = random.randint(1,2)
                x = ship.start.x
                y = ship.start.y
                width = ship.width
                direct = ship.direct
                # проверка кораблей на возможность вмесить в доску с учетом выбранной кординаты
                # установка корабля
                if direct == 2: # проверяет возможность вместить корабль по горизонтали
                    if x > (7 - width):
                        raise IndexError
                    for i in range(0, width):
                        if Dot(y, x + i) in self.pole_busy:
                            raise IndexError
                    for i in range(0, width):
                        self.pole_busy.append(Dot(y, x + i))
                        self.pole_free.remove(Dot(y, x + i))
                        self.dots_sh.append(Dot(y, x + i))
                        ship.live.append(Dot(y, x + i))
                    self.ships.append(ship) # внесение корабля в параметр ships доски
                    break

                if direct == 1: # проверяет возможность вмещения корабля по вертикали
                    if y > (7 - width):
                        raise IndexError
                    for i in range(0, width):
                        if Dot(y + i, x) in self.pole_busy:
                            raise IndexError
                    for i in range(0, width):
                        self.pole_busy.append(Dot(y+i, x))
                        self.pole_free.remove(Dot(y+i, x))
                        self.dots_sh.append(Dot(y+i, x))
                        ship.live.append(Dot(y+i, x))
                    self.ships.append(ship)
                    break

            except IndexError:
                pass
            except ValueError:
                pass

    def countour(self, ship):
        """обводит установленный корабль"""
        y = ship.start.y
        x = ship.start.x
        width = ship.width
        direct = ship.direct
        if direct == 1:
            for n in range(0,3):
                for i in range(0, width + 2):
                    if 1 <= (y - 1 + i) <= 6 and 1 <= (x - 1 + n) <= 6:
                        if Dot(y - 1 + i, x - 1 + n) not in self.pole_busy:
                            self.pole_busy.append(Dot(y - 1 + i, x - 1 + n))
                            self.pole_free.remove(Dot(y - 1 + i, x - 1 + n))
        if direct == 2:
            for n in range(0,3):
                for i in range(0, width + 2):
                    if 1 <= (y - 1 + n) <= 6 and 1 <= (x - 1 + i) <= 6:
                        if Dot(y - 1 + n, x - 1 + i) not in self.pole_busy:
                            self.pole_busy.append(Dot(y - 1 + n, x - 1 + i))
                            self.pole_free.remove(Dot(y - 1 + n, x - 1 + i))
    def clear(self, pole):
        """очищает доску для повторной установки"""
        self.pole_free = pole.copy()
        self.pole_busy.clear()
        self.ships.clear()
        self.dots_sh.clear()
        self.ships_live.clear()


    def out(self, dot):
        for i in self.pole_busy:
            if i == dot:
                if i in self.pole_free:
                    return False
        return True

    def shot(self, dot):
        for i in self.dots_sh:
            if i == dot:
                self.dots_sh.remove(dot)
                self.pole_free.remove(dot)
                self.doska[dot.x-1][dot.y-1] = '#'
                if self.hid == 1:
                    print('Компьютер попал!!!!!!')
                if self.hid == 2:
                    print('Вы попали!!!')
                return True
                break
        self.doska[dot.x - 1][dot.y - 1] = 'x'
        self.pole_free.remove(dot)
        return False

    def see_booard(self):
        print(f'  1|2|3|4|5|6')
        print(f'1|{self.doska[0][0]}|{self.doska[0][1]}|{self.doska[0][2]}|{self.doska[0][3]}|{self.doska[0][4]}|{self.doska[0][5]}')
        print(f'2|{self.doska[1][0]}|{self.doska[1][1]}|{self.doska[1][2]}|{self.doska[1][3]}|{self.doska[1][4]}|{self.doska[1][5]}')
        print(f'3|{self.doska[2][0]}|{self.doska[2][1]}|{self.doska[2][2]}|{self.doska[2][3]}|{self.doska[2][4]}|{self.doska[2][5]}')
        print(f'4|{self.doska[3][0]}|{self.doska[3][1]}|{self.doska[3][2]}|{self.doska[3][3]}|{self.doska[3][4]}|{self.doska[3][5]}')
        print(f'5|{self.doska[4][0]}|{self.doska[4][1]}|{self.doska[4][2]}|{self.doska[4][3]}|{self.doska[4][4]}|{self.doska[4][5]}')
        print(f'6|{self.doska[5][0]}|{self.doska[5][1]}|{self.doska[5][2]}|{self.doska[5][3]}|{self.doska[5][4]}|{self.doska[5][5]}')

class Player:
    def __init__(self, board_own, board_enemy):
        self.board_own = board_own
        self.board_enemy = board_enemy

    def ask(self):
        print('ok')

    def move(self, board, dot):
        if board.shot(dot):
            return True
        else:
            return False
