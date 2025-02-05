import pygame.event
import sqlite3

from settings import *
import sys
from connect import connect

con = connect()
CON = con[0]
CUR = con[1]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (0, 0, 0)
get_config()
settings = start_app()
screen = settings[0]
FPS = settings[1]
pygame.init()
username_for_game = ''
from start_window import run_menu


def terminate():
    pygame.quit()
    sys.exit()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BackGround = Background('./image/BackGround_login.jpg', [0, 0])


class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.font = pygame.font.Font(None, 32)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, surface):
        # Отрисовка поля ввода
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, FONT_COLOR)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = FONT_COLOR
        self.font = pygame.font.Font(None, 32)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))
        f1 = pygame.font.Font(None, 50)
        text1 = f1.render('MONSTER_HUNTER', True,
                          (0, 128, 128))
        surface.blit(text1, (300, 50))
        f2 = pygame.font.Font(None, 36)
        text2 = f2.render('Войдите или зарегестрируйтесь', True, WHITE)
        surface.blit(text2, (300, 20))
        f3 = pygame.font.Font(None, 36)
        text3 = f3.render("пароль:", True, WHITE)
        surface.blit(text3, (1, 162))
        text4 = f3.render("логин:", True, WHITE)
        surface.blit(text4, (1, 110))


class Osnova:
    def __init__(self):

        self.screen = screen
        pygame.display.set_caption("Вход и Регистрация")

        # Создание объектов
        self.input_box_user = InputBox(100, 100, 400, 40)
        self.input_box_pass = InputBox(100, 150, 400, 40)
        self.button_login = Button(100, 200, 80, 32, "Вход")
        self.button_register = Button(220, 200, 150, 32, "Регистрация")
        self.password_vhod = self.input_box_pass.text
        self.user_vhod = self.input_box_user.text

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_register.rect.collidepoint(event.pos):
                        app = Registration()
                        app.run()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_login.rect.collidepoint(event.pos):
                        self.password_vhod = self.input_box_pass.text
                        self.user_vhod = self.input_box_user.text
                        if self.password_vhod and self.user_vhod:
                            self.log_in()

                # Обработка событий для полей ввода
                self.input_box_user.event(event)
                self.input_box_pass.event(event)

            # Отрисовка элементов
            screen.fill([255, 255, 255])
            screen.blit(BackGround.image, BackGround.rect)
            self.input_box_user.draw(self.screen)
            self.input_box_pass.draw(self.screen)
            self.button_login.draw(self.screen)
            self.button_register.draw(self.screen)

            pygame.display.flip()

    def log_in(self):
        try:
            username_bd = CUR.execute(f"SELECT password FROM login WHERE username = '{self.user_vhod}'").fetchall()
            if username_bd[0][0] == self.password_vhod:
                run_menu(self.user_vhod)
                terminate()
        except Exception:
            f5 = pygame.font.Font(None, 36)
            text5 = f5.render("неправильный пароль или логин", True, (255, 0, 0))
            screen.blit(text5, (100, 400))


class Registration:
    def __init__(self):
        pygame.init()
        self.screen = screen
        pygame.display.set_caption("Регистрация")

        # Создание объектов
        self.input_box_user = InputBox(100, 100, 400, 40)
        self.input_box_pass = InputBox(100, 150, 400, 40)
        self.button_register = Button(220, 200, 150, 32, "Регистрация")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_register.rect.collidepoint(event.pos):
                        self.password = self.input_box_pass.text
                        self.user = self.input_box_user.text
                        self.reg()

                # Обработка событий для полей ввода
                self.input_box_user.event(event)
                self.input_box_pass.event(event)

            # Отрисовка элементов
            screen.fill([255, 255, 255])
            screen.blit(BackGround.image, BackGround.rect)
            self.input_box_user.draw(self.screen)
            self.input_box_pass.draw(self.screen)
            self.button_register.draw(self.screen)

            pygame.display.flip()

    def reg(self):
        if self.user and self.password:
            CUR.execute(f"INSERT INTO login(password, username) VALUES('{self.password}', '{self.user}')")
            CON.commit()
            run_menu(self.user)
            terminate()
        else:
            print('ER')


def start_game():
    app = Osnova()
    app.run()
