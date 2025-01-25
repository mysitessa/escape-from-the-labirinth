from settings import *
import pygame_menu
import login_window

WHITE = (255, 255, 255)

get_config()
settings = start_app()
screen = settings[0]
FPS = settings[1]


def return_login():
    login_window.start_game()


def run_menu():
    running = True
    theme = pygame_menu.themes.THEME_BLUE.copy()
    background = pygame_menu.baseimage.BaseImage("./image/BackGround_login.jpg")
    theme.background_color = background
    menu = pygame_menu.Menu('MONSTER_HUNTER', 900, 700,
                            theme=theme)

    menu.add.text_input('Имя:', default='')
    menu.add.button('Играть')
    menu.add.button('Сменить аккаунт', return_login)

    while running:
        clock = pygame.time.Clock()
        running = True
        menu.mainloop(screen)
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
