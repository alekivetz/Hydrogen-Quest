import pygame
from button import Button
from constants import *
from game import GameController
from sprites import Spritesheet
import time
from path import *


def get_font(size):
    """
    Function to set up and return font used in the menu screens using pygame.

    Parameters:
        size: size of the font
    """
    return pygame.font.Font(resource_path('Assets/PressStart2P-Regular.ttf'), size)


def main_menu(level, score):
    """
    Function to control the main menu, displaying text and creating buttons.

    Parameters:
        level: current game level
        score: current game score
    """
    while True:
        pygame.display.set_caption('Main Menu')
        screen.fill(LIGHT_BLUE)
        mouse_position = pygame.mouse.get_pos()

        # Create buttons
        play_button = Button(pos=(12.1 * TILE_WIDTH + 2, 8 * TILE_HEIGHT), text_input='PLAY GAME',
                             font=get_font(2 * TILE_HEIGHT), base_colour=BLACK, hover_colour=DARK_BLUE)
        how_to_button = Button(pos=(12.1 * TILE_WIDTH + 2, 12 * TILE_HEIGHT), text_input='HOW TO PLAY',
                               font=get_font(2 * TILE_HEIGHT), base_colour=BLACK, hover_colour=DARK_BLUE)
        quit_button = Button(pos=(12.1 * TILE_WIDTH + 2, 16 * TILE_HEIGHT), text_input='QUIT',
                             font=get_font(2 * TILE_HEIGHT), base_colour=BLACK, hover_colour=DARK_BLUE)

        # Display text
        screen.blit(get_font(65).render('HYDROGEN QUEST:', True, BLACK),
                    (0.2 * TILE_WIDTH, TILE_HEIGHT))
        screen.blit(get_font(36).render('THE ROAD TO SUSTAINABILITY', True, BLACK),
                    (0.2 * TILE_WIDTH, 3 * TILE_HEIGHT))

        for button in [play_button, how_to_button, quit_button]:
            button.change_colour(mouse_position)
            button.update(screen)

        # Check for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(mouse_position):
                    next_level(level, score)
                if how_to_button.check_for_input(mouse_position):
                    how_to(level, score)
                if quit_button.check_for_input(mouse_position):
                    sys.exit()

        pygame.display.update()


