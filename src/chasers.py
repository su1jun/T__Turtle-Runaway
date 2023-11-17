import turtle, random, os, math

class chaser(turtle.RawTurtle):
    def __init__(self, canvas, radius, step_move, step_turn):
        super().__init__(canvas)
        self.speed(0)
        self.radius = radius
        self.radius2 = radius * radius
        self.step_move = step_move
        self.step_turn = step_turn
        self.penup()
        
    def is_catched(self, opp_pos):
        my_pos = [self.xcor(), self.ycor()]
        val = (opp_pos[0] - my_pos[0]) ** 2 + (opp_pos[1] - my_pos[1]) ** 2
        # print(f"val : {val}, type : {type(self)}, limit : {self.radius2}")
        return val < self.radius2
    
    def run_ai(self, opp_pos):
        raise NotImplementedError("Make method")
        # 작동 관련 이벤트 작성        
    
class PurpleMushroom(chaser):
    def __init__(self, canvas, current_directory, radius=4, step_move=10, step_turn=30):
        super().__init__(canvas, radius, step_move, step_turn)
        file_directory = os.path.join(current_directory, 'purple_mushroom.gif')
        self.shape(file_directory)
        
    def run_ai(self, opp_pos=False):
        x_out = self.xcor() <= -300 or self.xcor() >= 300
        y_out = self.ycor() <= -300 or self.ycor() >= 300
        if x_out and y_out:
            self.backward(20)
            self.left(180)
        else:
            if x_out:
                self.backward(20)
                self.left(180)
            if y_out:
                self.backward(20)
                self.left(180)
                
        mode = random.randint(0, 2)
        if mode == 0:
            self.left(self.step_turn)
        elif mode == 1:
            self.right(self.step_turn)
        self.forward(self.step_move)
            
class RottenMushroom(chaser):
    def __init__(self, canvas, current_directory, radius=4 , step_move=10, step_turn=30):
        super().__init__(canvas, radius, step_move // 2, step_turn)
        file_directory = os.path.join(current_directory, 'rotten_mushroom.gif')
        self.shape(file_directory)
        
    def run_ai(self, opp_pos):
        my_pos = [self.xcor(), self.ycor()]
        slope = (opp_pos[1] - my_pos[1]) / (opp_pos[0] - my_pos[0])
        radian = math.atan(slope)
        degree = math.degrees(radian)
        
        # print(f"goto : {degree}, my : {self.heading()}")
        if my_pos[0] <= opp_pos[0]:
            self.setheading(degree)
        else:
            self.setheading(degree - 180)
        self.forward(self.step_move)