import sys

from settings import *  # Импорт настроек игры
import pygame_menu  # Импорт библиотеки для создания меню
import login_window  # Импорт модуля для окна авторизации
from game import get_user, show_levels  # Импорт функций из модуля игры

# Константа для белого цвета
WHITE = (255, 255, 255)

# Получение конфигурации и настроек игры
get_config()
settings = start_app()
screen = settings[0]  # Экран игры
FPS = settings[1]  # Частота кадров


# Функция для возврата к окну авторизации
def return_login():
    login_window.start_game()  # Запуск окна авторизации
    pygame.quit()  # Завершение работы Pygame
    sys.exit()  # Выход из программы


# Основная функция для запуска меню
def run_menu(username):
    running = True  # Флаг для работы основного цикла
    theme = pygame_menu.themes.THEME_BLUE.copy()  # Создание темы для меню
    background = pygame_menu.baseimage.BaseImage("./image/BackGround_login.jpg")  # Загрузка фонового изображения
    theme.background_color = background  # Установка фона для темы

    # Создание меню с заголовком и размерами
    menu = pygame_menu.Menu('escape-from-the-labirinth', 900, 700, theme=theme)

    get_user(username)  # Сохранение имени пользователя
    menu.add.button('К уровням', show_levels)  # Добавление кнопки для перехода к уровням
    menu.add.button('Сменить аккаунт', return_login)  # Добавление кнопки для смены аккаунта

    # Основной цикл меню
    while running:
        running = True
        menu.mainloop(screen)  # Запуск основного цикла меню
        for event in pygame.event.get():
            # При закрытии окна
            if event.type == pygame.QUIT:
                running = False  # Остановка цикла
        pygame.display.flip()  # Обновление экрана
    pygame.quit()  # Завершение работы Pygame
