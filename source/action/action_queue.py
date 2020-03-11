from source.entity.player import Player
from source.action.action import Action

class ActionQueue:
    """
        Class for holding all the actions characters currently want to execute
    """
    def __init__(self):
        self.queue:list = []
        self.player_actions_count:int = 0
    
    def append(self, action):
        """
        Append an action to the queue
        This always assumes action is an Action
        """
        if type(action.originator) is Player:
            self.player_actions_count += 1
        self.queue.append(action)
    
    def get_next_action(self):
        """
            Generator to get next action
        """
        i = 0
        debug_dict = {}
        while i < len(self.queue):
            breakpoint()
            debug_dict[f"self.queue[{i}] before subtracting"] = self.queue[i]
            self.queue[i] -= 1
            debug_dict[f"self.queue[{i}] after subtracting"] = self.queue[i]
            if self.queue[i] == 0:
                yield self.queue[i]
                self.queue.pop(i)
            else:
                i +=1
        return True

    def pop(self):
        """
            Iterate through the queue and reduce all actions time by 1. For every action whos time is now 0, resolve it.
        """
        actions_to_resolve = []
        for action in self.get_next_action():
            actions_to_resolve.append(action)
        for resolvable in actions_to_resolve:
            resolvable.resolve_action()
            if type(resolvable.originator) is Player:
                self.player_actions_count -= 1
