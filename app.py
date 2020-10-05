"""
Pathfinding App

GUI to visualize the different pathfinding algorithms: Breadth First Search, Dijkstra, Greedy BFS, and A*.
"""
import pygame
import random
import sys

from pathfind import Pathfinder
from utils import Button, get_cell_location


class App():
    RED = (255,0,0)
    BLUE = (0,0,255)
    PURPLE = (127,15,168)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    LIGHT_BLUE = (119,226,247)
    LIGHT_RED = (224,74,74)

    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 700

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pathfinder")

        self.grid = list() # grid coords

        self.clear_btn = Button(220, 470, 60, 30, "Clear", self.WHITE)

        self.bfs_btn = Button(10, 520, 60, 30, "BFS", self.WHITE)
        self.dijkstra_btn = Button(150, 520, 60, 30, "Dijkstra", self.WHITE)
        self.heap_btn = Button(290, 520, 60, 30, "Greedy", self.WHITE)
        self.a_star_btn = Button(430, 520, 60, 30, "A*", self.WHITE)

        self.terrain_btn = Button(10, 570, 20, 20, None, self.PURPLE)

        self.font = pygame.font.SysFont('comicsans', 20)

        self.setup()

    def setup(self):
        """Important feautures of the game. Used to reset board as well."""
        self.screen.fill(self.BLACK)
        self.create_grid(0, 20) # draws grid

        self.path = Pathfinder(self.grid, self.screen)

        self.draw_all_btns()

        pawn_instructions = self.font.render("BOTH PAWNS MUST BE ON BOARD BEFORE SEARCH", 1, self.WHITE)
        terrain_instructions = self.font.render("< CLICK BUTTON TO CHANGE TERRAIN", 1, self.WHITE)
        wall_instructions = self.font.render("purple = walls", 1, self.WHITE)
        water_instructions = self.font.render("light blue = water", 1, self.WHITE)
        draw_instructions = self.font.render("HOLD OR PRESS left click (draw terrain or pawns)", 1, self.WHITE)
        erase_instructions = self.font.render("HOLD OR PRESS right click (erase terrain or pawns)", 1, self.WHITE)

        self.screen.blit(pawn_instructions, (80, 440))
        self.screen.blit(terrain_instructions, (40, 570))
        self.screen.blit(wall_instructions, (10, 595))
        self.screen.blit(water_instructions, (10,610))
        self.screen.blit(draw_instructions, (150, 650))
        self.screen.blit(erase_instructions, (150, 665))

    def create_grid(self, y, w):
        """Creates the grid."""
        for i in range(1, 21):
            x = 50 # set x coord to start
            y += 20 # moves on to the new row

            for j in range(1, 21):
                pygame.draw.line(self.screen, self.WHITE, [x,y], [x + w, y]) # top of cell
                pygame.draw.line(self.screen, self.WHITE, [x + w, y], [x + w, y + w]) # right of cell
                pygame.draw.line(self.screen, self.WHITE, [x + w, y + w], [x, y + w]) # bottom of cell
                pygame.draw.line(self.screen, self.WHITE, [x, y + w], [x, y]) # left of cell

                self.grid.append((x,y))

                x += 20 # moves on to the new column

        pygame.display.update()

    def color_single_cell(self, color, x, y):
        """Colors in a perfect rect inbetween a grid cell."""
        pygame.draw.rect(self.screen, color, (x + 1, y + 1, 18, 18), 0)
        pygame.display.update()

    def draw_all_btns(self):
        """Draws all buttons being used."""
        self.clear_btn.draw_button(self.screen)
        self.bfs_btn.draw_button(self.screen)
        self.dijkstra_btn.draw_button(self.screen)
        self.heap_btn.draw_button(self.screen)
        self.a_star_btn.draw_button(self.screen)

        self.terrain_btn.draw_button(self.screen)

    def launch(self):
        """Main game loop."""
        clock = pygame.time.Clock()

        while True:

            self.draw_all_btns()
            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()

                if pygame.mouse.get_pressed() == (1,0,0):

                    if self.clear_btn.is_over(pos): # clear board
                        self.setup()

                    # Search path algorithm only if both pawns are on board.
                    if self.path.start_pawn and self.path.end_pawn:
                        if self.bfs_btn.is_over(pos):
                            self.path.bfs()

                        elif self.dijkstra_btn.is_over(pos):
                            self.path.dijkstra()

                        elif self.heap_btn.is_over(pos):
                            self.path.greedy()

                        elif self.a_star_btn.is_over(pos):
                            self.path.a_star()

                        elif self.terrain_btn.is_over(pos) and self.terrain_btn.color == self.PURPLE:
                            self.terrain_btn.color = self.LIGHT_BLUE

                        elif self.terrain_btn.is_over(pos) and self.terrain_btn.color == self.LIGHT_BLUE:
                            self.terrain_btn.color = self.PURPLE

                    # Left Click actions within the board
                    if pos[0] >= self.grid[0][0] and pos[0] <= self.grid[-1][0] + 20:
                        if pos[1] >= self.grid[0][1] and pos[1] <= self.grid[-1][1] + 20:

                            # Checks if start pawn and end pawn are on board.
                            # If not draw them next, they're the most prioritized
                            # then drawing walls or water.
                            wanted_cell = get_cell_location(pos)
                            if self.path.start_pawn and self.path.end_pawn:
                                if wanted_cell != self.path.start_pawn and wanted_cell != self.path.end_pawn:

                                    if self.terrain_btn.color == self.PURPLE and not wanted_cell in self.path.walls:
                                        self.path.walls.append(wanted_cell)
                                        self.color_single_cell(self.PURPLE, wanted_cell[0], wanted_cell[1])

                                    elif self.terrain_btn.color == self.LIGHT_BLUE and not wanted_cell in self.path.water:
                                        self.path.water.append(wanted_cell)
                                        self.color_single_cell(self.LIGHT_BLUE, wanted_cell[0], wanted_cell[1])
                            else:

                                if not self.path.start_pawn:
                                    self.path.start_pawn = wanted_cell
                                    self.color_single_cell(self.BLUE, wanted_cell[0], wanted_cell[1])

                                elif not self.path.end_pawn:
                                    self.path.end_pawn = wanted_cell
                                    self.color_single_cell(self.RED, wanted_cell[0], wanted_cell[1])


                if pygame.mouse.get_pressed() == (0,0,1):
                    # Righ Click commands within board
                    if pos[0] >= self.grid[0][0] and pos[0] <= self.grid[-1][0] + 20:
                        if pos[1] >= self.grid[0][1] and pos[1] <= self.grid[-1][1] + 20:

                            wanted_cell = get_cell_location(pos)
                            self.color_single_cell(self.BLACK, wanted_cell[0], wanted_cell[1])
                            if wanted_cell == self.path.start_pawn: # Erases the pawns
                                self.path.start_pawn = None

                            elif wanted_cell == self.path.end_pawn:
                                self.path.end_pawn = None

                            elif wanted_cell in self.path.walls: # Erases wall or water cell
                                self.path.walls.remove(wanted_cell)

                            elif wanted_cell in self.path.water:
                                self.path.water.remove(wanted_cell)

                if event.type == pygame.MOUSEMOTION:
                    if self.clear_btn.is_over(pos): # Changes button color if hover over
                        self.clear_btn.color = self.LIGHT_RED
                    else:
                        self.clear_btn.color = self.WHITE

                    if self.bfs_btn.is_over(pos):
                        self.bfs_btn.color = self.LIGHT_RED
                    else:
                        self.bfs_btn.color = self.WHITE

                    if self.dijkstra_btn.is_over(pos):
                        self.dijkstra_btn.color = self.LIGHT_RED
                    else:
                        self.dijkstra_btn.color = self.WHITE

                    if self.heap_btn.is_over(pos):
                        self.heap_btn.color = self.LIGHT_RED
                    else:
                        self.heap_btn.color = self.WHITE

                    if self.a_star_btn.is_over(pos):
                        self.a_star_btn.color = self.LIGHT_RED
                    else:
                        self.a_star_btn.color = self.WHITE

if __name__ == "__main__":
    start = App()
    start.launch()
