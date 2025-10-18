import math

# --- ИМЕНОВАННЫЕ КОНСТАНТЫ ---
EVENT_PROBABILITY_MODULO = 10  # Вероятность события 1/10
FATAL_TRAP_THRESHOLD = 3       # Порог "смертельного урона" (значения 0, 1, 2)
TRAP_DAMAGE_MODULO = 10        # Диапазон для расчета урона ловушки
RANDOM_EVENT_TYPES_COUNT = 4   # Количество типов случайных событий

# --- ФУНКЦИИ ДЛЯ СЛУЧАЙНЫХ СОБЫТИЙ ---

def pseudo_random(seed, modulo):
    """Генерирует предсказуемое псевдослучайное число."""
    if modulo <= 0:
        return 0
    # Математическая формула для предсказуемой псевдослучайности
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = x - math.floor(x)
    return int(fractional_part * modulo)

def trigger_trap(game_state):
    """Активирует ловушку, которая может забрать предмет или закончить игру."""
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    if inventory:
        index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы споткнулись и выронили предмет: {lost_item}")
    else:
        damage_chance = pseudo_random(
            game_state['steps_taken'], TRAP_DAMAGE_MODULO
        )
        if damage_chance < FATAL_TRAP_THRESHOLD:
            print("Ловушка оказалась смертельной. Вы проиграли.")
            game_state['game_over'] = True
        else:
            print("Вы чудом уцелели!")

def random_event(game_state):
    """Запускает случайное событие во время путешествия."""
    if pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY_MODULO) != 0:
        return

    event_type = pseudo_random(
        game_state['steps_taken'] + 1, RANDOM_EVENT_TYPES_COUNT
    )
    game_rooms = game_state['game_rooms']
    current_room_name = game_state['current_room']
    
    if event_type == 0:
        print("\nСобытие: Вы заметили блеск на полу и нашли монетку!")
        game_rooms[current_room_name]['items'].append('coin')
    elif event_type == 1:
        print("\nСобытие: В тенях что-то прошуршало...")
        if 'sword' in game_state['player_inventory']:
            print("Вы крепче сжали рукоять меча, и шорох прекратился.")
    elif event_type == 2:
        if (current_room_name == 'trap_room' 
                and 'torch' not in game_state['player_inventory']):
            print("\nСобытие: В темноте вы наступили на шаткую плиту!")
            trigger_trap(game_state)
    elif event_type == 3:
        if current_room_name == 'dungeon':
            print("\nСобытие: Существо в углу начинает двигаться в вашу сторону!")
            if 'sword' in game_state['player_inventory']:
                print(
                    "Вы выставляете вперед меч, и оно с шипением" 
                    "отступает обратно в тень."
                )
            else:
                print(
                    "У вас нет ничего, чтобы защититься, и вы в страхе замираете. "
                    "К счастью, оно не нападает."
                )

# --- ОСНОВНЫЕ ФУНКЦИИ ИГРЫ ---

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
        
    question, correct_answer = room['puzzle']
    
    answers = {correct_answer}
    if correct_answer == '10':
        answers.add('десять')

    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()

    if user_answer in answers:
        print("Верно! Загадка решена.")
        room['puzzle'] = None
        if room_name == 'hall':
            print("Щелкнул потайной механизм в стене.")
        elif room_name == 'library':
            print("Вы чувствуете, как ваш разум прояснился.")
    else:
        print("Неверно. Попробуйте снова.")
        if room_name == 'trap_room':
            trigger_trap(game_state)

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
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код.")
        else:
            print("Вы решаете пока не трогать сундук.")

def show_help(commands):
    """Показывает список доступных команд с форматированием."""
    print("\nДоступные команды:")
    for command, description in commands.items():
        print(f"  {command:<20} - {description}")


