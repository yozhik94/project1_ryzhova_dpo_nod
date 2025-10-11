from labyrinth_game.utils import describe_current_room


def get_input(prompt="> "):
    """Получает ввод от пользователя и обрабатывает выход из игры."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    """Показывает инвентарь игрока."""
    inventory = game_state['player_inventory']
    if not inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("В вашем инвентаре:")
        for item in inventory:
            print(f"  - {item}")

def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении."""
    game_rooms = game_state['game_rooms'] # <-- Используем "живую" карту
    current_room_name = game_state['current_room']
    current_room_data = game_rooms[current_room_name]

    if direction in current_room_data['exits']:
        new_room_name = current_room_data['exits'][direction]
        game_state['current_room'] = new_room_name
        game_state['steps_taken'] += 1
        print(f"Вы перешли в направлении '{direction}'.")
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    """Позволяет игроку подобрать предмет."""
    game_rooms = game_state['game_rooms'] # <-- Используем "живую" карту
    current_room_name = game_state['current_room']
    room_items = game_rooms[current_room_name]['items']

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in room_items:
        game_state['player_inventory'].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}.")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """Позволяет игроку использовать предмет из инвентаря."""
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Вы зажгли факел. Стало намного светлее.")
    elif item_name == 'sword':
        print("Вы чувствуете себя увереннее с мечом в руке.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty_key')
            print("Вы открыли бронзовую шкатулку и нашли внутри ржавый ключ!")
        else:
            print("Шкатулка пуста.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
