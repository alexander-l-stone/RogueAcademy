class Action:
    """
        Class for holding an action, extend this to make new actions
    """
    def __init__(self, originator, time_remaining:int, **kwargs):
        self.originator = originator
        self.time_remaining:int = time_remaining
        self.kwargs:dict = kwargs
    
    def __add__(self, o:int):
        # Raise a type error if there is not an int being added here
        if type(o) is not int:
            raise TypeError
        self.time_remaining += 1

    def __sub__(self, o:int):
        if type(o) is not int:
            raise TypeError
        self.time_remaining -= 1
    
    def __eq__(self, o:int):
        #Raise a type error if there is not an int being compared here
        return self.time_remaining == 0
    
    def resolve_action(self):
        """
            Resolve this action
        """
        return True
