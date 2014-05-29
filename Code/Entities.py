import math
from Vector import Vector
from StateManager import *
from States import *
from Config import *

#--------------- BASE CLASS OF ALL ENTITIES -----------------------
#--------------- Game Entity -------------------------------------

class GameEntity(object):

      def __init__(self, world, name, image, text):
            """Base class used to construct a game entity.

            Returns new GameEntity object
            with the specified variables world, name,image, text, location, destination, speed, brain and id, this is a super
            class and should ideally be used via inheritance

            world: holds a world object. For game entities this should ideally be the
            world game

            name: holds the name of the particular entity being constructed e.g. zombie

            image: holds the location of the image that will be used as the main image
            for whatever GameEntity is constructed. This image holder will also be used to
            store the image as a result of rotation for display

            start_image: holds the location of the image that will be used as the main image
            for whatever GameEntity is constructed. This one however will not be altered but
            used as a reference to reset the rotational image when a new rotation is required.

            text: holds the text that will be displayed in a textual entity; for example
            the TextBox Entity

            location: holds a default Vector of (0,0) that will be altered to set the location
            of the enity that is created

            destination: holds a default Vector of (0,0) that will be altered to set the destination
            location of the entity

            heading: holds a default Vector of (0,0) that will be altered to set the heading; vector
            between two points with no size. Can be seen as the direction

            last_heading: holds a default Vector of (0,0), this heading will typically be used
            to remember the last heading that was used for rotating an entity image, so that rotation
            does not get caught in an infinite loop

            speed: holds a number variable default 0. that will be altered to set the speed
            of the entity that is created

            brain: holds a StateManager object that is used to manage the states that the
            entity object will use

            id: holds the numerial id for the entity object that is being created

            """

            self.world = world
            self.name = name
            self.image = image
            self.start_image = image
            self.text = text
            self.location = Vector(0,0)
            self.destination = Vector(0,0)
            self.heading = Vector(0,0)
            self.last_heading = Vector(0,0)
            self.speed = 0.

            self.brain = StateManager()

            self.id = 0

      def render(self, surface):
            """Function to render the entity image to the screen

            Blit in this particular function places the sepecified image
            so that it its central point coorespondes to the location specified

            w,h: holds the width and height of the image used as the
            visual representation of the game entity

            new_image_vector: A vector that holds the central point of an image

            position: holds the value that represents the center of the image
            at a specified location
            """
            if self.speed != 0:
                  self.rotate_image()
                  
            w, h = self.image.get_size()
            w = w/2
            h = h/2
            new_image_vector = Vector(w, h)
            position = (self.location - new_image_vector)
            surface.blit(self.image, (position.get_x(), position.get_y()))

      def renderText(self, surface):
            """Function to render the entity text to the screen.

            Blit in this particular function places the specified text
            so that it appears in the center of the world it is created for

            font: holds a new font object, usually using a filename and the
            size of the font required Font(filename, size)

            lines: holds the separate lines of the text box so that they can be rendered.
            A new line is represented by a return character in the StartUpText(textBox) Code

            center: holds the location of the textbox object, and renders text in relation
            to this variable

            antialias: Boolean with value of 1, to ensure that when the font is rendered on
            screen all of the characters have smooth edges

            black: holds RGB value for the colour black, used later to set the text colour
            to black

            text: draws text on to a new surface. in this case it takes the line of text to
            be displayed, whether or not the charaters need antialising and what colour the
            characters should be

            text_pos: used to store the position of where the text will be rendered

            center: used in conjunction with self.location and text_pos to calculate the
            position of where the text will be rendered and then passes the value to the
            text_pos so that the text can be rendered

            height: simply the height of the font being used. Used to space one line of
            text from another
            """
            
            font = pygame.font.Font(None, font_size)

            lines = self.text.strip().splitlines()

            center = (self.location.get_x(), self.location.get_y())
            
            antialias = 1
            red = 255,0,0

            for line in lines:
                  text = font.render(line.strip(), antialias, red)
                  
                  text_pos = text.get_rect()

                  center_image_x = text_pos.width/2
                  center_image_y = text_pos.height/2
                  w, h = center
                  center = ((w - center_image_x),(h - center_image_y))
                  
                  text_pos = center 

                  height = font.get_linesize()
                  surface.blit(text, text_pos)
                  
                  new_y = self.location.get_y() + height
                  center = (self.location.get_x(), new_y)
                  

            pygame.display.flip()

      def process(self, time_passed):
            """Function that plots a new course.

            Function that determines whether or not the entity can move,
            if the enity can move then a new course is plotted based
            on its current location, and its destination

            vec_to_destination: holds a vector object that determines how to get
            from the current location to a destination location e.g. A (1,1) B(10,10)
            vec_to_des(9,9)

            distance_to_destination: holds the distance between two points. Should
            be a numeric value

            heading: holds the heading/direction that leads to the destination, Created
            by normalising the vec_to_destination. vect_to_destination / magnitude, giving it
            a magnitude of 1, which provides a heading

            travel_speed: holds the speed the entity should travel based on its given speed and
            the amount of time that has passed

            position: holds the current position of the entity based on its heading
            and its travel speed.
            """
            
            
            self.brain.think()

            if self.speed > 0 and self.location != self.destination:

                vec_to_destination = self.destination - self.location
                distance_to_destination = vec_to_destination.get_magnitude()
                self.heading = vec_to_destination
                self.heading.normalise()
                travel_speed = min(distance_to_destination, time_passed * self.speed)
                position = self.heading * travel_speed 
                self.location += position

      def rotate_image(self):
            """This function is used to rotate the entity image depending on its heading.
            """

            if self.heading.get_x() == 0 and self.heading.get_y() == 0: #or self.heading.compare_to(self.last_heading) == True:
                  self.heading = self.last_heading

            if self.heading.get_x() >=0 and self.heading.get_y() <=0:
                  value = math.degrees(math.acos(self.heading.get_x()))
                  self.image = self.start_image
                  self.image = pygame.transform.rotate(self.image, value)
                  self.last_heading = self.heading
                  return

            elif self.heading.get_x() <=0 and self.heading.get_y() <=0:
                  value = math.degrees(math.acos(self.heading.get_x()))
                  self.image = self.start_image
                  self.image = pygame.transform.rotate(self.image, value)
                  self.last_heading = self.heading
                  return

            elif self.heading.get_x() <=0 and self.heading.get_y() >=0 :
                  value = 180 + math.degrees(math.asin(self.heading.get_y()))
                  self.image = self.start_image
                  self.image = pygame.transform.rotate(self.image, value)
                  self.last_heading = self.heading
                  return

            elif self.heading.get_x() >=0 and self.heading.get_y() >=0:
                  value = 360 - math.degrees(math.asin(self.heading.get_y()))
                  self.image = self.start_image
                  self.image = pygame.transform.rotate(self.image, value)
                  self.last_heading = self.heading
                  return

      def handle_click(self, event):
            return

