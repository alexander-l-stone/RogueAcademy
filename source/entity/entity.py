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

    def get(self, name):
        if self.has(name):
            return self.components[name]
        return None

    def has(self, name):
        return self.components.get(name) is not None
