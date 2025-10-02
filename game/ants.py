class Ant:
    def __init__(self, ant_id, color, position, hp=1):
        self.id = ant_id
        self.color = color  # "black" or "red"
        self.position = position
        self.hp = hp
        self.next_node = None
        self.active = True
        self.selected = False

    def plan_move(self, target):
        self.next_node = target

    def execute_move(self):
        if self.next_node:
            self.position = self.next_node
            self.next_node = None
