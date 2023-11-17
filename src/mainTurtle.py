import turtle, os

class MainTurtle(turtle.RawTurtle):
    def __init__(self, canvas, current_directory, step_move=20, step_turn=15):
        super().__init__(canvas)
        self.speed(0)
        self.step_move = step_move
        self.step_turn = step_turn
        self.lifes = 2
        self.status = True
        self.current_directory = current_directory

        # Register event handlers
        canvas.onkey(self.turn_back, 'Up')
        canvas.onkey(self.turn_left, 'Left')
        canvas.onkey(self.turn_right, 'Right')
        canvas.listen()

        file_directory = os.path.join(self.current_directory, 'turtle_0.gif')
        self.shape(file_directory)

    def turn_head(self):
        angle = int(self.heading())
        file_directory = os.path.join(self.current_directory, 'turtle_')
        file_directory += str(angle) + '.gif'
        self.shape(file_directory)

    def turn_left(self):
        self.left(self.step_turn)
        self.turn_head()

    def turn_right(self):
        self.right(self.step_turn)
        self.turn_head()

    def turn_back(self):
        self.right(180)
        self.turn_head()
        
    