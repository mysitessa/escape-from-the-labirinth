from settings import *  # Импорт настроек игры
import sys  # Импорт модуля для работы с системными функциями
import sqlite3  # Импорт модуля для работы с базой данных SQLite

# Настройка заголовка окна
pygame.display.set_caption('escape-from-the-labirinth')

# Подключение к базе данных SQLite
CON = sqlite3.connect('Base_Date.sqlite')
CUR = CON.cursor()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (0, 0, 0)

# Получение конфигурации и настроек игры
get_config()
settings = start_app()
screen = settings[0]  # Экран игры
FPS = settings[1]  # Частота кадров

# Инициализация Pygame
pygame.init()

# Глобальная переменная для хранения имени пользователя
username_for_game = ''

# Импорт функции для запуска меню
from start_window import run_menu


# Функция для завершения работы программы
def terminate():
    pygame.quit()
    sys.exit()


# Создание фонового изображения
BackGround = Background('./image/BackGround_login.jpg', [0, 0])


# Класс для создания поля ввода
class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # Прямоугольник для поля ввода
        self.color_inactive = pygame.Color('lightskyblue3')  # Цвет неактивного поля
        self.color_active = pygame.Color('dodgerblue2')  # Цвет активного поля
        self.color = self.color_inactive  # Текущий цвет поля
        self.active = False  # Флаг активности поля
        self.text = ''  # Текст в поле
        self.font = pygame.font.Font(None, 32)  # Шрифт для текста

    # Обработка событий для поля ввода
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):  # Проверка клика на поле
                self.active = not self.active  # Переключение активности
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive  # Изменение цвета

        if event.type == pygame.KEYDOWN and self.active:  # Обработка ввода текста
            if event.key == pygame.K_RETURN:  # Очистка поля при нажатии Enter
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:  # Удаление символа при нажатии Backspace
                self.text = self.text[:-1]
            else:
                self.text += event.unicode  # Добавление символа

    # Отрисовка поля ввода
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)  # Отрисовка прямоугольника
        text_surface = self.font.render(self.text, True, FONT_COLOR)  # Отрисовка текста
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))


# Класс для создания кнопок
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)  # Прямоугольник для кнопки
        self.color = FONT_COLOR  # Цвет кнопки
        self.font = pygame.font.Font(None, 32)  # Шрифт для текста
        self.text = text  # Текст кнопки

    # Отрисовка кнопки на экране завершения уровня
    def draw_level_end(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)  # Отрисовка прямоугольника
        text_surface = self.font.render(self.text, True, WHITE)  # Отрисовка текста
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))

    # Отрисовка кнопки
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)  # Отрисовка прямоугольника
        text_surface = self.font.render(self.text, True, WHITE)  # Отрисовка текста
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))

        # Отрисовка дополнительных текстовых элементов
        f1 = pygame.font.Font(None, 50)
        text1 = f1.render('escape-from-the-labirinth', True, (0, 128, 128))
        surface.blit(text1, (300, 50))
        f2 = pygame.font.Font(None, 36)
        text2 = f2.render('Войдите или зарегестрируйтесь', True, WHITE)
        surface.blit(text2, (300, 20))
        f3 = pygame.font.Font(None, 36)
        text3 = f3.render("пароль:", True, WHITE)
        surface.blit(text3, (1, 162))
        text4 = f3.render("логин:", True, WHITE)
        surface.blit(text4, (1, 110))


# Основной класс для окна авторизации
class Osnova:
    def __init__(self):
        self.screen = screen

        # Создание объектов
        self.input_box_user = InputBox(100, 100, 400, 40)  # Поле для ввода логина
        self.input_box_pass = InputBox(100, 150, 400, 40)  # Поле для ввода пароля
        self.button_login = Button(100, 200, 80, 32, "Вход")  # Кнопка входа
        self.button_register = Button(220, 200, 150, 32, "Регистрация")  # Кнопка регистрации
        self.password_vhod = self.input_box_pass.text  # Текст пароля
        self.user_vhod = self.input_box_user.text  # Текст логина

    # Основной цикл окна авторизации
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Обработка закрытия окна
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_register.rect.collidepoint(event.pos):  # Обработка нажатия на кнопку регистрации
                        app = Registration()
                        app.run()
                        terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_login.rect.collidepoint(event.pos):  # Обработка нажатия на кнопку входа
                        self.password_vhod = self.input_box_pass.text
                        self.user_vhod = self.input_box_user.text
                        if self.password_vhod and self.user_vhod:  # Проверка заполненности полей
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

            pygame.display.flip()  # Обновление экрана

    # Функция для входа в систему
    def log_in(self):
        try:
            # Проверка логина и пароля в базе данных
            username_bd = CUR.execute(f"SELECT password FROM login WHERE username = '{self.user_vhod}'").fetchall()
            if username_bd[0][0] == self.password_vhod:  # Если пароль совпадает
                run_menu(self.user_vhod)  # Запуск меню
                terminate()  # Завершение работы
        except Exception:
            pass  # Обработка ошибок


# Класс для окна регистрации
class Registration:
    def __init__(self):
        pygame.init()
        self.screen = screen

        # Создание объектов
        self.input_box_user = InputBox(100, 100, 400, 40)  # Поле для ввода логина
        self.input_box_pass = InputBox(100, 150, 400, 40)  # Поле для ввода пароля
        self.button_register = Button(220, 200, 150, 32, "Регистрация")  # Кнопка регистрации
        self.nazad_login = Button(10, 50, 80, 32, "Назад")  # Кнопка возврата
        self.surface = pygame.Surface((400, 20))  # Поверхность для текста

    # Основной цикл окна регистрации
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Обработка закрытия окна
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_register.rect.collidepoint(event.pos):  # Обработка нажатия на кнопку регистрации
                        self.password = self.input_box_pass.text
                        self.user = self.input_box_user.text
                        self.reg()  # Вызов функции регистрации
                    if self.nazad_login.rect.collidepoint(event.pos):  # Обработка нажатия на кнопку возврата
                        app = Osnova()
                        app.run()
                        terminate()

                # Обработка событий для полей ввода
                self.input_box_user.event(event)
                self.input_box_pass.event(event)

            # Отрисовка элементов
            screen.fill([255, 255, 255])
            screen.blit(BackGround.image, BackGround.rect)
            self.input_box_user.draw(self.screen)
            self.input_box_pass.draw(self.screen)
            self.button_register.draw(self.screen)
            self.nazad_login.draw(self.screen)

            pygame.display.flip()  # Обновление экрана

    # Функция для регистрации нового пользователя
    def reg(self):
        # Проверка существования пользователя
        us_check = CUR.execute(f"SELECT username FROM login WHERE username = '{self.user}'").fetchall()
        if us_check:  # Если пользователь уже существует
            pass
        elif self.user and self.password:  # Если поля заполнены
            # Добавление нового пользователя в базу данных
            CUR.execute(f"INSERT INTO login(password, username) VALUES('{self.password}', '{self.user}')")
            CON.commit()  # Сохранение изменений
            run_menu(self.user)  # Запуск меню
            terminate()  # Завершение работы


# Функция для запуска окна авторизации
def start_game():
    app = Osnova()
    app.run()
