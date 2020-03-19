import random
import numpy

from source.grammar.GrammarRule import GrammarRule, GrammarVariable
from source.area.area import Area

#Grammar Library for SchoolGenerator
rule_great_hall_size = GrammarRule([[30],[40]], "size_hall")
# z x y floorTile
rule_great_hall = GrammarRule([[1, rule_great_hall_size, rule_great_hall_size, 1]], "great_hall")
# great_hall_ref = GrammarVariable('great_hall')

rule_room_size = GrammarRule([[]], "size", None, lambda x : random.randint(3,14))
# z x y floorTile
rule_room = GrammarRule([[1, rule_room_size, rule_room_size, 1]], "room")

# options 3, 6, 1
rule_num_rooms = GrammarRule([[]], "num_rooms", None, lambda x : [rule_room for i in range(0,random.randint(3,20))])
print(f"NUM_ROOMS = {GrammarRule.generate(rule_num_rooms)}")
rule_school = GrammarRule([[rule_great_hall, rule_num_rooms]], "root")

#TODO: Make this just a generate_school function
class SchoolGenerator:
    """
    Randomly generates a school
    """
    def __init__(self, area:Area):
        self.area = area

    # Make a Great Hall, and some number of rooms. Ensure that you can get from any room to any other room and that the great hall is connected to this network
    @staticmethod
    def generate_school(area:Area):
        school_tree = GrammarRule.generate(rule_school)
        startX = 0
        startY = 0
        elements = []
        i = 0
        while i < len(school_tree):
            # TODO make these a room class and return them at the end
            elem = {}
            elem['z'] = school_tree[i]
            elem['x'] = school_tree[i+1]
            elem['y'] = school_tree[i+2]
            elem['tile'] = school_tree[i+3]
            elements.append(elem)
            i += 4
        
        for element in elements:
            #randZ = random.randrange(1 + element['z'], area.z_length - 2 - element['z'])
            randX = random.randrange(1 + element['x'], area.x_length - 2 - element['x'])
            randY = random.randrange(1 + element['y'], area.y_length - 2 - element['y'])
            #Replace the prexisting tile with the floor_tile of the element
            for x in range(randX, randX + element['x']):
                for y in range(randY, randY + element['y']):
                    area.map[0, x, y] = element["tile"]
                    startX = x
                    startY = y
        # TODO instead of returning last room corner, use returned rooms to generate spawn point in great hall
        return (startX, startY)