#!/usr/bin/env python3

# Импортируем все необходимое из других файлов
import copy

from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
    """Обрабатывает введенную игроком команду."""
    parts = command.split()
    if not parts:
        print("Вы ничего не ввели.")
        return

    verb = parts[0]
    
    # Используем match/case для элегантной обработки команд
    match verb:
        case "go":
            if len(parts) > 1:
                move_player(game_state, parts[1])
            else:
                print("Укажите направление (например, 'go north').")
        case "take":
            if len(parts) > 1:
                take_item(game_state, parts[1])
            else:
                print("Укажите предмет (например, 'take torch').")
        case "use":
            if len(parts) > 1:
                use_item(game_state, parts[1])
            else:
                print("Укажите предмет (например, 'use torch').")
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "solve":
            solve_puzzle(game_state) # Логику добавим на следующем шаге
        case "help":
            show_help() # Логику добавим на следующем шаге
        case "quit" | "exit":
            print("Спасибо за игру! До встречи!")
            game_state['game_over'] = True
        case _:
            print("Я не понимаю эту команду. Введите 'help' для списка команд.")

def main():
    """Основная функция игры, запускает игровой цикл."""
    # 3. Создаем словарь состояния игры
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
        # Создаем полную, независимую копию карты для этой сессии игры
        'game_rooms': copy.deepcopy(ROOMS) 
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("> ")
        # Передаем весь game_state в обработчик
        process_command(game_state, command)

# Стандартная конструкция для запуска main()
if __name__ == "__main__":
    main()
