import pygame

from constants import *
from path import *
from sprites import Spritesheet
from vector import Vector


class Text:
    """
    Class to create individual text objects.
    """

    def __init__(self, text, color, x, y, size, id=None, visible=True):
        """
        Initializes a new text object.

        Parameters:
            text (string): the text to be written
            color (tuple): tuple representing a color in r, g, b format
            x (int): horizontal position
            y (int): vertical position
            size (int): size of the text
            id (int): individual id for the object
            visible (bool): boolean representing if the object is visible or not
        """
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector(x, y)
        self.set_up_font(resource_path('Assets/PressStart2P-Regular.ttf'))
        self.label = self.font.render(self.text, 1, self.color)
        self.lifespan = 5
        self.timer = 0

    def set_up_font(self, font_path):
        """
        Sets up the font used in the game.

        Parameters:
            font_path (string): font file location
        """
        self.font = pygame.font.Font(font_path, self.size)

    def set_text(self, new_text):
        """
        Updates a text object.

        Parameters:
            new_text (string): the new text to be written
        """
        self.text = str(new_text)
        self.label = self.font.render(self.text, 1, self.color)

    def draw(self, screen):
        """
        Draws a text object on the screen.

        Parameters:
             screen (object): pygame surface to draw on
        """
        if self.visible:
            x, y = self.position.as_tuple()
            screen.blit(self.label, (x, y))


class TextGroup:
    """
    Class to store all individual text objects in a dictionary: all_text.
    """

    def __init__(self):
        """
        Initializes the text group object.
        """
        self.nextid = 0
        self.all_text = {}
        self.set_up_text()
        self.image = Spritesheet()

    def add_text(self, text, color, x, y, size, id=None):
        """
        Adds a new text object to the dictionary.

        Parameters:
            text (string): the text to be written
            color (tuple): tuple representing a color in r, g, b format
            x (int): horizontal position
            y (int): vertical position
            size (int): size of the text
            id (int): individual id for the object
        """
        self.nextid += 1
        self.all_text[self.nextid] = Text(text, color, x, y, size, id=id)
        return self.nextid

    def set_up_text(self):
        """
        Adds all individual text objects to the text dictionary.
        """

        size = TILE_HEIGHT

        self.all_text[SCORE] = Text('SCORE', BLACK, 0, 0, size, visible=False)
        self.all_text[SCORE_TXT] = Text(str(0).zfill(6), BLACK, 0, TILE_HEIGHT, size, visible=False)

        self.all_text[FUEL] = Text('FUEL LEVEL', BLACK, 19.2 * TILE_WIDTH - 2, 0, size, visible=False)
        self.all_text[PAUSED_TXT] = Text('PAUSED!', BLACK, 8.7 * TILE_WIDTH, 13.5 * TILE_HEIGHT, size, visible=False)

        self.all_text[REFUEL_TXT] = Text('REMEMBER TO BUILD FUEL STATIONS TO REFUEL!', WHITE,
                                         1.6 * TILE_WIDTH, 2.8 * TILE_HEIGHT, 20, visible=False)
        self.all_text[NO_FUEL_TXT] = Text('OH NO! YOU RAN OUT OF FUEL!', WHITE,
                                          5.4 * TILE_WIDTH, 2.8 * TILE_HEIGHT, 20, visible=False)
        self.all_text[COLLECT_TXT] = Text('COLLECT OTHER VEHICLES TO EARN MORE POINTS!', WHITE,
                                          1.4 * TILE_WIDTH, 2.8 * TILE_HEIGHT, 20, visible=False)
        self.all_text[SEND_TXT] = Text('SEND YOUR HYDROGEN TRUCKS TO THE EG YARD!', WHITE,
                                       1.8 * TILE_WIDTH, 2.8 * TILE_HEIGHT, 20, visible=False)
        self.all_text[CONSTRUCTION_TXT] = Text('CONSTRUCTION SITES SLOW DOWN YOUR VEHICLE!', WHITE,
                                               1.6 * TILE_WIDTH, 2.8 * TILE_HEIGHT, 20, visible=False)

    def show_text(self, id):
        """
        Shows a text object on the screen.

        Parameters:
            id (int): id corresponding to a text object.
        """
        self.all_text[id].visible = True

    def hide_text(self, id):
        """
        Hides a text object on the screen.

        Parameters:
            id (int): id corresponding to a text object.
        """
        self.all_text[id].visible = False

    def show_game_text(self):
        """
        Shows the text objects for fuel, level, and lives.
        """
        for msg in [SCORE, SCORE_TXT, FUEL]:
            self.all_text[msg].visible = True

    def hide_game_text(self):
        """
        Shows the text objects for fuel, level, and lives.
        """
        for msg in [SCORE, SCORE_TXT, FUEL]:
            self.all_text[msg].visible = False

    def hide_tip_text(self):
        """
        Hides the text objects for in-game tips.
        """
        for msg in [REFUEL_TXT, NO_FUEL_TXT, COLLECT_TXT, SEND_TXT, CONSTRUCTION_TXT]:
            self.all_text[msg].visible = False

    def update_text(self, id, value):
        """
        Updates a text object in the dictionary.

        Parameters:
            id (int): id corresponding to a text object
            value (string): the new value of the text object
        """
        self.all_text[id].set_text(value)

    def update(self, dt):
        """
        Updates the text objects once per frame.

        Parameters:
        dt (float) : number of seconds since the previous update
        """
        for msg in [REFUEL_TXT, NO_FUEL_TXT, COLLECT_TXT, SEND_TXT, CONSTRUCTION_TXT]:
            self.all_text[msg].timer += dt
            if not self.all_text[msg].visible:
                self.all_text[msg].timer = 0
            if self.all_text[msg].timer >= self.all_text[msg].lifespan:
                self.hide_text(msg)
                self.all_text[msg].timer = 0

    def draw(self, screen):
        """
        Draws all text objects and welcome screen images.

        Parameters:
            screen (object): pygame screen to be drawn on
        """

        pygame.draw.rect(screen, DARK_BLUE, (TILE_WIDTH, 2.5 * TILE_HEIGHT, 880, 40), border_radius=20)
        for text_key in list(self.all_text.keys()):
            self.all_text[text_key].draw(screen)
