import os
import sys

import login_window
from settings import *
import time
import sqlite3

# Подключение к базе данных SQLite
CON = sqlite3.connect('Base_Date.sqlite')
CUR = CON.cursor()

# Список файлов уровней
LEVELS_SP = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt', 'level6.txt', 'level7.txt',
             'level8.txt']

# Группа для спрайтов ключей
key_group = pygame.sprite.Group()

# Создание фонового изображения
BackGround = Background('./image/H-qKzXj2k-k.jpg', [0, 0])


# Функция для загрузки изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('image', name)  # Полный путь к изображению
    if not os.path.isfile(fullname):  # Проверка существования файла
        print(f"Файл с изображением '{fullname}' не найден")
        raise FileNotFoundError(fullname)
    image = pygame.image.load(fullname)  # Загрузка изображения
    return image


# Инициализация Pygame и получение настроек
pygame.init()
get_config()
settings = start_app()
screen = settings[0]  # Экран
FPS = settings[1]  # Частота кадров

# Группы спрайтов
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

# Словарь с изображениями для тайлов
tile_image = {
    'wall': load_image('stena.jpg'),
    'hero': load_image('main_hero.png'),
    'door': load_image('door.png'),
    'key': load_image('key.png')
}

# Размеры тайлов
tile_width = tile_height = 50
player_x, player_y = 0, 0  # Начальные координаты игрока


# Базовый класс для спрайтов
class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


# Класс для тайлов
class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]  # Изображение тайла
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)  # Позиция тайла
        if tile_type == 'key':  # Если это ключ, добавляем его в отдельную группу
            self.add(key_group)


# Класс для игрока
class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = tile_image['hero']  # Изображение игрока
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)  # Позиция игрока
        self.pos = (pos_x, pos_y)
        self.keys_collected = 0  # Счетчик собранных ключей

    # Метод для перемещения игрока
    def move(self, dx, dy):
        global player_x, player_y
        while True:
            new_x = player_x + dx
            new_y = player_y + dy
            if 0 <= new_x < len(level[0]) and 0 <= new_y < len(level):  # Проверка границ уровня
                if level[new_y][new_x] != '#':  # Проверка на стену
                    if level[new_y][new_x] == '-':  # Проверка на ключ
                        self.keys_collected += 1  # Увеличиваем счетчик ключей
                        level[new_y] = level[new_y][:new_x] + '.' + level[new_y][new_x + 1:]  # Убираем ключ с карты
                        for key_sprite in key_group:  # Удаляем спрайт ключа
                            if key_sprite.rect.collidepoint(new_x * tile_width, new_y * tile_height):
                                key_sprite.kill()
                                print('peresec')
                    level[player_y] = level[player_y][:player_x] + '.' + level[player_y][player_x + 1:]
                    level[new_y] = level[new_y][:new_x] + '@' + level[new_y][new_x + 1:]
                    player_x, player_y = new_x, new_y
                    self.rect.move_ip(dx * tile_width, dy * tile_height)  # Обновление позиции спрайта
                else:
                    break
            else:
                break


# Функция для завершения работы программы
def terminate():
    pygame.quit()
    sys.exit()


# Функция для загрузки уровня из файла
def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


# Функция для отображения списка уровней
def show_levels():
    level1 = login_window.Button(200, 300, 150, 50, 'Уровень 1')
    level2 = login_window.Button(200, 360, 150, 50, 'Уровень 2')
    level3 = login_window.Button(200, 420, 150, 50, 'Уровень 3')
    level4 = login_window.Button(200, 480, 150, 50, 'Уровень 4')
    level5 = login_window.Button(600, 300, 150, 50, 'Уровень 5')
    level6 = login_window.Button(600, 360, 150, 50, 'Уровень 6')
    level7 = login_window.Button(600, 420, 150, 50, 'Уровень 7')
    font1 = pygame.font.Font(None, 85)
    font2 = pygame.font.Font(None, 36)
    text = font1.render("УРОВНИ", True, (255, 0, 0))
    text2 = font2.render('Передвигаясь по лабиринту с помощью стрелок дойдите до выхода',
                         True, (255, 255, 255))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1.rect.collidepoint(event.pos):
                    check_level_num(0)
                    running = False
                if level2.rect.collidepoint(event.pos):
                    check_level_num(1)
                    running = False
                if level3.rect.collidepoint(event.pos):
                    check_level_num(2)
                    running = False
                if level4.rect.collidepoint(event.pos):
                    check_level_num(3)
                    running = False
                if level5.rect.collidepoint(event.pos):
                    check_level_num(4)
                    running = False
                if level6.rect.collidepoint(event.pos):
                    check_level_num(5)
                    running = False
                if level7.rect.collidepoint(event.pos):
                    check_level_num(6)
                    running = False
        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)
        screen.blit(text, (350, 50))
        screen.blit(text2, (10, 100))
        level1.draw_level_end(screen)
        level2.draw_level_end(screen)
        level3.draw_level_end(screen)
        level4.draw_level_end(screen)
        level5.draw_level_end(screen)
        level6.draw_level_end(screen)
        level7.draw_level_end(screen)
        pygame.display.flip()


