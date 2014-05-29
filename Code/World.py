import pygame
from Config import *
from Vector import *
#----------------------------- World --------------------------

class World(object):
    
    def __init__(self, background):
        self.entities = {} # Stores all the entities
        self.entity_id = 0 # Last entity ID assigned
        self.state = "idle"

        # Draw the background
        self.background = pygame.surface.Surface(screen_size).convert()
        self.background = pygame.image.load(background).convert()

    def add_entity(self, entity):
        # Stores the entity then advances the current id
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]

    def get(self, entity_id):
        # Find the entity, given its id
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def getEntity(self, name):
        for entity in self.entities.values():
            if entity.name == name:
                return entity
        return None

    def processEntities(self, time_passed):
        # process every entity in the world
        time_passed_seconds = time_passed / 1000.0
        for entity in self.entities.values():
                entity.process(time_passed_seconds)

    def renderEntities(self, surface):
        #draw the background and all the entities
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
                entity.render(surface)


    def get_close_entity(self, name, location, range=200.):
        # Find an entity within range of a location
        for entity in self.entities.values():
                if entity.name == name:
                    distance = location.get_distance_to(entity.location)
                    if distance < range:
                            return entity
        return None
    
    def get_clickable_entity(self, event):
        for entity in self.entities.values():
            get_state = entity.handle_click(event)
            if(get_state != None):
                return get_state
        return 
            
