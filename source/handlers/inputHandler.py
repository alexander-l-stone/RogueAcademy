import tcod.event

#TODO: Figure out a good way of doing input handling.

class InputHandler:
    def __init__(self):
        pass
    
    def handle_keypress(self, event):
        if(event.sym == tcod.event.K_UP):
            return {"type": "move", "value": (0, 0, -1)}
        elif(event.sym == tcod.event.K_DOWN):
            return {"type": "move", "value": (0, 0, 1)}
        elif(event.sym == tcod.event.K_LEFT):
            return {"type": "move", "value": (0, -1, 0)}
        elif(event.sym == tcod.event.K_RIGHT):
            return {"type": "move", "value": (0, 1, 0)}
