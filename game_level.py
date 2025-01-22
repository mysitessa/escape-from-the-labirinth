from settings import *
import sys
get_config()

if __name__ == '__main__':
    while True:
        start_app()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
