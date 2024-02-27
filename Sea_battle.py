from In_logica import Board, Dot, Ship, Player
import random

class AI(Player):
    def ask(self):
        dot = random.choice(list(board1.pole_free))
        return dot

class User(Player):
    def ask(self):
        print('Выберите точку для выстрела:')
        while True:
            try:
                x = int(input('Введите координуату по х (от 1 до 6:)'))
                y = int(input('Введите координуату по y (от 1 до 6:)'))
                if not board2.out(Dot(x, y)):
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Вы ошиблись при вводе')
        return Dot(x, y)

    def move(self, board, dot):
        if board.shot(dot):
            board.see_booard()
            return True
        else:
            board.see_booard()
            return False
class Game:
    def __init__(self):
        self.user = user
        self.board_user = user.board_own
        self.ai = ai
        self.board_ai = ai.board_own
    def random_board(self):
        final_add_ship(board1)
        final_add_ship(board2)
    def greet(self):
        print(""""Добрый день. Это игра морской бой. Вам предлагается играть против компьютера.
        Правила игры следующие: после каждого хода вам будет высвечиваться поле на котором:
        о - клетки, куда выстрел еще не производился, 
        # - клетки, в которых вы подбили корабль компьютера,
        х - попадание в пустую клетку.
            КОРАБЛИ РАССТАВЛНЫ МОЖНО НАЧИНАТЬ ИГРУ. ПОБЕДИТ СИЛЬНЕЙШИЙ""")
    def loop(self):
        while True:
            dot_U = user.ask()
            while user.move(board2, dot_U):
                dot_U = user.ask()
            dot_AI = ai.ask()
            while ai.move(board1, dot_AI):
                dot_AI = ai.ask()

            if len(board1.dots_sh) == 0 or len(board2.dots_sh) == 0:
                print('Игра окончена.')
                if len(board1.dots_sh) == 0:
                    print('Победил компьютер!!!')
                if len(board2.dots_sh) == 0:
                    print('Победил человек!!!')
                break
    def start(self):
        game.random_board()
        game.greet()
        game.loop()

def make_doska(raz):
    """"функуия создания двумерного массива размером игрового поля"""
    doska = ['o'] * raz
    for i in range(raz):
        doska[i] = ['o'] * raz
    return doska

def final_add_ship(board):
    """"функция финальной расстановки кораблей аргумент берет доску"""
    while True:
        try:
            for i in ships1:
                board.add_ship(i)
                board.countour(i)
        except ImportWarning:
            board.clear(pole)
        else:
            board.pole_free = pole.copy() # создаем поля под проверку выстрелов
            board.pole_busy = pole.copy()
            break

dot11, dot12, dot13, dot14, dot15, dot16 = Dot(1, 1), Dot(1, 2), Dot(1, 3), Dot(1, 4), Dot(1, 5), Dot(1, 6)
dot21, dot22, dot23, dot24, dot25, dot26 = Dot(2, 1), Dot(2, 2), Dot(2, 3), Dot(2, 4), Dot(2, 5), Dot(2, 6)
dot31, dot32, dot33, dot34, dot35, dot36 = Dot(3, 1), Dot(3, 2), Dot(3, 3), Dot(3, 4), Dot(3, 5), Dot(3, 6)
dot41, dot42, dot43, dot44, dot45, dot46 = Dot(4, 1), Dot(4, 2), Dot(4, 3), Dot(4, 4), Dot(4, 5), Dot(4, 6)
dot51, dot52, dot53, dot54, dot55, dot56 = Dot(5, 1), Dot(5, 2), Dot(5, 3), Dot(5, 4), Dot(5, 5), Dot(5, 6)
dot61, dot62, dot63, dot64, dot65, dot66 = Dot(6, 1), Dot(6, 2), Dot(6, 3), Dot(6, 4), Dot(6, 5), Dot(6, 6)

pole = [dot11, dot12, dot13, dot14, dot15, dot16,
        dot21, dot22, dot23, dot24, dot25, dot26,
        dot31, dot32, dot33, dot34, dot35, dot36,
        dot41, dot42, dot43, dot44, dot45, dot46,
        dot51, dot52, dot53, dot54, dot55, dot56,
        dot61, dot62, dot63, dot64, dot65, dot66]

ship_1_11, ship_1_12, ship_1_13, ship_1_14, ship_1_21, ship_1_22, ship_1_3 = Ship(width=1, live=[]), \
    Ship(width=1, live=[]), Ship(width=1, live=[]), Ship(width=1, live=[]), Ship(width=2, live=[]), \
    Ship(width=2, live=[]), Ship(width=3, live=[])
ship_2_11, ship_2_12, ship_2_13, ship_2_14, ship_2_21, ship_2_22, ship_2_3 = Ship(width=1, live=[]), \
    Ship(width=1, live=[]), Ship(width=1, live=[]), Ship(width=1, live=[]), Ship(width=2, live=[]), \
    Ship(width=2, live=[]), Ship(width=3, live=[])
ships1 = [ship_1_3, ship_1_21, ship_1_22, ship_1_11, ship_1_12, ship_1_13, ship_1_14]
ships2 = [ship_2_3, ship_2_21, ship_2_22, ship_2_11, ship_2_12, ship_2_13, ship_2_14]
doska1 = make_doska(6)
doska2 = make_doska(6)
board1 = Board(pole_free=pole.copy(), pole_busy=[], doska_pl=doska1, ships=[], dots_sh=[],
                       hid=1, ships_live=[])
board2 = Board(pole_free=pole.copy(), pole_busy=[], doska_pl=doska2, ships=[], dots_sh=[],
                       hid=2, ships_live=[])

user = User(board1, board2)
ai = AI(board2, board1)

game = Game()
game.start()

