from source.entity.player import Player
from source.action.action import Action
import heapq

class ActionQueue:
    """
    Class for holding all the actions characters currently want to execute
    """
    def __init__(self):
        self.heap:list = []
        self.player_actions_count:int = 0
        heapq.heapify(self.heap)

    def push(self, action:Action):
        """
        Append an action to the queue
        This always assumes action is an Action
        """
        if(type(action.originator) is Player):
            self.player_actions_count += 1
        heapq.heappush(self.heap, action)
    
    def pop(self):
        """
        Take the top item of the queue
        """
        if len(self.heap) != 0:
            return heapq.heappop(self.heap)
    
    def resolve_actions(self, time):
        action_list = []
        while len(self.heap) > 0 and self.heap[0].time <= time:
            action_list.append(self.pop())
        for action in action_list:
            if isinstance(action.originator, Player):
                self.player_actions_count -= 1
            action.resolve_action()
