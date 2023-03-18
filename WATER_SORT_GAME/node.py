
class NodeForBFS:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action


class NodeForAStar:
    def __init__(self, state, parent=None, action=None, g_value=0, f_value=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g_value = g_value
        self.f_value = f_value

    def __lt__(self, other):
        # priority: f, h
        if self.f_value < other.f_value:
            return True
        elif self.f_value == other.f_value:
            return self.f_value - self.g_value < other.f_value - other.g_value
        else:
            return False