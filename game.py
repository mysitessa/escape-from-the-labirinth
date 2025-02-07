import os
import sys

import login_window
from settings import *
import time
from connect import connect

con = connect()
CON = con[0]
CUR = con[1]
LEVELS_SP = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt', 'level6.txt', 'level7.txt',
             'level8.txt']


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround = Background('./image/H-qKzXj2k-k.jpg', [0, 0])


def load_image(name, colorkey=None):
    fullname = os.path.join('image', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        raise FileNotFoundError(fullname)
    image = pygame.image.load(fullname)
    return image


pygame.init()
get_config()
settings = start_app()
screen = settings[0]
FPS = settings[1]

sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

tile_image = {
    'wall': load_image('stena.jpg'),
    'hero': load_image('main_hero.png'),
    'door': load_image('door.png')
}

tile_width = tile_height = 50
player_x, player_y = 0, 0


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = tile_image['hero']
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, dx, dy):
        global player_x, player_y
        # Продолжаем двигаться в заданном направлении до столкновения со стеной
        while True:
            new_x = player_x + dx
            new_y = player_y + dy
            if 0 <= new_x < len(level[0]) and 0 <= new_y < len(level):
                if level[new_y][new_x] != '#':
                    level[player_y] = level[player_y][:player_x] + '.' + level[player_y][player_x + 1:]
                    level[new_y] = level[new_y][:new_x] + '@' + level[new_y][new_x + 1:]
                    player_x, player_y = new_x, new_y
                    self.rect.move_ip(dx * tile_width, dy * tile_height)  # Обновление позиции спрайта
                else:
                    break
            else:
                break


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


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
            # нач коорд
            elif level[y][x] == '*':
                Tile('door', x, y)

    return new_player


def get_user(username):
    global user
    user = username


def game_end(cur_time, rec_time, rec, cur_level, cur_stolb):
    running = True
    to_level = login_window.Button(350, 300, 150, 50, 'К уровням')
    restart = login_window.Button(350, 400, 150, 50, 'Заново')
    exit = login_window.Button(15, 20, 100, 50, "выход")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart.rect.collidepoint(event.pos):
                    print(cur_level, cur_stolb)
                    run_game_py(cur_level, cur_stolb)
                    terminate()
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
        restart.draw_level_end(screen)
        exit.draw_level_end(screen)
        pygame.display.flip()


def run_game_py(cur_level, cur_stolb):
    sprite_group.empty()
    hero_group.empty()

    start_time = time.time()
    running = True
    level_map = load_level(cur_level)
    print(level_map)
    hero = generate_level(level_map)
    print(hero)

    cur_record = CUR.execute(f"SELECT {cur_stolb} FROM login WHERE username = '{user}'").fetchall()
    cur_record = cur_record[0][0]
    cur_record_min = ''
    cur_record_sec = ''
    font = pygame.font.Font(None, 74)

    if cur_record:
        cur_record_min = int(cur_record[:cur_record.index(':')])
        cur_record_sec = int(cur_record[cur_record.index(':') + 1:])
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Движение
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    hero.move(0, -1)
                    print(player_x, player_y)
                elif event.key == pygame.K_DOWN:
                    hero.move(0, 1)
                    print(player_x, player_y)
                elif event.key == pygame.K_LEFT:
                    hero.move(-1, 0)
                    print(player_x, player_y)
                elif event.key == pygame.K_RIGHT:
                    hero.move(1, 0)
                    print(player_x, player_y)

        elapsed_time = f'{time.time() - start_time}:.2f'
        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)
        sprite_group.draw(screen)
        hero_group.draw(screen)

        new_minutes = int(elapsed_time[:elapsed_time.index('.')]) // 60
        new_seconds = int(elapsed_time[:elapsed_time.index('.')]) % 60
        time_display = font.render(f"{new_minutes}:{new_seconds}", True, (255, 255, 255))
        screen.blit(time_display, (700, 20))
        pygame.display.flip()

        if cur_record and level_map[player_y][player_x] == '*':
            time_to_BD = f'{new_minutes}:{new_seconds}'
            if new_minutes < cur_record_min or (new_seconds < cur_record_sec and new_minutes == cur_record_min):
                CUR.execute(f"UPDATE login SET {cur_stolb} = '{time_to_BD}' WHERE username = '{user}'")
                CON.commit()
                game_end(time_to_BD, time_to_BD, 1, cur_level, cur_stolb)
                running = False
                screen.fill((0, 0, 0))
                terminate()
            else:
                game_end(time_to_BD, cur_record, 0, cur_level, cur_stolb)
                running = False
                screen.fill((0, 0, 0))
                cur_stolb = ''
                cur_level = ''
                terminate()

                # break
        elif level_map[player_y][player_x] == '*':
            time_to_BD = f'{new_minutes}:{new_seconds}'
            CUR.execute(f"UPDATE login SET {cur_stolb} = '{time_to_BD}' WHERE username = '{user}'")
            CON.commit()
            game_end(time_to_BD, time_to_BD, 1, cur_level, cur_stolb)
            print(cur_level, cur_stolb)
            running = False
            screen.fill((0, 0, 0))
            terminate()

    terminate()
