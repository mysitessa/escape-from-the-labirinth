from settings import *
import pygame_menu
import login_window

WHITE = (255, 255, 255)

get_config()
settings = start_app()
screen = settings[0]
FPS = settings[1]


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround = Background('./image/BackGround_login.jpg', [0, 0])


def return_login():
    login_window.start_game()


def start_game():
    running = True
    menu = pygame_menu.Menu('Welcome', 900, 700,
                            theme=pygame_menu.themes.THEME_BLUE)

    menu.add.text_input('Имя:', default='')
    menu.add.button('Играть')
    menu.add.button('Сменить аккаунт', return_login)

    while running:
        clock = pygame.time.Clock()
        running = True

        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)
        menu.mainloop(screen)
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
