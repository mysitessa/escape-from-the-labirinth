import pygame

FPS = 30
size = width, height = 800, 700
WHITE = (255, 255, 255)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 60


    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, WHITE,
                                 (self.left + self.cell_size * x,
                                  self.top + self.cell_size * y,
                                  self.cell_size, self.cell_size), 1)


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    b = Board(10, 10)

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
        b.render(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