def how_to(level, score):
    """
    Function to display the 'how to' page of the menu, displaying text and images, and creating buttons.

    Parameters:
        level: current game level
        score: current game score
        """
    while True:
        pygame.display.set_caption('How to Play')
        screen.fill(LIGHT_BLUE)
        mouse_position = pygame.mouse.get_pos()
        image = Spritesheet()

        # Display text
        screen.blit(get_font(22).render('WELCOME TO', True, BLACK), (9.3 * TILE_WIDTH, 0.4 * TILE_HEIGHT))
        screen.blit(get_font(22).render('HYDROGEN QUEST: THE ROAD TO SUSTAINABILITY', True, BLACK),
                    (0.5 * TILE_WIDTH, 1.1 * TILE_HEIGHT))
        screen.blit(get_font(19).render('YOUR MISSION IS TO COLLECT 5000 HYDROGEN POINTS',
                                        True, BLACK), (0.6 * TILE_WIDTH, 2.5 * TILE_HEIGHT))
        screen.blit(get_font(19).render('ACROSS 5 CITIES, IN ORDER TO CREATE A SUSTAINABLE',
                                        True, BLACK), (0.4 * TILE_WIDTH, 3.1 * TILE_HEIGHT))
        screen.blit(get_font(19).render('TRANSPORTATION NETWORK AND COMBAT CLIMATE CHANGE!',
                                        True, BLACK), (0.4 * TILE_WIDTH, 3.7 * TILE_HEIGHT))
        screen.blit(get_font(19).render('COLLECT POWER UPS TO BUILD FUEL STATIONS AND ADD',
                                        True, BLACK), (0.7 * TILE_WIDTH, 4.7 * TILE_HEIGHT))
        screen.blit(get_font(19).render('MORE VEHICLES TO YOUR FLEET!',
                                        True, BLACK), (5.5 * TILE_WIDTH, 5.3 * TILE_HEIGHT))
        screen.blit(get_font(19).render('COLLECT OTHER VEHICLES TO EARN HYDROGEN POINTS!',
                                        True, BLACK), (0.9 * TILE_WIDTH, 6.3 * TILE_HEIGHT))
        screen.blit(get_font(19).render('WHEN A TRUCK HAS BEEN CONVERTED, IT IS READY TO BE',
                                        True, BLACK), (0.2 * TILE_WIDTH, 6.9 * TILE_HEIGHT))
        screen.blit(get_font(19).render('SENT TO THE EDMONTON GLOBAL YARD FOR USE!',
                                        True, BLACK), (2.3 * TILE_WIDTH, 7.5 * TILE_HEIGHT))

        screen.blit(get_font(19).render('+ 25 POINTS', True, BLACK),
                    (2.2 * TILE_WIDTH, 9.3 * TILE_HEIGHT))
        screen.blit(get_font(19).render('+ 50 POINTS', True, BLACK), (2.2 * TILE_WIDTH, 10.3 * TILE_HEIGHT))
        screen.blit(get_font(19).render('+ FUEL STATION (+ 25)', True, BLACK), (2.2 * TILE_WIDTH, 11.3 * TILE_HEIGHT))
        screen.blit(get_font(19).render('+ COLLECTIBLE VEHICLE:', True, BLACK),
                    (2.2 * TILE_WIDTH, 12.3 * TILE_HEIGHT))
        screen.blit(get_font(19).render('SEND TRUCKS TO EDMONTON GLOBAL YARD (+ 50)', True, BLACK),
                    (2.2 * TILE_WIDTH, 13.3 * TILE_HEIGHT))

        screen.blit(get_font(19).render('CONTROL YOUR VEHICLE WITH THE ARROW KEYS',
                                        True, BLACK), (2.4 * TILE_WIDTH, 14.5 * TILE_HEIGHT))
        screen.blit(get_font(19).render(' AND PRESS SPACE TO PAUSE!',
                                        True, BLACK), (5.7 * TILE_WIDTH, 15.1 * TILE_HEIGHT))

        screen.blit(get_font(19).render('COLLECT 1000 HYDROGEN POINTS TO',
                                        True, BLACK), (4.7 * TILE_WIDTH, 16 * TILE_HEIGHT))
        screen.blit(get_font(19).render(' ADVANCE TO THE NEXT CITY!',
                                        True, BLACK), (5.7 * TILE_WIDTH, 16.6 * TILE_HEIGHT))

        # Display images
        screen.blit(image.get_image(6, 0, TILE_WIDTH, TILE_HEIGHT),
                    (TILE_WIDTH, 9 * TILE_HEIGHT))
        screen.blit(image.get_image(6, 1, TILE_WIDTH, TILE_HEIGHT),
                    (TILE_WIDTH, 10 * TILE_HEIGHT))
        screen.blit(image.get_image(6, 4, TILE_WIDTH, TILE_HEIGHT),
                    (TILE_WIDTH, 11 * TILE_HEIGHT))
        screen.blit(image.get_image(6, 3, TILE_WIDTH, TILE_HEIGHT),
                    (TILE_WIDTH, 12 * TILE_HEIGHT))
        screen.blit(image.get_image(0, 1, TILE_WIDTH, TILE_HEIGHT),
                    (13 * TILE_WIDTH, 12 * TILE_HEIGHT))
        screen.blit(image.get_image(0, 7, TILE_WIDTH, TILE_HEIGHT),
                    (15 * TILE_WIDTH, 12 * TILE_HEIGHT))
        screen.blit(image.get_image(0, 5, TILE_WIDTH, TILE_HEIGHT),
                    (17 * TILE_WIDTH, 12 * TILE_HEIGHT))
        screen.blit(image.get_image(0, 3, TILE_WIDTH, TILE_HEIGHT),
                    (19 * TILE_WIDTH, 12 * TILE_HEIGHT))
        screen.blit(image.get_image(0, 9, TILE_WIDTH, TILE_HEIGHT),
                    (21 * TILE_WIDTH, 12 * TILE_HEIGHT))
        screen.blit(image.get_image(6, 5, TILE_WIDTH, TILE_HEIGHT),
                    (TILE_WIDTH, 13 * TILE_HEIGHT))

        # Display back button
        back_button = Button(pos=(12.1 * TILE_WIDTH, 19 * TILE_HEIGHT),
                             text_input='BACK', font=get_font(50), base_colour=BLACK, hover_colour=DARK_BLUE)
        back_button.change_colour(mouse_position)
        back_button.update(screen)

        # Check for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(mouse_position):
                    main_menu(level, score)

        pygame.display.update()


