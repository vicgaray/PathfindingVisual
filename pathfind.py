"""
Pathfinder Class

Run the board, scan the board using the algorithm chosen by the user.
"""
import math
import pygame
import random

from utils import PriorityQue


class Pathfinder():
    RED = (255,0,0)
    BLUE = (0,0,255)
    PINK = (245,164,212)
    GREY = (157,161,158)
    GREEN = (33,235,80)
    LIGHT_BLUE = (119,226,247)

    def __init__(self, grid, screen):
        self.start_pawn = None
        self.end_pawn = None
        self.grid = grid
        self.screen = screen
        self.walls = list()
        self.water = list()

        self.que = PriorityQue() # list

        self.end_pawn = random.choice(self.grid)
        self.start_pawn = self.assign_start_pawn_location()

        self.color_single_cell(self.RED, self.end_pawn[0], self.end_pawn[1])
        self.color_single_cell(self.BLUE, self.start_pawn[0], self.start_pawn[1])

    def assign_start_pawn_location(self):
        """Picks a location for start pawn."""
        while True:
            start = random.choice(self.grid)

            if start != self.end_pawn:
                return start

    def color_single_cell(self, color, x, y):
        """Draws a perfect cell on the grid."""
        pygame.draw.rect(self.screen, color, (x + 1, y + 1, 18, 18), 0)
        pygame.display.update()

    def get_neighbors(self, node):
        """Get all the neighbor cells for a specific node."""
        neighbors = list()

        if not node in self.walls:
            if node[0] - 20 >= 50:
                neighbors.append((node[0] - 20, node[1])) # checks the left neighbor node
            if node[0] + 20 <= 430:
                neighbors.append((node[0] + 20, node[1])) # checks the right neighbor node
            if node[1] - 20 >= 20:
                neighbors.append((node[0], node[1] - 20)) # checks the upward neighbor node
            if node[1] + 20 <= 400:
                neighbors.append((node[0], node[1] + 20)) # checks the downward neighbor node

        return neighbors

    def reconstructed_path(self, came_from):
        """Rebuilds the path of the dictionary."""
        path = list()
        current = self.end_pawn

        while current != self.start_pawn: # Checks if the node is start pawn
            path.append(current)
            current = came_from[current] # Gets the previous node it came from

        path.append(self.start_pawn)
        path.reverse()

        if path[0] == self.start_pawn:
            if self.water:
                for aqua in self.water: # Re-color the water
                    self.color_single_cell(self.LIGHT_BLUE, aqua[0], aqua[1])

            for node in path: # Color the most efficient path
                if node != self.start_pawn and node != self.end_pawn:
                    self.color_single_cell(self.GREEN, node[0], node[1])

    def bfs(self):
        """Runs the Breadth First Search, rebuilds path when end location found."""
        q = list() # Que list
        q.append(self.start_pawn)

        came_from = dict() # Dict holding the node and it's previous node
        came_from[self.start_pawn] = None

        while q:
            ev = pygame.event.poll() # will cancel loop
            if ev.type == pygame.QUIT or ev.type == pygame.KEYDOWN:
                break

            current_node = q.pop(0) # Deque the first node

            if current_node == self.end_pawn:
                self.reconstructed_path(came_from)
                break

            if current_node != self.start_pawn and not current_node in self.walls:
                self.color_single_cell(self.GREY, current_node[0], current_node[1])

            for next_node in self.get_neighbors(current_node):
                if not next_node in came_from: # Adds the node to the que
                    q.append(next_node)
                    came_from[next_node] = current_node

                    if next_node != self.end_pawn and not next_node in self.walls:
                        self.color_single_cell(self.PINK, next_node[0], next_node[1])

    def dijkstra(self):
        """Runs the Dijkstra search, rebuilds path when end location found."""
        self.que.enque(self.start_pawn, 0) # Priority que adds to que

        came_from = dict() # Dict holding the node and it's pervious node
        cost_so_far = dict() # Dict holding the node and it's cost to get there
        came_from[self.start_pawn] = None
        cost_so_far[self.start_pawn] = 0

        while self.que.wait_list:
            ev = pygame.event.poll() # will cancel loop
            if ev.type == pygame.QUIT or ev.type == pygame.KEYDOWN:
                break

            current_node = self.que.deque() # gets the lowest costly node

            if current_node == self.end_pawn:
                self.reconstructed_path(came_from)
                break

            if current_node != self.start_pawn and not current_node in self.walls:
                self.color_single_cell(self.GREY, current_node[0], current_node[1])

            for next_node in self.get_neighbors(current_node):
                if next_node in self.water: # Set the cost of getting to the node
                    new_cost = cost_so_far[current_node] + 70
                else:
                    new_cost = cost_so_far[current_node] + 20

                if not next_node in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost # Save the node and its new cost
                    self.que.enque(next_node, new_cost)
                    came_from[next_node] = current_node

                    if next_node != self.end_pawn and not next_node in self.walls:
                        self.color_single_cell(self.PINK, next_node[0], next_node[1])

    def heuristic(self, node):
        """Uses the manhattan distance of target pawn and node."""
        #return math.sqrt((self.end_pawn[0] - node[0])**2 + (self.end_pawn[1] - node[1])**2)
        return abs(node[0] - self.end_pawn[0]) + abs(node[1] - self.end_pawn[1]) # |x1 - x2| + |y1 - y2|

    def greedy(self):
        """Runs the greedy search, rebuilds path when end location found."""
        self.que.enque(self.start_pawn, 0) # Priority que adds to que

        came_from = dict() # Dict holding the node and it's pervious node
        came_from[self.start_pawn] = None

        while self.que.wait_list:
            ev = pygame.event.poll() # will cancel loop
            if ev.type == pygame.QUIT or ev.type == pygame.KEYDOWN:
                break

            current_node = self.que.deque() # gets the lowest costly node, returns a sublist [(grid loc), cost]

            if current_node == self.end_pawn:
                self.reconstructed_path(came_from)
                break

            if current_node != self.start_pawn and not current_node in self.walls:
                self.color_single_cell(self.GREY, current_node[0], current_node[1])

            for next_node in self.get_neighbors(current_node):
                if not next_node in came_from:
                    priority = self.heuristic(next_node) # Gets the manhattan distance
                    self.que.enque(next_node, priority)      # of the node.
                    came_from[next_node] = current_node

                    if next_node != self.end_pawn and not next_node in self.walls:
                        self.color_single_cell(self.PINK, next_node[0], next_node[1])

    def a_star(self):
        """Runs the A* search, rebuilds path when end location found."""
        self.que.enque(self.start_pawn, 0) # Priority que adds to que

        came_from = dict() # dict holding the node and it's pervious node
        cost_so_far = dict() # dict holding the node and it's cost to get there
        came_from[self.start_pawn] = None
        cost_so_far[self.start_pawn] = 0

        while self.que.wait_list:
            ev = pygame.event.poll() # will cancel loop
            if ev.type == pygame.QUIT or ev.type == pygame.KEYDOWN:
                break

            current_node = self.que.deque() # Gets lowest costly node

            if current_node == self.end_pawn:
                self.reconstructed_path(came_from)
                break

            if current_node != self.start_pawn and not current_node in self.walls:
                self.color_single_cell(self.GREY, current_node[0], current_node[1])

            for next_node in self.get_neighbors(current_node):
                if next_node in self.water: # Sets the cost of getting to the node
                    new_cost = cost_so_far[current_node] + 70
                else:
                    new_cost = cost_so_far[current_node] + 20

                if not next_node in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost # Save the new cost of node
                    priority = new_cost + self.heuristic(next_node) # Will combine cost and manhattan distance of that node
                    self.que.enque(next_node, priority)
                    came_from[next_node] = current_node

                    if next_node != self.end_pawn and not next_node in self.walls:
                        self.color_single_cell(self.PINK, next_node[0], next_node[1])