#------------------------------END BASE CLASS DECLARATION ------------------------------------------

#------------------------------------------------------------------------------------
#                             Main Game Entities
#------------------------------------------------------------------------------------

#-----------------------------------------zombie Entity -------------------------------------------

class Zombie(GameEntity):
      
      def __init__(self, world):
            """Sub-class of GameEntity used to represent a Zombie Entity.

            Initiating variables the same for the most part.

            text: By default is set to None, as only an image is required to
            represent a zomb

            image: used to hold the default image of a zombie Entity, rather
            than it being called in the main game loop

            exploring_state: used to hold the ZombieStateExploring object that will
            determine the zombie Entity's exploring action (AI)

            seeking_state: used to hold the ZombieStateSeeking object that will determine
            the zombie Entity's seeking action (AI)
            """
            
            text = None 
            image = pygame.image.load(zombie_image).convert_alpha()

            GameEntity.__init__(self, world, "zombie", image, None)

            #Create instances of each of the states
            exploring_state = ZombieStateExploring(self)
            seeking_state = ZombieStateSeeking(self)

            #Add the states to the state machine (self.brain)
            self.brain.add_state(exploring_state)
            self.brain.add_state(seeking_state)

      def render(self, surface):
            """Overridden function render provides unique rendering to the zombie Entity

            The function determines how much time has passed in the game
            and swaps the Entity image to give the effect of movement to the
            zombie Entity

            time: holds the time that has passed in the game in milliseconds

            time_seconds: holds the time that has passed in seconds. Cast used to
            ensure that the value does not contain decimal points so that a modulo can
            be performed
            """
            
            time = pygame.time.get_ticks()
            time_seconds = time /1000
            time_seconds = (int(float(time_seconds)))

            if (time_seconds % 2):
                  self.start_image = pygame.image.load(zombie_image).convert_alpha()
                  GameEntity.render(self, surface)
            else:
                  self.start_image = pygame.image.load(zombie1_image).convert_alpha()
                  GameEntity.render(self, surface)


      def random_destination(self):
            """Function that plots a random destination on the screen.

            random destination plotted by picking a random coordinate (number)
            between 0 and the screen size.
            
            w: stores the width of the screen. Usually a numeric value.
            h: stores the height of the screen. Usually a numeric value. 

            """
            # Select a point on the screen
            w, h = screen_size
            self.destination = Vector(randint(0, w), randint(0, h))

                  
#-------------------- food Entity -----------------------------