def choose_level():
    """
    Function to display the 'choose level' page of the menu, lets player choose the next level.

    Return:
        city: next city chosen by the user
    """
    time.sleep(4)
    pygame.mixer.music.load(resource_path('Assets/background2.wav'))
    pygame.mixer.music.play(-1)
    while True:
        pygame.display.set_caption('Where to Next?')
        screen.fill(LIGHT_BLUE)
        mouse_position = pygame.mouse.get_pos()

        # Display buttons
        city_1 = Button(pos=(12.1 * TILE_WIDTH + 2, 8 * TILE_HEIGHT), text_input=next_city[0],
                        font=get_font(60), base_colour=BLACK, hover_colour=DARK_BLUE)
        city_2 = Button(pos=(12.1 * TILE_WIDTH + 2, 12 * TILE_HEIGHT), text_input=next_city[1],
                        font=get_font(60), base_colour=BLACK, hover_colour=DARK_BLUE)
        city_3 = Button(pos=(12.1 * TILE_WIDTH + 2, 16 * TILE_HEIGHT), text_input=next_city[2],
                        font=get_font(60), base_colour=BLACK, hover_colour=DARK_BLUE)

        # Display text
        screen.blit(get_font(65).render('WHERE TO NEXT?', True, BLACK),
                    (0.8 * TILE_WIDTH, TILE_HEIGHT))

        for button in [city_1, city_2, city_3]:
            button.change_colour(mouse_position)
            button.update(screen)

        # Check for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if city_1.check_for_input(mouse_position):
                    city = next_city[0]
                    next_city.remove(city)
                    return city
                if city_2.check_for_input(mouse_position):
                    city = next_city[1]
                    next_city.remove(city)
                    return city
                if city_3.check_for_input(mouse_position):
                    city = next_city[2]
                    next_city.remove(city)
                    return city

        pygame.display.update()


def next_level(level, score):
    """
    Function to display the 'next' page of the menu, displaying text and images, and creating buttons.

    Parameters:
        level: current game level
        score: current game score
    """

    # First level is always Edmonton, then user gets to choose
    if level != 1:
        city = choose_level()
    else:
        city = 'EDMONTON'
    while True:
        screen.fill(LIGHT_BLUE)
        pygame.display.set_caption('Hydrogen Quest: The Road to Sustainability')
        mouse_position = pygame.mouse.get_pos()

        # Display text
        screen.blit(get_font(60).render(f'LEVEL {level}', True, BLACK), (6.8 * TILE_WIDTH, 8 * TILE_HEIGHT))
        city_name = get_font(60).render(city, True, BLACK)
        city_rect = city_name.get_rect(center=(485, 430))
        screen.blit(city_name, city_rect)

        # Display start button
        start_button = Button(pos=(12.1 * TILE_WIDTH, 16 * TILE_HEIGHT),
                              text_input='START', font=get_font(50), base_colour=BLACK, hover_colour=DARK_BLUE)
        start_button.change_colour(mouse_position)
        start_button.update(screen)

        # Check for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_for_input(mouse_position):
                    game = GameController(level, score)
                    game.start_game()
                    while True:
                        game.update()

                        if game.game_over:
                            end_game()
                        elif game.next_level:
                            level += 1
                            score = game.score
                            next_level(level, score)

        pygame.display.update()


def end_game():
    """
    Function to display the 'end game' page of the menu, displaying text and creating buttons.

    """
    while True:
        pygame.display.set_caption('You did it!')
        screen.fill(LIGHT_BLUE)
        mouse_position = pygame.mouse.get_pos()

        # Display buttons
        quit_button = Button(pos=(12.1 * TILE_WIDTH + 2, 16 * TILE_HEIGHT), text_input='QUIT',
                             font=get_font(2 * TILE_HEIGHT), base_colour=BLACK, hover_colour=DARK_BLUE)
        play_again_button = Button(pos=(12.1 * TILE_WIDTH + 2, 12 * TILE_HEIGHT), text_input='PLAY AGAIN?',
                                   font=get_font(2 * TILE_HEIGHT), base_colour=BLACK, hover_colour=DARK_BLUE)

        for button in [quit_button, play_again_button]:
            button.change_colour(mouse_position)
            button.update(screen)

        # Display text
        screen.blit(get_font(60).render('CONGRATULATIONS! YOU WIN!', True, BLACK),
                    (0.3 * TILE_WIDTH, 4 * TILE_HEIGHT))
        screen.blit(get_font(60).render('YOU WIN!', True, BLACK),
                    (6.2 * TILE_WIDTH, 6 * TILE_HEIGHT))

        # Check for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.check_for_input(mouse_position):
                    sys.exit()
                elif play_again_button.check_for_input(mouse_position):
                    global next_city
                    next_city = ['FORT MCMURRAY', 'GRANDE PRAIRIE', 'CALGARY', 'KAMLOOPS', 'PRINCE GEORGE', 'VANCOUVER']
                    next_level(1, 0)

        pygame.display.update()


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
starting_level = 1
starting_score = 0
next_city = ['FORT MCMURRAY', 'GRANDE PRAIRIE', 'CALGARY', 'KAMLOOPS', 'PRINCE GEORGE', 'VANCOUVER']
pygame.mixer.music.load(resource_path('Assets/background2.wav'))
pygame.mixer.music.play(-1)

main_menu(starting_level, starting_score)
