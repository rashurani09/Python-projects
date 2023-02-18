import pygame
import math
from queue import PriorityQueue

# Define colors for visualization
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Define the size of the grid and the size of each grid square
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")
ROWS = 50
SQUARE_SIZE = WIDTH // ROWS

# Define node class for each square in the grid
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * SQUARE_SIZE
        self.y = col * SQUARE_SIZE
        self.color = WHITE
        self.neighbors = []
        self.parent = None
        self.f = 0
        self.g = 0
        self.h = 0

    # Define methods to get the position of the node
    def get_pos(self):
        return self.row, self.col

    # Define methods to check if the node has been closed
    def is_closed(self):
        return self.color == RED

    # Define methods to check if the node is open
    def is_open(self):
        return self.color == GREEN

    # Define methods to check if the node is a barrier
    def is_barrier(self):
        return self.color == BLACK

    # Define methods to check if the node is the start node
    def is_start(self):
        return self.color == ORANGE

    # Define methods to check if the node is the end node
    def is_end(self):
        return self.color == TURQUOISE

    # Define method to reset the node to its default color
    def reset(self):
        self.color = WHITE

    # Define method to make the node a barrier
    def make_barrier(self):
        self.color = BLACK

    # Define method to make the node the start node
    def make_start(self):
        self.color = ORANGE

    # Define method to make the node the end node
    def make_end(self):
        self.color = TURQUOISE

    # Define method to make the node closed
    def make_closed(self):
        self.color = RED

    # Define method to make the node open
    def make_open(self):
        self.color = GREEN

    # Define method to make the node a path node
    def make_path(self):
        self.color = PURPLE

    # Define method to draw the node on the grid
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))

    # Define method to update the node's neighbors
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier(): # Check above
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    # Define method to compare two nodes
    def __lt__(self, other):
        return False

# Define heuristic function to calculate the distance between two points
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Define function to reconstruct the path from the end node to the start node
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# Define function to implement the A* algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

# Define function to initialize the grid
def make_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node = Node(i, j)
            grid[i].append(node)
    return grid

# Define function to draw the grid lines
def draw_grid(win):
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE))
        for j in range(ROWS):
            pygame.draw.line(win, GREY, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, WIDTH))

# Define function to draw the nodes on the grid
def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win)
    pygame.display.update()

# Define function to get the clicked position in the grid
def get_clicked_pos(pos):
    row, col = pos
    row //= SQUARE_SIZE
    col //= SQUARE_SIZE
    return row, col

# Define main function to implement the pathfinding visualization
def main(win, width):
    grid = make_grid()

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid()

    pygame.quit()

# Call main function to start the visualization
main(WIN, WIDTH)



