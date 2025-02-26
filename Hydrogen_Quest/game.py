from random import randint

import pygame
from pygame.locals import *

from constants import *
from fuel_stations import FuelStations
from health import Health
from items import PowerUpGroup, ObstacleGroup
from my_vehicle import MyVehicle
from nodes import NodeGroup
from other_vehicles import OtherVehicles, VehicleGroup
from path import *
from pauser import Pause
from sprites import MazeSprites
from text import TextGroup


class GameController:
    """
    Class representing and controlling our game.
    """

    def __init__(self, level, score):
        """
        Initializes a new game and all variables.

        Parameters:
            level (int): current level
            score (int): current player score
        """
        pygame.init()
        # Initialize screen and first background
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill(LIGHT_BLUE)

        # Timer for updates
        self.clock = pygame.time.Clock()

        # All game text, welcome screen, end game
        self.text_group = TextGroup()
        self.ready = False
        self.game_over = False

        # Sounds
        pygame.mixer.music.load(resource_path('Assets/theme_loop.wav'))
        pygame.mixer.music.play(-1)
        self.powerup_sound = pygame.mixer.Sound(resource_path('Assets/power_up.wav'))
        self.refuel_sound = pygame.mixer.Sound(resource_path('Assets/refuel.wav'))
        self.convert_sound = pygame.mixer.Sound(resource_path('Assets/convert.wav'))
        self.lose_fuel_sound = pygame.mixer.Sound(resource_path('Assets/lose_fuel.wav'))
        self.level_up_sound = pygame.mixer.Sound(resource_path('Assets/level_up.wav'))

        # Pauser
        self.pause = Pause(False)

        # Game variables
        self.score = score
        self.text_group.update_text(SCORE_TXT, str(self.score).zfill(6))
        self.level = level
        self.health = Health(self.lose_fuel_sound)
        self.next_level = False

        # Images for maze
        self.maze_sprites = MazeSprites(self.level)

        # Game objects
        # Maze map locations
        self.nodes = None
        self.road = None
        self.grass = None
        self.yard = None

        # Initializes lists to hold all occupied positions
        self.occupied_road = []
        self.occupied_grass = []

        # Game objects
        self.my_vehicle = None
        self.other_vehicles = None
        self.powerups = None
        self.obstacles = None
        self.fuel_stations = None

    def start_game(self):
        """
        Starts the game. Initializes the correct map and all game objects:
        hydrogen vehicle, obstacles, power ups.
        """
        # Map for game play - node locations represent the road
        self.nodes = NodeGroup(self.level)
        self.nodes.create_position_dict()
        self.road = self.nodes.road_locations
        self.grass = self.nodes.grass_locations
        self.yard = self.nodes.yard_location

        # Hydrogen vehicle controlled by user
        self.my_vehicle = MyVehicle(self.nodes.get_node_from_tiles(12, 18))

        # All other collectible vehicles
        self.other_vehicles = VehicleGroup()

        # Power up objects
        self.powerups = PowerUpGroup(self.nodes, self.road, self.occupied_road)
        # Obstacles
        self.obstacles = ObstacleGroup(self.nodes, self.road, self.occupied_road)

        # Fuel stations
        self.fuel_stations = FuelStations(self.nodes, self.grass)

    def update(self):
        """
         Updates the game and game objects once per frame.
        """
        # dt is the number of seconds since the previous call
        dt = self.clock.tick(30) / 1000
        if not self.pause.paused:
            self.my_vehicle.update(dt)
            self.other_vehicles.update(dt)
            for vehicle in self.other_vehicles.vehicles:
                if vehicle.remove:
                    self.other_vehicles.vehicles.remove(vehicle)

            if len(self.powerups.powerups) > 0:
                self.powerups.update(dt)

            if len(self.obstacles.obstacles) > 0:
                self.obstacles.update(dt)

            self.check_powerup_events()
            self.check_obstacle_events()
            self.check_fuel_events()

            self.health.update(dt, self.text_group)
            if self.health.fuel_level <= 0:
                self.my_vehicle.set_speed(20)

        self.pause.update(dt)
        self.check_events()
        self.draw()
        self.text_group.update(dt)

    def update_score(self, points):
        """
        Updates the player score.
        Parameters:
            points (int): point value of the power up
        """
        # Update score
        self.score += points
        self.text_group.update_text(SCORE_TXT, str(self.score).zfill(6))

        # Player win
        if self.score >= 5000:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(self.level_up_sound)
            self.game_over = True

        # Go to next level
        elif self.score >= self.level * 1000:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(self.level_up_sound)
            self.next_level = True

    def check_powerup_events(self):
        """
        Creates power up objects, and checks for collisions.
        """
        # Maintains desired number power ups on the screen at all times
        while len(self.powerups.powerups) < 5 + (self.level // 2):
            # Only spawn 'send truck' power up if one is not already on screen, and there is a truck to send
            if CONV_TRUCK in self.other_vehicles.vehicle_types and SEND_TRUCK not in self.powerups.powerup_types:
                type = SEND_TRUCK
            else:
                type = POWER_UP
            self.powerups.add_powerup(type)
            self.occupied_road = self.powerups.occupied_locations

        # Check for collision with user vehicle
        for powerup in self.powerups.powerups:
            # If there was a collision, remove power up and update score/do power up action
            if self.my_vehicle.collision(powerup):
                pygame.mixer.Sound.play(self.powerup_sound)
                # Add vehicle power up
                if powerup.name is ADD_VEHICLE:
                    self.text_group.hide_tip_text()
                    self.text_group.show_text(COLLECT_TXT)
                    position = self.road[randint(0, len(self.road) - 1)]
                    x, y = position[0], position[1]
                    vehicle_type = VEHICLE_TYPES[self.level - 1][randint(0, len(VEHICLE_TYPES[self.level - 1]) - 1)]
                    self.other_vehicles.vehicles.append(OtherVehicles(self.nodes.get_node_from_tiles(x, y),
                                                                      vehicle_type, self.convert_sound, self.yard))
                    if len(self.other_vehicles.vehicles) == 4:
                        self.text_group.hide_tip_text()
                        self.text_group.show_text(SEND_TXT)

                # Add station power up
                elif powerup.name is ADD_STATION:
                    self.fuel_stations.add_station()
                    self.occupied_grass = self.fuel_stations.occupied_locations

                # Send truck power up
                elif powerup.name is SEND_TRUCK:
                    for vehicle in self.other_vehicles.vehicles:
                        if vehicle.sprites.name is CONV_TRUCK:
                            if not vehicle.send:
                                vehicle.send = True
                                self.update_score(50)

                self.powerups.powerups.remove(powerup)
                self.update_score(powerup.points)

    def check_obstacle_events(self):
        """
        Creates obstacle objects, and checks for collisions.
        """
        # Maintains desired number obstacles on the screen at all times
        while len(self.obstacles.obstacles) < 5 + (self.level // 2):
            self.obstacles.add_obstacle()
            self.occupied_road = self.obstacles.occupied_locations

        # Check for pylon collision with user vehicle
        for obstacle in self.obstacles.obstacles:
            # If there was a collision, play sound, slow down player vehicle
            if self.my_vehicle.collision(obstacle):
                self.text_group.hide_tip_text()
                self.text_group.show_text(CONSTRUCTION_TXT)
                self.obstacles.obstacles.remove(obstacle)
                pygame.mixer.Sound.play(self.lose_fuel_sound)
                self.my_vehicle.set_speed(20)
                self.my_vehicle.timer = 0

        # Check for other vehicle collection
        for vehicle in self.other_vehicles.vehicles:
            if self.my_vehicle.collision(vehicle):
                if vehicle.sprites.name in [TRUCK, BUS, TAXI, CAR, TRAIN]:
                    pygame.mixer.Sound.play(self.convert_sound)
                    if vehicle.sprites.name is TRUCK:
                        vehicle.sprites.name = CONV_TRUCK
                        self.update_score(50)
                    elif vehicle.sprites.name is BUS:
                        vehicle.sprites.name = CONV_BUS
                        self.update_score(100)
                    elif vehicle.sprites.name is TAXI:
                        vehicle.sprites.name = CONV_TAXI
                        self.update_score(100)
                    elif vehicle.sprites.name is CAR:
                        vehicle.sprites.name = CONV_CAR
                        self.update_score(125)
                    elif vehicle.sprites.name is TRAIN:
                        vehicle.sprites.name = CONV_TRAIN
                        self.update_score(125)

    def check_fuel_events(self):
        """
        Checks for collisions between user vehicle and fuel stations to fuel up.
        """
        # Make sure fuel station exists
        if len(self.fuel_stations.positions) > 0:
            for position in self.fuel_stations.positions:
                dist = self.my_vehicle.position - position
                dist_squared = dist.magnitude_squared()
                rad_squared = (self.my_vehicle.collide_radius + 40) ** 2
                if dist_squared <= rad_squared:
                    if self.health.fuel_level < 5:
                        self.health.fuel_level += 1
                        pygame.mixer.Sound.play(self.refuel_sound)
                        self.my_vehicle.set_speed(60)

    def check_events(self):
        """
        Function to check for game events using pygame methods.
        """
        for event in pygame.event.get():
            # Check if user closes the game window
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                # Check if user presses the space bar
                if event.key == K_SPACE:
                    self.pause.set_pause(player_paused=True)
                    # Game paused - show text and hide objects
                    if self.pause.paused:
                        self.text_group.show_text(PAUSED_TXT)
                        self.hide_entities()
                    # Game not paused - hide text and show objects
                    else:
                        self.text_group.hide_text(PAUSED_TXT)
                        self.show_entities()

    def show_entities(self):
        """
        Makes all game objects visible.
        """
        self.my_vehicle.visible = True
        self.other_vehicles.show()
        self.powerups.show()
        self.obstacles.show()

    def hide_entities(self):
        """
        Makes all game objects invisible.
        """
        self.my_vehicle.visible = False
        self.other_vehicles.hide()
        self.powerups.hide()
        self.obstacles.hide()

    def draw(self):
        """
        Draws all game objects to the screen.
        """

        # Background and all text objects (currently all invisible)
        self.screen.blit(self.background, (0, 0))
        self.text_group.draw(self.screen)

        # Header text
        self.text_group.show_game_text()

        # Draw maze images on background
        self.background = self.maze_sprites.construct_background(self.background)

        # Fuel and life icons
        self.health.draw(self.screen)

        # All other objects
        self.powerups.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.my_vehicle.draw(self.screen)
        self.other_vehicles.draw(self.screen)
        self.background = self.fuel_stations.draw(self.background)

        pygame.display.update()
