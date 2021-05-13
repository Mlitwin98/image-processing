class StateManager():
    def __init__(self, image):
        self.states = []
        self.current_index = 0

        self.states.append(image)

    def new_state(self, image):
        if len(self.states) - 1 - self.current_index != 0:
            del self.states[self.current_index+1:]
        self.states.append(image)
        self.current_index = len(self.states) - 1

    def undo(self):
        if self.current_index > 0:
            self.current_index -= 1
        
        return self.states[self.current_index]

    def redo(self):
        if self.current_index < len(self.states) - 1:
            self.current_index += 1

        return self.states[self.current_index]