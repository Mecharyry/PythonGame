"""This module allows the user to customise the game to a certain extent

screen_size: the required size of the window in which the game will be displayed

w, h: holds the width and height of the screen. used throughout the program
to set entity locations etc

startup_screen_backdrop: holds the location of the background image that will be used
as a backdrop to the start up screen 

game_screen_backdrop: holds the location of the background that will be used
as a backdrop to the game screen

zombie_image: holds the location of the image that will be used as the zombie entity's
main image

zombie1_image: holds the location of the image that will be used as the zombie entity's
animation image (alternates between zombie and zombie1 to simulate walking

food_image: holds the location of the image that will be used as the food entity's
main image

player_image: holds the location of the image that will be used as the player entity's
main image

font_size = holds the font size that will be used when constructing the TextBox entity

clock: holds a new clock object that will be used to keep track of how long the game
has been running
"""
import pygame

screen_size = (800,600)
w, h = screen_size

zombie_count = 5
trapdoor_count = 1
player_count = 1
food_count = 1

main_image = 'assets/Backdrops/HordeMain.png'
startup_screen_backdrop = 'assets/Backdrops/startupBackdrop.png'
game_screen_backdrop = 'assets/Backdrops/gameBackdrop.png'

zombie_image = 'assets/Characters/zombieLeft.png'
zombie1_image = 'assets/Characters/zombieRight.png'

player_image = 'assets/Characters/playerLeft.png'
player1_image = 'assets/Characters/playerRight.png'
player_dead = 'assets/Characters/player_dead.png'

food_image = 'assets/Characters/food.png'

trapdoor_image = 'assets/Characters/trapdoor_open.png'
trapdoor1_image = 'assets/Characters/trapdoor_closed.png'

btn_new_game = 'assets/Buttons/newGame.png'
btn_quit_game = 'assets/Buttons/quitGame.png'
font_size = 42
clock = pygame.time.Clock()

