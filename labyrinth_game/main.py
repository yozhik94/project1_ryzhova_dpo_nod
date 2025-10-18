#!/usr/bin/env python3

# Импортируем все необходимое из других файлов
import copy

from labyrinth_game.constants import COMMANDS, ROOMS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
    """Обрабатывает введенную игроком команду."""
    parts = command.strip().split()
    if not parts:
        print("Вы ничего не ввели.")
        return

    verb = parts[0]

    # Список всех возможных направлений для односложных команд
    directions = {"north", "south", "east", "west", "up", "down", "in", "out", "secret"}

    # Превращаем 'north' в 'go north' для унификации
    if verb in directions and len(parts) == 1:
        parts = ["go", verb]
        verb = "go"

    match verb:
        case "go":
            if len(parts) > 1:
                move_player(game_state, parts[1])
            else:
                print("Укажите направление (например, 'go north').")
        
        case "solve":
            # Особая логика для сокровищницы
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        
        case "help":
            show_help(COMMANDS)
        
        case "take":
            if len(parts) > 1:
                item_name = "_".join(parts[1:]) 
                take_item(game_state, item_name)
            else:
                print("Укажите предмет (например, 'take rusty_key').")
        
        case "use":
            if len(parts) > 1:
                # То же самое для команды use
                item_name = " ".join(parts[1:])
                use_item(game_state, item_name)
            else:
                print("Укажите предмет (например, 'use torch').")
        
        case "look":
            describe_current_room(game_state)
        
        case "inventory":
            show_inventory(game_state)
        
        case "quit" | "exit":
            print("Спасибо за игру! До встречи!")
            game_state['game_over'] = True
        
        case _:
            print("Я не понимаю эту команду. Введите 'help' для списка команд.")


def main():
    """Основная функция игры, запускает игровой цикл."""

    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
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

