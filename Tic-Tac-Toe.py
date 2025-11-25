import random
import os
from datetime import datetime

os.makedirs("stats", exist_ok=True)

def save_stats(text):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f = open("stats/game_logs.txt", "a", encoding="utf-8")
    f.write(t + " - " + text + "\n")
    f.close()

def print_board(a):
    n = len(a)
    print("  ", end="")
    for i in range(n):
        print(i+1, end=" ")
    print()
    for i in range(n):
        print(i+1, end=" ")
        for j in range(n):
            if a[i][j] == " ":
                print(".", end=" ")
            else:
                print(a[i][j], end=" ")
        print()

def check_win(a, p):
    n = len(a)
    # горизонталь
    for i in range(n):
        for j in range(n-2):
            if a[i][j] == p and a[i][j+1] == p and a[i][j+2] == p:
                return True
    # вертикаль
    for i in range(n-2):
        for j in range(n):
            if a[i][j] == p and a[i+1][j] == p and a[i+2][j] == p:
                return True
    # диагональ \
    for i in range(n-2):
        for j in range(n-2):
            if a[i][j] == p and a[i+1][j+1] == p and a[i+2][j+2] == p:
                return True
    # диагональ /
    for i in range(n-2):
        for j in range(2, n):
            if a[i][j] == p and a[i+1][j-1] == p and a[i+2][j-2] == p:
                return True
    return False

def check_draw(a):
    for i in a:
        for j in i:
            if j == " ":
                return False
    return True

def bot_move(a):
    free = []
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] == " ":
                free.append((i, j))
    return random.choice(free)

def play():
    while True:
        # размер поля
        while True:
            try:
                n = int(input("Размер поля (3-9): "))
                if n < 3 or n > 9:
                    print("Ошибка!")
                    continue
                break
            except:
                print("Нужно число!")

        a = [[" " for i in range(n)] for j in range(n)]

        print("\n1 — игрок против игрока")
        print("2 — игрок против бота")
        mode = input("Выбор: ")
        while mode not in ("1", "2"):
            mode = input("Ошибка! Введите 1 или 2: ")

        player = random.choice(["X", "O"])
        print("\nПервым ходит:", player)

        while True:
            print("\nХод:", player)
            print_board(a)

            if mode == "2" and player == "O":
                r, c = bot_move(a)
                print("Бот сделал ход:", r+1, c+1)
            else:
                while True:
                    try:
                        r = int(input("Строка: ")) - 1
                        c = int(input("Столбец: ")) - 1
                        if r < 0 or r >= n or c < 0 or c >= n:
                            print("Вне поля!")
                            continue
                        if a[r][c] != " ":
                            print("Занято!")
                            continue
                        break
                    except:
                        print("Ошибка!")

            a[r][c] = player

            if check_win(a, player):
                print_board(a)
                print("Победа:", player)
                save_stats("Победа: " + player)
                break

            if check_draw(a):
                print_board(a)
                print("Ничья!")
                save_stats("Ничья")
                break

            if player == "X":
                player = "O"
            else:
                player = "X"

        again = input("\nСыграть снова? (y/n): ")
        if again.lower() != "y":
            print("Выход.")
            break

play()
