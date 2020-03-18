import random

from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.area.area import Area

#Grammar Library for SchoolGenerator
#TODO: Assign Great Hall to a variable
great_hall = GrammarRule([[{'size': (1, 30, 30), 'floor_tile': 1}]])
# great_hall_ref = GrammarVariable('great_hall')

#TODO: Differentiate between different types of rooms
room = GrammarRule([[{'size': (1, 10, 10), 'floor_tile': 1}], [{'size': (1, 6, 6), 'floor_tile': 1}], [{'size': (1, 3, 3), 'floor_tile': 1}]])

num_rooms = GrammarRule([[room, room, room], [room, room, room, room, room, room], [room]])
school = GrammarRule([[great_hall, num_rooms]])

#TODO: Make this just a generate_school function
class SchoolGenerator:
    """
    Randomly generates a school
    """
    def __init__(self, area:Area):
        self.area = area

# Make a Great Hall, and some number of rooms. Ensure that you can get from any room to any other room and that the great hall is connected to this network
    def generate_school(self):
        school_tree = GrammarRule.generate(school)
        startX = 0
        startY = 0
        for element in school_tree:
            randX = random.randrange(1 + element["size"][1], self.area.x_length - 2 - element["size"][1])
            randY = random.randrange(1 + element["size"][2], self.area.y_length - 2 - element["size"][2])
            #TODO: make RandZ
            #Replace the prexisting tile with the floor_tile of the element
            for x in range(randX, randX + element["size"][1]):
                for y in range(randY, randY + element["size"][2]):
                    self.area.map[0, x, y] = element["floor_tile"]
                    startX = x
                    startY = y
        return (startX, startY)