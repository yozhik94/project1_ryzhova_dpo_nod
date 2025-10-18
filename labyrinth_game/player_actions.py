
from labyrinth_game.utils import describe_current_room, random_event


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
    """Перемещает игрока, проверяет ключи и запускает события."""
    game_rooms = game_state['game_rooms']
    current_room_name = game_state['current_room']
    current_room_data = game_rooms[current_room_name]

    if direction in current_room_data['exits']:
        new_room_name = current_room_data['exits'][direction]

        # Проверка ключа для сокровищницы
        if (new_room_name == 'treasure_room' 
            and 'rusty_key' not in game_state['player_inventory']):
            print("Дверь заперта. Нужен ржавый ключ, чтобы пройти дальше.")
            return

        game_state['current_room'] = new_room_name
        game_state['steps_taken'] += 1
        
        if new_room_name == 'treasure_room':
             print("Вы используете ржавый ключ, и тяжелая дверь открывается.")

        print(f"\nВы перешли в направлении '{direction}'.")
        describe_current_room(game_state)
        
        # Запускаем случайное событие после хода
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Позволяет игроку подобрать предмет."""
    game_rooms = game_state['game_rooms']
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
        print(f"Предмета '{item_name}' здесь нет.")


def use_item(game_state, item_name):
    """Позволяет игроку использовать предмет из инвентаря."""
    if item_name not in game_state['player_inventory']:
        print(f"У вас нет предмета '{item_name}'.")
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


