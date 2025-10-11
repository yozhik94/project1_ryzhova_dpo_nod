def describe_current_room(game_state):
    """Описывает текущую комнату, ее предметы, выходы и загадки."""
    game_rooms = game_state['game_rooms'] 
    room_name = game_state['current_room']
    room = game_rooms[room_name]
    
    print("\n" + "="*20)
    print(f"== {room_name.upper()} ==")
    print("="*20)
    
    print(room['description'])

    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))

    if room['exits']:
        print("Выходы:", ", ".join(room['exits'].keys()))
        
    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду 'solve').")


def solve_puzzle(game_state):
    """Решает загадку в текущей комнате."""
    game_rooms = game_state['game_rooms']
    room_name = game_state['current_room']
    room = game_rooms[room_name]

    if not room['puzzle']:
        print("Загадок здесь нет.")
        return

    if room_name == 'treasure_room':
        attempt_open_treasure(game_state)
        return

    question, correct_answer = room['puzzle']
    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()

    if user_answer == correct_answer:
        print("Верно! Загадка решена.")
        room['puzzle'] = None
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    """Логика для открытия сундука с сокровищами."""
    game_rooms = game_state['game_rooms']    
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        game_rooms['treasure_room']['items'].remove('treasure_chest') 
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        print("Сундук заперт. Нужен специальный ключ, но можно попробовать ввести код.")
        choice = input("Ввести код? (да/нет): ").strip().lower()
        if choice == 'да':
            question, correct_answer = game_rooms['treasure_room']['puzzle'] 
            user_code = input("Введите код: ").strip().lower()
            if user_code == correct_answer:
                print("Код верный! Сундук открывается.")
                game_rooms['treasure_room']['items'].remove('treasure_chest') 
                game_state['game_over'] = True
            else:
                print("Неверный код.")
        else:
            print("Вы отступаете от сундука.")


def show_help():
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
