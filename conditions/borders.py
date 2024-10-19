class BaseBorder:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
    
    def check_border(self, machine):
        if machine.coord.x < 0 or machine.coord.x >= self.width or machine.coord.y < 0 or machine.coord.y >= self.height:
            return True
        return False
    
class PeriodicBorder(BaseBorder):
    def check_border(self, machine):
        machine.coord.x = machine.coord.x % self.width
        machine.coord.y = machine.coord.y % self.height

        return False
