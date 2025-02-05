import os
import sys
from settings import *
import time
from connect import connect

con = connect()
CON = con[0]
CUR = con[1]


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
    'hero': load_image('main_hero.png')
}

tile_width = tile_height = 50
player_x, player_y = 0, 0


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for inet in self:
            inet.get_event(event)


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


LEVELS_SP = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt', 'level6.txt', 'level7.txt',
             'level8.txt']
cur_stolb = LEVELS_SP[1]
cur_level = './levels_txt/' + cur_stolb
cur_stolb = cur_stolb[:cur_stolb.index('.')]
level = load_level(cur_level)
norm_level = []
for i in level:
    norm_level.append(''.join(i))

level = norm_level.copy()
norm_level.clear()


def generate_level(level):
    new_player = None

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
                global player_x, player_y
                player_x, player_y = x, y  # нач коорд
    return new_player


font = pygame.font.Font(None, 74)
start_time = time.time()


def timer():
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = f"{minutes}:{seconds}"
    time.sleep(0.1)
    return time_text, minutes, seconds


def get_user(username):
    global user
    user = username


def run_game_py():
    running = True
    level_map = load_level(cur_level)
    hero = generate_level(level_map)

    cur_record = CUR.execute(f"SELECT {cur_stolb} FROM login WHERE username = '{user}'").fetchall()
    cur_record = cur_record[0][0]
    cur_record_min = ''
    cur_record_sec = ''
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
                    # print(player_x, player_y)
                elif event.key == pygame.K_DOWN:
                    hero.move(0, 1)
                    # print(player_x, player_y)
                elif event.key == pygame.K_LEFT:
                    hero.move(-1, 0)
                    # print(player_x, player_y)
                elif event.key == pygame.K_RIGHT:
                    hero.move(1, 0)
                    # print(player_x, player_y)

        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)
        sprite_group.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
        time = timer()
        if cur_record and level_map[player_y][player_x] == '*':
            new_minutes = int(time[1])
            new_seconds = int(time[2])
            if new_minutes < cur_record_min or (new_seconds < cur_record_sec and new_minutes == cur_record_min):
                print('wdqwd')
                CUR.execute(f"UPDATE login SET {cur_stolb} = '{time[0]}' WHERE username = '{user}'")
                CON.commit()
                ranning = False
        elif level_map[player_y][player_x] == '*':
            CUR.execute(f"UPDATE login SET {cur_stolb} = '{time[0]}' WHERE username = '{user}'")
            print('asasd')
            CON.commit()
            running = False

    terminate()
