from source.entity.entity import Entity

class Material(Entity):
    """
    Base class for all Materials.
    """
    def __init__(self, *components):
        Entity.__init__(self, *components)