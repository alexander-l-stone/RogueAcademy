class Action:
    """
        Class for holding an action, extend this to make new actions
    """
    def __init__(self, originator:str, time_remaining:int, **kwargs):
        self.originator:str = originator
        self.time_remaining:int = time_remaining
        self.kwargs:dict = kwargs
        self.num_subtract = 0
    
    def __add__(self, o:int):
        # Raise a type error if there is not an int being added here
        if type(o) is not int:
            raise TypeError
        self.time_remaining += 1

    def __sub__(self, o:int):
        if type(o) is not int:
            raise TypeError
        print('subtracting')
        self.num_subtract += 1
        self.time_remaining -= 1
    
    def __eq__(self, o:int):
        #Raise a type error if there is not an int being compared here
        print('equating')
        return self.time_remaining == 0
    
    def resolve_action(self):
        """
            Resolve this action
        """
        pass
