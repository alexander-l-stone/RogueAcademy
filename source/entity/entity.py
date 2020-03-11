class Entity:
    def __init__(self, *components):
        self.components = {}

        for component in components:
            self.set(component)

    def set(self, component):
        if (type(component) == str):
            key = component
            self.components[key] = True
            return
        else:
            key = type(component)
            self.components[key] = component
            return

    def get(self, key):
        if self.has(key):
            return self.components[key]
        return None

    def has(self, key):
        return self.components.get(key) is not None
