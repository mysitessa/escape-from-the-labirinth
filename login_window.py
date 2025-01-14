from settings import *
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (0, 0, 0)
get_config()
settings = start_app()
screen = settings[0]
FPS = settings[1]


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
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, surface):
        # Отрисовка поля ввода
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, FONT_COLOR)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


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


class Osnova:
    def __init__(self):
        pygame.init()
        self.screen = screen
        pygame.display.set_caption("Вход и Регистрация")

        # Создание объектов
        self.input_box_user = InputBox(100, 100, 400, 40)
        self.input_box_pass = InputBox(100, 150, 400, 40)
        self.button_login = Button(100, 200, 80, 32, "Вход")
        self.button_register = Button(220, 200, 150, 32, "Регистрация")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Обработка событий для полей ввода
                self.input_box_user.event(event)
                self.input_box_pass.event(event)

            # Отрисовка элементов
            self.screen.fill(WHITE)
            self.input_box_user.draw(self.screen)
            self.input_box_pass.draw(self.screen)
            self.button_login.draw(self.screen)
            self.button_register.draw(self.screen)

            pygame.display.flip()


def start_game():
    app = Osnova()
    app.run()
