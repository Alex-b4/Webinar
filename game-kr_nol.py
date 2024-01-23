pole = (['_|', 0, 1, 2], [0,' ', ' ', ' '], [1,' ', ' ', ' '], [2,' ', ' ', ' ']) # создаем кортеж с полем
razmer = (0, 1, 2) # кортеж для проверки поподания в поле
def pobeda(): # функция проверки выполнения условия окончания партии
    pob1 = pole[1][1] == pole[2][2] == pole[3][3] == 'x' \
        or pole[1][1] == pole[1][2] == pole[1][3] == 'x'\
        or pole[2][1] == pole[2][2] == pole[2][3] == 'x'\
        or pole[3][1] == pole[3][2] == pole[3][3] == 'x'\
        or pole[1][1] == pole[2][1] == pole[3][1] == 'x'\
        or pole[1][2] == pole[2][2] == pole[3][2] == 'x'\
        or pole[1][3] == pole[2][3] == pole[3][3] == 'x'\
        or pole[1][3] == pole[2][2] == pole[3][1] == 'x'
    pob2 = pole[1][1] == pole[2][2] == pole[3][3] == 'o' \
           or pole[1][1] == pole[1][2] == pole[1][3] == 'o' \
           or pole[2][1] == pole[2][2] == pole[2][3] == 'o' \
           or pole[3][1] == pole[3][2] == pole[3][3] == 'o' \
           or pole[1][1] == pole[2][1] == pole[3][1] == 'o' \
           or pole[1][2] == pole[2][2] == pole[3][2] == 'o' \
           or pole[1][3] == pole[2][3] == pole[3][3] == 'o' \
           or pole[1][3] == pole[2][2] == pole[3][1] == 'o'
    if pob2 or pob1:
        return True

def drawing_pole(): # функция для рисования поля
    print(*pole[0], '\n', *pole[1], '\n', *pole[2], '\n', *pole[3], '\n')


def step(): # функция для запроса хода игрока и его проверка
    x = int(input('Введите номер клетки по вертикали (0,1,2): '))
    prov = x in razmer
    while not prov: # проверка попадания в поле по вертикали
        x = int(input('Вы ошиблись при вводе. Размеры поля 3х3. Возможен выбор 0,1,2: '))
        prov = x in razmer
    y = int(input('Введите номер клетки по горизонтали (0,1,2): '))
    prov = y in razmer
    while not prov: # проверка попадания в поле по горизонтали
        y = int(input('Вы ошиблись при вводе. Размеры поля 3х3. Возможен выбор 0,1,2: '))
        prov = y in razmer
    return (x, y)

def busy(): # проверка занятости квадрата
    x, y = step()
    while pole[x + 1][y + 1] != ' ':
        print('Квадрат занят. Выберите другой.')
        x, y = step()
    return (x, y)

print('Игра крестики-нолики!!!')
drawing_pole()

while not pobeda(): # циклим до выполнения условия трех в одну линию
    print('Ходит первый игрок нолик.')
    x, y = busy()
    pole[x + 1][y + 1] = 'x'
    drawing_pole()
    if pobeda(): # проверка на окнчание игры после хода второго игрока
        break
    print('Ходит второй игрок крестики.')
    x, y = busy()
    pole[x + 1][y + 1] = 'o'
    drawing_pole()
if pobeda():
    print('Игра окончена!!!')