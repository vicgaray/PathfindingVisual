"""Extra utilites used for the Pathfinding App."""
import pygame

class Button():

    def __init__(self, x, y, w, h, text, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color

    def draw_button(self, window):
        """Draws the button on, if there's text, align the text in the middle of the button."""
        pygame.draw.rect(window, self.color, (self.x, self.y, self.w, self.h), 0)

        if self.text:
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0,0,0))
            window.blit(text, (self.x + (self.w / 2 - text.get_width() / 2), self.y + (self.h / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        """Checks if position of mouse on grid is inbetween the buttons area."""
        if pos[0]  > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True

        return False


class PriorityQue():

    def __init__(self):
        self.wait_list = list()

    def deque(self):
        """Re-organizes list before returning the most prioritized node tuple."""
        self.wait_list.sort(key = lambda sub: sub[1]) # [[(nodex, nodey), priority], [(nodex, nodey), priority])]
        return self.wait_list.pop(0)[0]

    def enque(self, node, cost):
        """Adds node to list"""
        self.wait_list.append([node, cost])


def get_cell_location(pos):
    """Gets the cell's location based on the grid."""
    x = 50 # grid's starting x
    y = 20 # grid's starting y
    target_x = None # holds the cells x value
    target_y = None # holds the cells y value
    for i in range(20):
        if x <= pos[0]:
            target_x = x
        if y <= pos[1]:
            target_y = y

        x += 20
        y += 20

    return (target_x, target_y)
