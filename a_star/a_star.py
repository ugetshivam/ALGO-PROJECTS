# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 13:49:14 2021

@author: Shivam
"""

import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
NEON = (57,255,20)
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_obstacle(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    def make_start(self):
        self.color  = ORANGE
    def is_end(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color = WHITE
    
    def make_closed(self):
        self.color = RED
        
    def make_open(self):
        self.color = GREEN
    
    def make_obstacle(self):
        self.color = BLACK
        
    def make_end(self):
        self.color = NEON
    
    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        #SOUTH
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col])
        #NORTH
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col]) 
        #EAST
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])
        #WEST
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])
        #NORTH-EAST
        if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col + 1])
        #NORTH-WEST
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col - 1])
        #SOUTH-EAST
        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col + 1])
        #SOUTH-WEST
        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col - 1])
    def __lt__(self, other):
        return False
    
def calculate_h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    return math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))
def output_path(parents, end, draw):
    while end in parents:
        end = parents[end]
        end.make_path()
        draw()


def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = calculate_h(start.get_pos(), end.get_pos())
    
    closed_set = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        closed_set.remove(current)
        
        if current == end:
            output_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            gNew = g_score[current] + 1
            
            if gNew < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = gNew
                f_score[neighbor] = gNew + calculate_h(neighbor.get_pos(), end.get_pos())
                if neighbor not in closed_set:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    closed_set.add(neighbor)
                    neighbor.make_open()
                
        draw()
        
        if current != start:
            current.make_closed()
    return False
        
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
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
    
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]: #left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_obstacle()
            elif pygame.mouse.get_pressed()[2]: #right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                    
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                       for node in row:
                           node.update_neighbors(grid)
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()
main(WIN, WIDTH)
    
        
    
    
