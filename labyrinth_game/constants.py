# labyrinth_game/constants.py

ROOMS = {
    'entrance': {
        'description': (
            'Вы в темном входе лабиринта. Стены покрыты мхом. '
            'На полу лежит старый факел.'
        ),
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': (
            'Большой зал с эхом. По центру стоит пьедестал '
            'с запечатанным сундуком.'
        ),
        'exits': {'south': 'entrance', 'west': 'library'},
        'items': [],
        'puzzle': (
            'На пьедестале надпись: "Назовите число, которое идет '
            'после девяти". Введите ответ цифрой или словом.', '10'
        )
    },
    'trap_room': {
          'description': (
              'Комната с хитрой плиточной поломкой. На стене видна '
              'надпись: "Осторожно — ловушка".'
          ),
          'exits': {'west': 'entrance', 'down': 'dungeon'},
          'items': ['rusty_key'],
          'puzzle': (
              'Система плит активна. Чтобы пройти, назовите слово "шаг" '
              'три раза подряд (введите "шаг шаг шаг")', 'шаг шаг шаг'
          )
    },
    'library': {
          'description': (
              'Пыльная библиотека. На полках старые свитки. Где-то здесь '
              'может быть ключ от сокровищницы.'
          ),
          'exits': {'east': 'hall', 'north': 'armory', 'secret': 'secret_chamber'},
          'items': ['ancient_book'],
          'puzzle': (
              'В одном свитке загадка: "Что растет, когда его съедают?" '
              '(ответ одно слово)', 'резонанс'
          )
    },
    'armory': {
          'description': (
              'Старая оружейная комната. На стене висит меч, '
              'рядом — небольшая бронзовая шкатулка.'
          ),
          'exits': {'south': 'library'},
          'items': ['sword', 'bronze_box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': (
              'Комната, на столе большой сундук. Дверь заперта — нужен '
              'особый ключ.'
          ),
          'exits': {'west': 'secret_chamber'},
          'items': ['treasure_chest'],
          'puzzle': (
              'Дверь защищена кодом. Введите код (подсказка: это число '
              'пятикратного шага, 2*5= ? )', '10'
          )
    },
    'dungeon': {
          'description': (
              'Вы в сыром и холодном подземелье. В углу скелет '
              'незадачливого искателя приключений.'
          ),
          'exits': {'up': 'trap_room'},
          'items': [],
          'puzzle': None
    },
    'secret_chamber': {
        'description': (
            'Тайная комната, скрытая за книжным шкафом. На бархатной '
            'подушке лежит изящный ключ.'
        ),
        'exits': {'out': 'library', 'east': 'treasure_room'},
        'items': ['treasure_key'],
        'puzzle': None
    }
}

