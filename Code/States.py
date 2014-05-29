import pygame
from pygame.locals import *
from random import randint
from StateManager import *
from Config import *
from Vector import Vector
from World import *

#--------------------------- State ----------------------------

      # This is the State Base Class
class State(object):

      def __init__(self, name):
            """State base class sets up basic requirements of child classes.

            name: The quick reference name given to a state so that it can be
            quickly called using an internal dictionary
            """
            self.name = name

      def do_actions(self):
            """Function responsible for determining the entity's action (what it does)

            Function is called everytime the entity is processed. By default this function
            does nothing, subclasses determine there own functionality.
            """
            pass

      def check_condtions(self):
            """ Function resposible for determining whether or not another state is required.

            Function is called everytime the entity is processed. By default this
            function does nothing, subclasses determine there own functionality.
            """
            pass

      def entry_actions(self):
            """Function responsible for one time entry actions into a particular state.

            Function is called only once when entering a new state. By default this
            function does nothing, subclasses determine there own functionality.
            """
            pass

      def exit_actions(self):
            """Function responsible for one time exit actions when leaving a particular state.

            Function is called only once when exiting a state. By default this
            function does nothing, subclass determine there own functionality.
            """
            pass

#------------------------- zombie State Exploring -----------------------

class ZombieStateExploring(State):
      
      def __init__(self, zombie):
            """Subclass of State used to represent a zombie exploring state.

            This class has a zombie entity(sprite) plot its own course around
            the screen going at a set speed. When the zombie entity comes within a
            specified range of the player sprite it will swap to the seeking state.
            """
            # Call the base class constructor to initialise the State
            State.__init__(self, "exploring")

            # Set the zombie that this State will manipulate
            self.zombie = zombie
            
      def do_actions(self):
            """Function that is resposible for determining the entity's action.

            This function states that 1 in 20 calls plot a random destination
            for the zombie entity
            """
            # Change direction, 1 in 20 calls
            if randint(1, 20) == 1:
                  self.zombie.random_destination()

      def check_conditions(self):
            """Function that determines whether or not to swap to a different state.

            In this class a state change is triggered when the zombie sprite is
            within a particular distance of the player sprite.

            player: stores the return value of calling the get_close_entity function.
            Usually None unless the zombie entity is within the required distance of
            the player entity to swap states. In which case it will return the player
            entity and change states from exploring to seeking
            """
            # If there is a nearby player, switch to seeking state
            player = self.zombie.world.get_close_entity("player", self.zombie.location)
            if player is not None and player.player_dead != True:
                  self.zombie.player_id = player.id
                  return "seeking"
            
            return None

      def entry_actions(self):
            """Function responsible when first running the Exploring state.

            simply sets up the zombie entity speed, which is 50 plus a random
            number between -20 and 10 to make each zombie entity behave differently
            the function then calls the random_destination() function to make the
            zombie move randomly
            """
            # Start with random speed and heading
            self.zombie.speed = 50 + randint(-20, 10)
            self.zombie.random_destination()


#------------------------- zombie State Seeking Class -----------------------
class ZombieStateSeeking(State):
      def __init__(self, zombie):
            """Subclass of State used to represent a zombie seeking state.

            This class has a zombie entity(sprite) chase after a player entity
            by setting the zombies destinaion to match the player location when entering
            the seeking state the zombie entity gains additional speed. If the player
            manages to outrun the zombie then the zombie will revert to its exploring
            state.

            self.got_player: if the zombie comes in range of the player and manages
            to kill them then this will trigger the zombie to go into an eating
            state within the check_conditions function
            """
            State.__init__(self, "seeking")
            #set the zombie that this state will manipulate
            self.zombie = zombie
            self.got_player = False

      def do_actions(self):
            """Function that is resposible for determining the entity's action.

            This function gets the player location and sets the zombie entity destination
            location should correspond. giving the effect of the zombie chasing the player
            """            
            player = self.zombie.world.get(self.zombie.player_id)

            if player is None:
                  return

            self.zombie.destination = player.location

            if self.zombie.location.get_distance_to(player.location) < 55.:
                  player.bitten()
            

      
      def check_conditions(self):
            """Function that determines whether or not to swap to a different state.

            In this class a state change is triggered when the zombie sprite is
            no longer within a particular distance of the player sprite.

            player: stores the return value of calling the get_close_entity function.
            Usually None unless the zombie entity is within the required distance of
            the player entity. If the zombie entity is still within range then the
            seeking state is still within affect
            """
            player = self.zombie.world.get_close_entity("player", self.zombie.location)

            if player is None:
                  return 'exploring'
            elif player.player_dead == True:
                  return 'exploring'
            return None

      def entry_actions(self):
            """Function responsible when first running the Seeking state.

            simply sets up the zombie entity speed, which is 70 plus a random
            number between -20 and 10 to make each zombie entity behave differently.
            The seeking state provides an extra boost of speed to the zombies in their
            blood lust
            """
            #set the destination to the location of the player
            player = self.zombie.world.get(self.zombie.player_id)
        
            if player is not None:
                  self.zombie.destination = player.location
                  self.zombie.speed = 70 + randint(-20, 10)

