import pygame

size = 800
rows = 20


def grid(window, size, rows):
    distance_between_rows = size // rows
    x = 0
    y = 0
    for i in range(rows):
        x += distance_between_rows
        y += distance_between_rows
        pygame.draw.line(window, (0, 0, 0), (x, 0), (x, size))
        pygame.draw.line(window, (0, 0, 0), (0, y), (size, y))


def redraw(window):
    window.fill((255, 255, 255))
    grid(window, size, rows)
    pygame.display.update()


def main():
    window = pygame.display.set_mode((size, size))
    play = True

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        redraw(window)


if __name__ == '__main__':
    main()
