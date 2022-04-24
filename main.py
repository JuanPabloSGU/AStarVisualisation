import pygame                                           # PyGame Install
from queue import PriorityQueue                         # Priority Queue used for Alogrithm

from tkinter import *
from tkinter import messagebox                          # Display Message Boxes

WIDTH = 400                                             # Window Width
WIN = pygame.display.set_mode((WIDTH, WIDTH))           # Set Canvas Sizing
pygame.display.set_caption("Path Finding")              # Set Window Caption

# Colours Used
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, num_rows):
        self.row = row                                  # Node Row
        self.col = col                                  # Node Col
        self.x = row * width                            # X Position on Grid
        self.y = col * width                            # Y Position on Grid
        self.color = WHITE                              # Default Colour
        self.neighbors = []                             # List of Neighbors
        self.width = width                              # Node Width
        self.num_rows = num_rows                        # Number of Rows

    def get_pos(self):                                  # Get Position on Grid
        return self.row, self.col

    def is_visited(self):                               
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = GREEN

    def make_start(self):
        self.color = ORANGE

    def make_visited(self):
        self.color = GREY

    def make_open(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        x = self.row
        y = self.col

        # UP
        if x > 0 and not grid[x - 1][y].is_barrier():
            self.neighbors.append(grid[x - 1][y])

        # DOWN
        if x < self.num_rows - 1 and not grid[x + 1][y].is_barrier():
            self.neighbors.append(grid[x + 1][y])

        # LEFT
        if y > 0 and not grid[x][y - 1].is_barrier():
            self.neighbors.append(grid[x][y - 1])

        # RIGHT
        if y < self.num_rows - 1 and not grid[x][y + 1].is_barrier():
            self.neighbors.append(grid[x][y + 1])

    def __lt__(self, other):
        return False

def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)                      # Manhattan Distance / Taxicab geometry

def reconstruct_path(visited_nodes, current, render):           # Recontruct the path when the algoritm
    while current in visited_nodes:                             # Loop through the nodes that were visited
        current = visited_nodes[current]                        # Index the Current Node in List
        current.make_path()                                     # Change Color
        render()                                                # Re-render Grid
    

def AStar(render, grid, start, end):                                                # AStar Path Finding Algorithm
    count = 0                                                                       # Distance / Weight since we are using a Grid Format 
    open_set = PriorityQueue()                                                      # Priority Queue Implementation

    open_set.put((0, count, start))                                                 # Input Start Node

    visited_nodes = {}                                                              # Dictionary of Visited Nodes

    g_score = {node: float("inf") for row in grid for node in row}                  # Set all nodes to Infinity - current shorest Path
    g_score[start] = 0                                                              # Since we start at this position is 0
    
    f_score = {node: float("inf") for row in grid for node in row}                  # Set all (weights / distance) to each node to Infinity
    f_score[start] = heuristic(start.get_pos(), end.get_pos())                      # Since we start at this position is 0
    
    open_set_hash = {start}                                                         # Helper for open_set since it is not indexable

    while not open_set.empty():
        for event in pygame.event.get():                                            # Loop needs to be exitied
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]                                                 # Get the current Node in the Priority Queue that has the shortest distance
        open_set_hash.remove(current)                                               # Since we do not need this index anymore

        if current == end:                                                          # Found End
            reconstruct_path(visited_nodes, end, render)                            # Reconstruct Path 
            end.make_end()                                                          # Recolour after path has been completed
            start.make_start()                                                      # Recolour after path has been completed
            return True
        
        for neighbor in current.neighbors:                                          # Go through all neighbors the current node has
            temp_g_score = g_score[current] + 1                                     # Calculated

            if temp_g_score < g_score[neighbor]:                                    # Compare less than
                visited_nodes[neighbor] = current                                   # Update visited nodes
                g_score[neighbor] = temp_g_score                                    # Update with Score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())     # Update with new heuristic

                if neighbor not in open_set_hash:                                   # If not found in the helper set
                    count += 1                                                      # Update distance
                    open_set.put((f_score[neighbor], count, neighbor))              # Update open_set
                    open_set_hash.add(neighbor)                                     # Update helper set
                    neighbor.make_open()                                            # Recolor to possible position

        render()                                                                    # Re-render Screen

        if current != start:                                                        # Does not pass through start Node
            current = current.make_closed()                                         # Close node

    return False                                                                    # Not able to find path to end node

def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)  

    return grid

def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def render(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    
    pygame.display.update()

def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    
    run = True

    Tk().wm_withdraw()

    howTo = "Controls\nMouse 1 : Place Block\nMouse 2 : Remove Block\nKey 'c' : Reset Board\nKey 'Space' : Start Visualisation\n\nEnjoy"

    messagebox.showinfo('How To Use', howTo)

    while run:

        render(win, grid, ROWS, width)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
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
                row, col = get_mouse_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None

                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    result = AStar(lambda: render(win, grid, ROWS, width), grid, start, end)

                    if result:
                        Tk().wm_withdraw()
                        messagebox.showinfo("Program Finished", "Shortest Path has been displayed")
                    else:
                        Tk().wm_withdraw()
                        messagebox.showinfo("Program Finished", "There is no Shortest Path")

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
 
    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)