#
# Python Bouncing BU Logo
# Based on Python Pygame Introduction by Pete Shinners
#  http://www.pygame.org/docs/tut/intro/intro.html
#

# Import the sys and pygame modules into the program
import sys
import pygame
from pygame.locals import *

from World import *
from Entities import *
from Config import *

# Initialise the size, width and height variables
#w, h = screen_size

# Initialise the screen for the screen size we set
screen = pygame.display.set_mode((screen_size), 0, 32)

# Set the caption on the window
pygame.display.set_caption('Games Lab #3')


#---------------------- Set Up Animation Loop ETC ----------------------------

# Create a clock to allow us to access tick_busy_loop
clock = pygame.time.Clock()
global world
#------------------- Game Class -----------------------------
                
class Game:
        def __init__(self, *args):
                """Constructor for the Game class,ensures that the Game class starts on the correct state

                state: The phase the game is running in, determines what world and entities should be created
                """
                self.world = World(startup_screen_backdrop)
                self.world.state = "startup"

        def startup(self):
                """Creates a new startup textbox, with specified text, and places it in the location on the specified world

                world: Essentially the window to which entities are added to,
                should be a World object

                entity: Arbitrary label to hold a new TextBox Entity
                """
                self.world = World(startup_screen_backdrop)
                
                hordelogo = MainImage(self.world)
                hordelogo.location = Vector((screen_size[0]/2),(screen_size[1]/3))
                self.world.add_entity(hordelogo)

                btn_new = ButtonImageNew(self.world)
                w,h = hordelogo.image.get_size()
                btn_new.location = Vector(hordelogo.location.get_x(), hordelogo.location.get_y() +h)
                self.world.add_entity(btn_new)
                
                btn_quit = ButtonImageQuit(self.world)
                w,h = btn_new.image.get_size()
                btn_quit.location = Vector(btn_new.location.get_x(), btn_new.location.get_y() + h)
                self.world.add_entity(btn_quit)

        def playerDead(self):
                text = DeadText(self.world)
                text.location = Vector((screen_size[0]/2),(screen_size[1]/3))
                self.world.add_entity(text)

                self.world.state = "idle"

        def completed(self):
                """Creates a new startup textbox, with specified text, and places it in the location on the specified world

                world: Essentially the window to which entities are added to,
                should be a World object

                entity: Arbitrary label to hold a new TextBox Entity
                """
                self.world = World(startup_screen_backdrop)
                
                hordelogo = MainImage(self.world)
                hordelogo.location = Vector((screen_size[0]/2),(screen_size[1]/3))
                self.world.add_entity(hordelogo)

                btn_new = ButtonImageNew(self.world)
                w,h = hordelogo.image.get_size()
                btn_new.location = Vector(hordelogo.location.get_x(), hordelogo.location.get_y() +h)
                self.world.add_entity(btn_new)
                
                btn_quit = ButtonImageQuit(self.world)
                w,h = btn_new.image.get_size()
                btn_quit.location = Vector(btn_new.location.get_x(), btn_new.location.get_y() + h)
                self.world.add_entity(btn_quit)

                text = CompletedText(self.world)
                text.location = Vector(220,120)
                self.world.add_entity(text)
                                

        def runGame(self):
                """Creates the sprites essential to playing the game.

                places the sprites in a specified location on the specified world

                zombie_count: determines how many zombie entities will be created

                food_count: determines how many food entities will be created

                entity: Arbitrary label to hold a new entity. Should create a specified
                entity and place on the specified world

                Within the first if statement this function also specifies the state
                that the zombie object should adopt (AI)
                """
                self.world = World(startup_screen_backdrop)
                
                i = 0
                
                while i < zombie_count:
                        entity = Zombie(self.world)
                        entity.location = Vector(randint(80, w), randint(80, h))
                        entity.brain.set_state("exploring")
                        self.world.add_entity(entity)
                        i += 1
                                                
                i = 0

                while i < food_count:
                        entity = Food(self.world)
                        entity.location = Vector(randint(100, w), randint(100, h))
                        self.world.add_entity(entity)
                        i += 1
                        
                i = 0

                while i < trapdoor_count:
                        entity = Trapdoor(self.world)
                        entity.location = Vector(50,50)
                        entity.brain.set_state("trapdoor_open")
                        self.world.add_entity(entity)
                        i += 1
                        
                i = 0

                while i < player_count:
                        entity = Player(self.world)
                        entity.location = Vector(50,50)
                        entity.brain.set_state("playing")
                        self.world.add_entity(entity)
                        i += 1
                i = 0
                        
                self.state = "idle"
                

        def handleEvent(self, event):
                """Returns a new state for the Game object.

                based on the previous state and input from the user,
                which essentially depends on what world is currently being displayed

                pressed_keys: The keys pressed by the user. Determined by the
                pygame.key.get_pressed module
                """
                pressed_keys = pygame.key.get_pressed()
                mouse_pressed = pygame.mouse.get_pos()
                if event == MOUSEBUTTONDOWN:
                        self.world.state = self.world.get_clickable_entity(mouse_pressed)
                elif self.world.state == "idle" and pressed_keys[K_ESCAPE]:
                        self.world.state = "startup"
                elif event == pygame.QUIT: exit()
                

        def run(self):
                """Function that controls the whole running of the Game.

                Determines which world should be presented to the user, along with the
                required entities and display's them on the screen

                world: used to store the currently displaying world. Should
                be a World object

                time_passed: stores the update of the clock object, running at 20fps

                screen: Specifies the screen to which the world and its entities
                should be displayed
                """
                # initialise pygame
                pygame.init()

                # The animation loop (infinite)
                while 1:
                        if self.world.state == "startup":
                                self.startup()
                        elif self.world.state == "newGame":
                                self.runGame()
                        elif self.world.state == "completed":
                                self.completed()
                        elif self.world.state == "dead":
                                self.playerDead()         
                        elif self.world.state == "quitGame":
                                exit()
                                


                        # checks to see if there are any events occuring in pygame
                        for event in pygame.event.get():
                                # passes the event type to the handleEvent function which determines what shall be done
                                self.handleEvent(event.type)

                        time_passed= clock.tick(30)

                        self.world.processEntities(time_passed)
                        self.world.renderEntities(screen)
     
                        # flips display from buffer onto the screen
                        pygame.display.flip()

game = Game(*sys.argv)
game.run()
