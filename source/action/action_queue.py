from source.entity.player import Player
from source.action.action import Action

class ActionQueue:
    """
    Class for holding all the actions characters currently want to execute
    """
    def __init__(self):
        self.heap:list = []
        self.player_actions_count:int = 0
    
    def push(self, action):
        """
        Append an action to the queue
        This always assumes action is an Action
        """
        if type(action.originator) is Player:
            self.player_actions_count += 1
        self.heap.append(action)
        i = len(self.heap)-1
        while(i != 0 and self.heap[i//2].time > self.heap[i].time):
            self.heap[i], self.heap[i//2] = self.heap[i//2], self.heap[i]
            i = i//2
    
    def pop(self):
        """
        Take the top item of the queue
        """
        #TODO fix pop
        if(len(self.heap) < 1):
            return False
        action = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap = self.heap[0:-1]
        i = 0
        while (i*2 < len(self.heap)):
            try:
                if(self.heap[i*2].time < self.heap[i*2+1].time):
                    least_index = i*2
                else:
                    least_index = i*2+1
                if self.heap[i].time > self.heap[least_index].time:
                    self.heap[i], self.heap[least_index] = self.heap[least_index], self.heap[i]
                    i = least_index
                else:
                    break
            except IndexError:
                break
        return action
    
    def resolve_actions(self, time):
        action_list = []
        while len(self.heap) > 0 and self.heap[0].time <= time:
            action_list.append(self.pop())
        for action in action_list:
            if type(action.originator) is Player:
                self.player_actions_count -= 1
            action.resolve_action()