# Функция для проверки номера уровня
def check_level_num(num):
    cur_stolb = LEVELS_SP[num]
    cur_level = './levels_txt/' + cur_stolb
    cur_stolb = cur_stolb[:cur_stolb.index('.')]
    global level
    level = load_level(cur_level)
    norm_level = []
    for i in level:
        norm_level.append(''.join(i))
    level = norm_level.copy()
    norm_level.clear()
    run_game_py(cur_level, cur_stolb)


# Функция для генерации уровня
def generate_level(level):
    new_player = None

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
                global player_x, player_y
                player_x, player_y = x, y
            elif level[y][x] == '*':
                Tile('door', x, y)
            elif level[y][x] == '-':
                Tile('key', x, y)  # Ключи добавляются в key_group

    return new_player


# Функция для получения имени пользователя
def get_user(username):
    global user
    user = username


# Функция для завершения игры
def game_end(cur_time, rec_time, rec, cur_level, cur_stolb):
    running = True
    to_level = login_window.Button(350, 300, 150, 50, 'К уровням')
    exit = login_window.Button(15, 20, 100, 50, "выход")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if to_level.rect.collidepoint(event.pos):
                    show_levels()
                    terminate()
                if exit.rect.collidepoint(event.pos):
                    terminate()

        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)
        font1 = pygame.font.Font(None, 74)
        font2 = pygame.font.Font(None, 36)
        tex = font1.render('Уровень Завершен', True, (255, 0, 0))
        screen.blit(tex, (250, 20))
        tex2 = font2.render(f'Текущее время:{cur_time}', True, (255, 255, 255))
        screen.blit(tex2, (350, 100))
        tex3 = font2.render(f'Рекордное время:{rec_time}', True, (255, 255, 255))
        screen.blit(tex3, (350, 150))
        if rec:
            tex4 = font1.render('ВЫ ПОБИЛИ РЕКОРД', True, (0, 255, 0))
            screen.blit(tex4, (230, 210))
        to_level.draw_level_end(screen)
        exit.draw_level_end(screen)
        pygame.display.flip()


# Основная функция для запуска игры
def run_game_py(cur_level, cur_stolb):
    sprite_group.empty()
    hero_group.empty()
    key_group.empty()  # Очищаем группу ключей

    start_time = time.time()
    running = True
    level_map = load_level(cur_level)  # Загружаем уровень из файла
    hero = generate_level(level_map)  # Генерируем уровень
    ret_level = login_window.Button(10, 670, 130, 30, 'к уровням->')

    cur_record = CUR.execute(f"SELECT {cur_stolb} FROM login WHERE username = '{user}'").fetchall()
    cur_record = cur_record[0][0]
    cur_record_min = ''
    cur_record_sec = ''
    font = pygame.font.Font(None, 74)
    font_keys = pygame.font.Font(None, 36)  # Шрифт для отображения счетчика ключей

    if cur_record:
        cur_record_min = int(cur_record[:cur_record.index(':')])
        cur_record_sec = int(cur_record[cur_record.index(':') + 1:])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Движение
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    hero.move(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    hero.move(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    hero.move(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    hero.move(1, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ret_level.rect.collidepoint(event.pos):
                    show_levels()
                    running = False
                    terminate()

        elapsed_time = f'{time.time() - start_time:.2f}'
        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)
        sprite_group.draw(screen)
        hero_group.draw(screen)
        key_group.draw(screen)  # Отрисовываем ключи

        new_minutes = int(float(elapsed_time)) // 60
        new_seconds = int(float(elapsed_time)) % 60
        time_display = font.render(f"{new_minutes}:{new_seconds}", True, (255, 255, 255))
        screen.blit(time_display, (700, 20))

        # Отображение счетчика ключей
        keys_display = font_keys.render(f"Ключи: {hero.keys_collected}", True, (255, 255, 255))
        screen.blit(keys_display, (20, 20))
        ret_level.draw_level_end(screen)

        pygame.display.flip()

        # Проверка завершения уровня
        if level_map[player_y][player_x] == '*' and hero.keys_collected == 4:
            time_to_BD = f'{new_minutes}:{new_seconds}'
            if cur_record:
                if new_minutes < cur_record_min or (new_seconds < cur_record_sec and new_minutes == cur_record_min):
                    CUR.execute(f"UPDATE login SET {cur_stolb} = '{time_to_BD}' WHERE username = '{user}'")
                    CON.commit()
                    game_end(time_to_BD, time_to_BD, 1, cur_level, cur_stolb)
                else:
                    game_end(time_to_BD, cur_record, 0, cur_level, cur_stolb)
            else:
                CUR.execute(f"UPDATE login SET {cur_stolb} = '{time_to_BD}' WHERE username = '{user}'")
                CON.commit()
                game_end(time_to_BD, time_to_BD, 1, cur_level, cur_stolb)
            running = False
            screen.fill((0, 0, 0))
            terminate()
