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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
CELESTE = (83, 195, 189)

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



def draw_cell(x, y, walls, current=False, exit=False):
    # draw the cell with its walls
    cell_x = x * CELL_SIZE
    cell_y = y * CELL_SIZE
    if exit:
        pygame.draw.rect(screen, RED, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
    elif current:
        pygame.draw.rect(screen, GREEN, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
    if walls["up"]:
        pygame.draw.line(screen, WHITE, (cell_x, cell_y), (cell_x + CELL_SIZE, cell_y), 2)
    if walls["down"]:
        pygame.draw.line(screen, WHITE, (cell_x, cell_y + CELL_SIZE), (cell_x + CELL_SIZE, cell_y + CELL_SIZE), 2)
    if walls["left"]:
        pygame.draw.line(screen, WHITE, (cell_x, cell_y), (cell_x, cell_y + CELL_SIZE), 2)
    if walls["right"]:
        pygame.draw.line(screen, WHITE, (cell_x + CELL_SIZE, cell_y), (cell_x + CELL_SIZE, cell_y + CELL_SIZE), 2)

def place_exit():
    dirs = ["top", "bottom", "left", "right"]
    edge = random.choice(dirs)

    if edge == "top":
        x = random.randint(0, COLS - 1)
        y = 0
    elif edge == "bottom":
        x = random.randint(0, COLS - 1)
        y = ROWS - 1
    elif edge == "left":
        x = 0
        y = random.randint(0, ROWS - 1)
    elif edge == "right":
        x = COLS - 1
        y = random.randint(0, ROWS - 1)

    if edge in ["top", "bottom"]:
        grid[y][x]["walls"][edge] = False
    else:
        grid[y][x]["walls"][edge] = True
    
    return x, y

def generate_maze(x, y):
    grid[y][x]["visited"] = True
    if x == 0 and y == 0:
        grid[y][x]["walls"]["left"] = False
    draw_maze(x, y)
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


def draw_maze(current_x=None, current_y=None, exit_x=None, exit_y=None):
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):

            if x == current_x and y == current_y:
                current = True
            else:
                current = False        

            if x == exit_x and y == exit_y:
                exit = True
            else:
                exit = False
            
            draw_cell(x, y, grid[y][x]["walls"], current=current, exit=exit)

    for x in range(COLS):
        pygame.draw.line(screen, WHITE, (x * CELL_SIZE, HEIGHT - 1), ((x + 1) * CELL_SIZE, HEIGHT - 1), 2)
    for y in range(ROWS):
        pygame.draw.line(screen, WHITE, (WIDTH - 1, y * CELL_SIZE), (WIDTH - 1, (y + 1) * CELL_SIZE), 2)

    pygame.display.flip()
    if current_x != None:
        time.sleep(0.005)


def main():
    generate_maze(0, 0)

    exit_x, exit_y = place_exit()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze(current_x=0, current_y=0, exit_x=exit_x, exit_y=exit_y)

    pygame.quit()


if __name__ == "__main__":
    main()