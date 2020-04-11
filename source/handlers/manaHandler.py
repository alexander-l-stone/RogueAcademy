# from typing import Dict

class ManaHandler:
    def __init__(self):
        #TODO: Maybe add mana type here so each type gets its own handler
        return
    
    def spread_mana(self, area):
        """
        Does the mana spread for an area
        """
        # For Tile in Area, spread to the nearby 26 tiles
        pass
    
    def produce_mana(self, area):
        """
        Does the mana production for an area
        """
        pass
    
    def decay_mana(self, area):
        """
        Does the mana decay for an area
        """
        pass

    def tick_mana(self, area):
        """
        Doess all mana processes for an area
        """
        self.produce_mana(area)
        self.spread_mana(area)
        self.decay_mana(area)