import pygame
import random
import time

pygame.init()

# screen settings
WIDTH = 600
HEIGHT = 600
ROWS = 20
COLS = 20
CELL_SIZE = WIDTH // COLS
WHITE = (255,255,255)
BLACK = (0, 0, 0)


DIRECTIONS = {
    "up": (0,-1),
    "down": (0, 1),
    "left": (-1, 0),
    "right":(1, 0)
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("laberinto")

# grid is a list of dictionaries
grid = []
for y in range(ROWS):
    row = []
    for x in range(COLS):
        cell = {"visited": False, "walls": {"up": True, "down": True, "left": True, "right": True}}
        row.append(cell)
    grid.append(row)



def draw_cell(x, y, walls):
    # draw the cell with its walls
    cell_x = x * CELL_SIZE
    cell_y = y * CELL_SIZE
    if walls["up"]:
        pygame.draw.line(screen, WHITE, (cell_x, cell_y), (cell_x + CELL_SIZE, cell_y), 2)
    if walls["down"]:
        pygame.draw.line(screen, WHITE, (cell_x, cell_y + CELL_SIZE), (cell_x + CELL_SIZE, cell_y + CELL_SIZE), 2)
    if walls["left"]:
        pygame.draw.line(screen, WHITE, (cell_x, cell_y), (cell_x, cell_y + CELL_SIZE), 2)
    if walls["right"]:
        pygame.draw.line(screen, WHITE, (cell_x + CELL_SIZE, cell_y), (cell_x + CELL_SIZE, cell_y + CELL_SIZE), 2)

def generate_maze(x, y):
    grid[y][x]["visited"] = True
    directions = list(DIRECTIONS.keys())
    random.shuffle(directions) #randomize direction order

    for direction in directions:
        # d for direction n for neighbour
        dx, dy = DIRECTIONS[direction]
        nx = x + dx
        ny = y + dy

        # check if the neighbour is unvisited and in the grid
        if 0 <= nx < COLS and 0 <= ny < ROWS and not grid[ny][nx]["visited"]:
            # remove the wall between current cell and neighbour
            grid[y][x]["walls"][direction] = False
            opposite = {"up":"down", "down":"up", "left":"right", "right":"left"}
            grid[ny][nx]["walls"][opposite[direction]] = False

            # recursion to generate maze from the neighbor
            generate_maze(nx, ny)


def draw_maze():
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            draw_cell(x, y, grid[y][x]["walls"])
    pygame.display.flip()


def main():
    generate_maze(0, 0)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze()

    pygame.quit()


if __name__ == "__main__":
    main()