class Food(GameEntity):
      def __init__(self, world):
            """Sub-class of GameEntity used to represent a Food Entity.

            class sets its unique text(none) and image(foodEntity) and then
            calls to the GameEntity superclass to carry out all other functions
            required to run and display this Entity

            text: By default is set to None, as only an image is required to
            represent a food Entity

            image: used to hold the default image of a food Entity, rather
            than it being called in the main game loop
            """
            text = None
            image = pygame.image.load(food_image).convert_alpha()
            GameEntity.__init__(self, world, "food", image, None)

#------------------ Trap Door --------------------------------
class Trapdoor(GameEntity):
      def __init__(self, world):
            """Sub-class of GameEntity used to represent a Food Entity.

            class sets its unique text(none) and image(foodEntity) and then
            calls to the GameEntity superclass to carry out all other functions
            required to run and display this Entity

            text: By default is set to None, as only an image is required to
            represent a food Entity

            image: used to hold the default image of a food Entity, rather
            than it being called in the main game loop
            """
            text = None
            image = pygame.image.load(trapdoor_image).convert_alpha()
            GameEntity.__init__(self, world, "trapdoor", image, None)

            closed_state = TrapdoorStateClosed(self)
            open_state = TrapdoorStateOpen(self)

            #Add the states to the state machine (self.brain)
            self.brain.add_state(closed_state)
            self.brain.add_state(open_state)
            


#------------------- Player Entity ----------------------------

class Player(GameEntity):
      def __init__(self, world):
            """Sub-class of GameEntity used to represent a Player Entity.

            class sets its unique text(none) and image(PlayerEntity) and then
            calls to the GameEntity superclass to carry out all other functions
            required to run and display this Entity

            text: By default is set to None, as only an image is required to
            represent a player Entity

            image: used to hold the default image of a player Entity, rather
            than it being called in the main game loop
            """
            text = None
            image = pygame.image.load(player_image).convert_alpha()
            self.image_dead = pygame.image.load(player_dead).convert_alpha()
            self.health = 25
            self.stamina = 0
            self.max_stamina= 5
            self.stamina_use = False
            self.last_updated = 0
            self.carry_image = None
            self.got_food = False
            self.player_dead = False
            
            GameEntity.__init__(self, world, "player", image, None)

            playing_state = PlayerStatePlaying(self)
            running_state = PlayerStateRunning(self)
            self.brain.add_state(playing_state)
            self.brain.add_state(running_state)

      def carry(self, image):
            self.carry_image = image
            self.got_food = True

      def bitten(self):
            self.health -= 1
            if self.health <= 0:
                  self.speed = 0.
                  self.image = self.image_dead
                  self.player_dead = True
                  self.world.state = "dead"

      def deduct_stamina(self):
            time = pygame.time.get_ticks()
            time_seconds = time / 1000
            time_seconds = (int(float(time_seconds)))
            difference = time_seconds - self.last_updated

            if (difference <= self.max_stamina):
                  self.stamina = self.stamina - difference
                  self.last_updated = time_seconds

      def add_stamina(self):
            time = pygame.time.get_ticks()
            time_seconds = time / 1000
            time_seconds = (int(float(time_seconds)))
            difference = time_seconds - self.last_updated
            
            if (self.stamina <= self.max_stamina):
                  self.stamina = self.stamina + difference
                  self.last_updated = time_seconds
            if (self.stamina == self.max_stamina):
                  self.stamina_use = True

                  
      def player_destination(self):
            """Function that plots the player destination on the screen.

            player destination set by setting a blank vector and altering the x and y
            coords based on which key is pressed by the user. The player destination will
            then consist of a heading, and multiple key presses will simulate movement.

            pressed_keys: holds the state of all keyboard buttons. Used to determine
            if the user has pressed any of the buttons designed for movement.
          
            heading: holds a vector that corresponds to a heading. Determined by
            key presses.
            """
            # Select a point on the screen
            # set up variable to hold the result of determining if a key is pressed
            pressed_keys = pygame.key.get_pressed()
            heading = Vector(0,0)

            if pressed_keys[K_LEFT]:
                  heading.x = -1
            elif pressed_keys[K_RIGHT]:
                  heading.x = +1
            elif pressed_keys[K_UP]:
                  heading.y = -1
            elif pressed_keys[K_DOWN]:
                  heading.y = +1

            #diagonals
            if pressed_keys[K_RIGHT] and pressed_keys[K_UP]:
                  heading.x = 0.707
                  heading.y = -0.707
            if pressed_keys[K_DOWN] and pressed_keys[K_RIGHT]:
                  heading.x = 0.707
                  heading.y = 0.707
            if pressed_keys[K_DOWN] and pressed_keys[K_LEFT]:
                  heading.x = -0.707
                  heading.y = 0.707
            if pressed_keys[K_UP] and pressed_keys[K_LEFT]:
                  heading.x = -0.707
                  heading.y = -0.707

            self.heading = heading

            self.destination = self.location
                  

      def render(self, surface):
                        
            time = pygame.time.get_ticks()
            time_seconds = time/1000
            time_seconds = (int(float(time_seconds)))

            if (time_seconds % 2):
                  self.start_image = pygame.image.load(player_image).convert_alpha()
                  GameEntity.render(self, surface)
            else:
                  self.start_image = pygame.image.load(player1_image).convert_alpha()
                  GameEntity.render(self, surface)

            x = self.location.get_x()
            y = self.location.get_y()
            w,h = self.image.get_size()
            
            health_bar_x = x -15
            health_bar_y = y + h/2 +10
            surface.fill((255,0,0), (health_bar_x, health_bar_y, 25, 4))
            surface.fill((0,255,0), (health_bar_x, health_bar_y, self.health, 4))

            stamina_bar_x = x -15
            stamina_bar_y = y + h/2 + 20
            surface.fill((255,0,0), (stamina_bar_x, stamina_bar_y, self.max_stamina*4, 4))
            surface.fill((0,255,0), (stamina_bar_x, stamina_bar_y, self.stamina*4, 4))

            if self.carry_image:
                  w,h = self.carry_image.get_size()
                  carry_image_x = health_bar_x + 30
                  carry_image_y = health_bar_y
                  surface.blit(self.carry_image,(carry_image_x, carry_image_y))

      def process(self, time_passed):
            """Function that plots a new course.

            Function that determines whether or not the entity can move,
            if the enity can move then a new course based on its heading an
            its travel speed

            travel_speed: holds the speed the entity should travel based on its given speed and
            the amount of time that has passed
            """

            self.brain.think()

            if self.speed > 0:

                  travel_speed = time_passed * self.speed
                  self.location += self.heading * travel_speed