#--------------------- Player State Playing Class ----------------------
class PlayerStatePlaying(State):
      def __init__(self, player):
            """Subclass of State used to represent a player playing state.

            This class provides the functionality to allow a user to play the
            game by allowing them to take control of a player entity with the
            keyboard arrow controls. The arrow keys set the heading and movement of the
            player sprite.
            """
            # Call the base class constructor to initialise the State
            State.__init__(self, "playing")
            # Set the player that this State will manipulate
            self.player = player
            
      def do_actions(self):
            """Function that is resposible for determining the entity's action.
            This function passes straight to the player_destination function so that it can
            plot a players heading and simulate movement
            """
            self.player.player_destination()
            self.player.add_stamina()

      def check_conditions(self):
            """Function that determines whether or not to swap to a different state.
            In this case remains blank at present, as the player will typically not
            change state
            """
            pressed_keys = pygame.key.get_pressed()
            
            food = self.player.world.getEntity("food")
            if food is not None:
                  if self.player.location.get_distance_to(food.location) < 10.:
                        self.player.carry(food.image)
                        self.player.world.remove_entity(food)

            if pressed_keys[K_SPACE] and self.player.stamina_use != False:
                  return "running"
            else:
                  return None

      def entry_actions(self):
            """Function responsible when first running the Playing state.

            simply sets up the player entity speed, which is 60
            """
            self.player.last_updated = pygame.time.get_ticks() / 1000
            #Start with random speed
            self.player.speed = 60

#--------------------- Player State Running Class ----------------------
class PlayerStateRunning(State):
      def __init__(self, player):
            """Subclass of State used to represent a player playing state.

            This class provides the functionality to allow a user to play the
            game by allowing them to take control of a player entity with the
            keyboard arrow controls. The arrow keys set the heading and movement of the
            player sprite.
            """
            # Call the base class constructor to initialise the State
            State.__init__(self, "running")
            # Set the player that this State will manipulate
            self.player = player
            
      def do_actions(self):
            """Function that is resposible for determining the entity's action.
            This function passes straight to the player_destination function so that it can
            plot a players heading and simulate movement
            """
            self.player.player_destination()
            self.player.deduct_stamina()

      def check_conditions(self):
            """Function that determines whether or not to swap to a different state.
            In this case remains blank at present, as the player will typically not
            change state
            """
            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_SPACE] == False:
                  self.player.stamina_use = False
                  return "playing"
            elif self.player.stamina <= 0:
                  self.player.stamina_use = False
                  return "playing"
            else:
                  return None

      def entry_actions(self):
            """Function responsible when first running the Playing state.

            simply sets up the player entity speed, which is 60
            """

            self.player.last_updated = pygame.time.get_ticks() / 1000
            #Start with random speed
            self.player.speed = 200

      def exit_actions(self):
            self.player.starting_stamina = self.player.stamina
            pass

#--------------------------- Trapdoor Class -----------------

class TrapdoorStateClosed(State):
      def __init__(self, trapdoor):
            # Call the base class constructor to initialise the State
            State.__init__(self, "trapdoor_closed")
            # Set the player that this State will manipulate
            self.trapdoor = trapdoor
            
      def do_actions(self):
            return

      def check_conditions(self):
            player = self.trapdoor.world.getEntity("player")
            if player is not None and player.got_food == True:
                  return "trapdoor_open"
            return None

      def entry_actions(self):
            self.trapdoor.image = pygame.image.load(trapdoor1_image).convert_alpha()
            

class TrapdoorStateOpen(State):
      def __init__(self, trapdoor):
            # Call the base class constructor to initialise the State
            State.__init__(self, "trapdoor_open")
            # Set the player that this State will manipulate
            self.trapdoor = trapdoor
            
      def do_actions(self):
            return None

      def check_conditions(self):
            player = self.trapdoor.world.getEntity("player")
            if player is not None and player.got_food == False:
                  if self.trapdoor.location.get_distance_to(player.location) > 50.:
                        return "trapdoor_closed"

            elif player is not None and player.got_food == True:
                  if self.trapdoor.location.get_distance_to(player.location) < 10.:
                        self.trapdoor.world.state = "completed"
            return

      def entry_actions(self):
            self.trapdoor.image = pygame.image.load(trapdoor_image).convert_alpha()

            
