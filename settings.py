import pygame


def get_config():  # Считывает настройки из файла config
    with open('config.cfg', 'r') as f:
        settings = []
        for i in f.read().split('\n'):
            i = i.split(' = ')
            settings.append(int(i[1]))
        return settings


def start_app():
    pygame.init()  # Установка начальных настроек и инициализация pygame
    settings = get_config()
    size = width, height = settings[0], settings[1]
    FPS = settings[2]
    screen = pygame.display.set_mode(size)
    return screen, FPS


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)  # Загрузка изображения
        self.rect = self.image.get_rect()  # Получение прямоугольника изображения
        self.rect.left, self.rect.top = location  # Установка позиции