#----------------------------------------------------------------------
#                       Additional Entities
#----------------------------------------------------------------------

#-------------------- Image Entity -------------------------

class Image(GameEntity):
      def __init__(self, world, image, name):
            GameEntity.__init__(self, world, name, image, None)

class MainImage(Image):
      def __init__(self, world):
            image = pygame.image.load(main_image).convert_alpha()
            name = "main"
            Image.__init__(self, world, image, name)

#-------------------- Button Entity -----------------------

class Button(GameEntity):
      def __init__(self, world, image, name):
            GameEntity.__init__(self, world, name, image, None)

      def handle_click(self, event):

            rect = self.image.get_rect()
            x,y = self.location.get_x(), self.location.get_y()
            w,h = rect.width, rect.height
            w,h = w/2, h/2
            rect.top = self.location.get_y() - h
            rect.left = self.location.get_x() - w

            if(rect.collidepoint(event)):
                  return self.name
            else:   
                  return None

class ButtonImageNew(Button):
      def __init__(self, world):
            image = pygame.image.load(btn_new_game).convert_alpha()
            name = "newGame"
            Button.__init__(self, world, image, name)

class ButtonImageQuit(Button):
      def __init__(self, world):
            image = pygame.image.load(btn_quit_game).convert_alpha()
            name = "quitGame"
            Button.__init__(self, world, image, name)


#-------------------- Text Entity -------------------------
class TextBox(GameEntity):
      def __init__(self, world, name, text):
            """Subclass of GameEntity used to represent a default textBox Entity

            Subclass of GameEntity, but also baseclass for other TextBox Entitites
            such as StartupText(TextBox). This class is used to simply set up
            default variables and behaviours.

            text: By default is passed from a subclass, but if this class is used
            independent of a subclass then text is established when the object is created

            image: By default set to None, as text is not required to represent a
            TextBox Entity
            """
            image = None
            GameEntity.__init__(self, world, name, image, text)

      def render(self, surface):
            """Overridden function render provides unique rendering to the TextBox Entity

            This funstion ensures that the TextBox entity and all subclasses render
            correctly by passing itself to the renderText function of the GameEntity
            Class, and not to the render function which is meant specifically for images
            """
            GameEntity.renderText(self, surface)

#------------------ Startup Text Box --------------------------
class CompletedText(TextBox):    
      def __init__(self, world):
            """Subclass of TextBox used to store the text required at startup to display to
            the used

            Simply holds startupText and then passes to its superclass for rendering
            and behaviour

            text: used to hold the text to be rendered to the screen. Can be multi-line
            this will be handled in the renderText function
            """
            text = '''You Beat!'''
            TextBox.__init__(self, world, "completed",text)

class DeadText(TextBox):
      def __init__(self, world):
            text = '''YOU ARE DEAD!
                  press <Esc> to go back to the main menu'''
            TextBox.__init__(self, world, "completed", text)



