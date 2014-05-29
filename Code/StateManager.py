#----------------------- State Manager --------------------------
      
class StateManager(object):
      def __init__(self):
            """Class that controls the running of the game Entities states.

            This class determines what current state a particular game enity is
            using and ensures that the correct function is called to represent
            this

            self.states: stores all of the states in an internal dictionary
            so that they can be refered to later in the program. Usually a string variable

            self.active_state: Simply stores the currently active state. Usually a
            string variable.

            """
            self.states = {} # Stores the states
            self.active_state = None # The currently active state

      def add_state(self, state):
            """Function that adds a new state to the internal dictionary.
            """
            self.states[state.name] = state

      def think(self):
            """Function that runs an active state, and possibly change to a new state

            new_state_name: used to hold the return value of calling the check_conditions
            function.
            """
            # Only continue if there is an active state
            if self.active_state is None: return

            # Perform the actions of the active state, and check conditions
            self.active_state.do_actions()
            new_state_name = self.active_state.check_conditions()

            # If check_conditions returns new state then call set_state function
            if new_state_name is not None:
                  self.set_state(new_state_name)

      def set_state(self, new_state_name):
            """Function that is responsible for changing between states

            This function also performs any exit and entry actions required to
            change states, such as changing entity speed or location (dependent on
            state coding)

            """
            # Change states and perform any exit / entry actions
            if self.active_state is not None:
                  self.active_state.exit_actions()
                  
            self.active_state = self.states[new_state_name]
            self.active_state.entry_actions()
