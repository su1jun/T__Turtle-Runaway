import turtle, os

class Item(turtle.RawTurtle):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.speed(0)
        self.penup()

class Coin(Item): # score +50
    def __init__(self, canvas, current_directory):
        super().__init__(canvas)
        file_directory = os.path.join(current_directory, 'coin.gif')
        self.shape(file_directory)

class RedMushroom(Item): # score +100
    def __init__(self, canvas, current_directory):
        super().__init__(canvas)
        file_directory = os.path.join(current_directory, 'red_mushroom.gif')
        self.shape(file_directory)

class FireFlower(Item): # score +200
    def __init__(self, canvas, current_directory):
        super().__init__(canvas)
        file_directory = os.path.join(current_directory, 'fire_flower.gif')
        self.shape(file_directory)

class Star(Item): # score +300
    def __init__(self, canvas, current_directory):
        super().__init__(canvas)
        file_directory = os.path.join(current_directory, 'star.gif')
        self.shape(file_directory)
        
class Timer(Item): # time +
    def __init__(self, canvas, current_directory):
        super().__init__(canvas)
        file_directory = os.path.join(current_directory, 'timer.gif')
        self.shape(file_directory)
