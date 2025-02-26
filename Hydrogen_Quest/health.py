from sprites import FuelSprites
from constants import *
import pygame


class Health:
    """
    Class to represent user health.
    """
    def __init__(self, sound):
        """
        Initializes a new health object to keep track of user fuel.
        """
        self.fuel_level = 5
        self.timer = 0
        self.lifespan = 8
        self.fuel_sprites = FuelSprites(self.fuel_level)
        self.lose_fuel_sound = sound

    def update(self, dt, text_group):
        """
        Updates our fuel and life images once per frame.
        Checks for end-game conditions - no lives or fuel left. Returns true if either are empty.

        Parameters:
            dt (float): number of seconds since the previous update
         """

        self.timer += dt
        # Fuel depletes once per lifespan
        if self.timer >= self.lifespan:
            self.fuel_level -= 1
            self.timer = 0
            pygame.mixer.Sound.play(self.lose_fuel_sound)
            if self.fuel_level == 2:
                text_group.hide_tip_text()
                text_group.show_text(REFUEL_TXT)
            elif self.fuel_level == 0:
                text_group.hide_tip_text()
                text_group.show_text(NO_FUEL_TXT)

        self.fuel_sprites.reset_fuel(self.fuel_level)

    def draw(self, screen):
        """
        Draws the fuel icons on the screen.

        Parameters:
            screen (object): pygame surface to draw on
        """
        for i in range(len(self.fuel_sprites.images)):
            x = (i + 19) * TILE_WIDTH
            screen.blit(self.fuel_sprites.images[i], (x, TILE_HEIGHT))
