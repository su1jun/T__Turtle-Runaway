import turtle, time, random, sys
import tkinter as tk
from mainTurtle import MainTurtle
import items as itm
import chasers as chs

class RunawayGame:
    def __init__(self, canvas, root, ob1, ob2, ob3, current_directory, game_duration=60):
        self.canvas = canvas
        self.root = root
        self.ob1 = ob1 # time entry
        self.ob2 = ob2 # stage entry
        self.ob3 = ob3 # score entry
        
        self.current_directory = current_directory
        
        self.coins = 0 # type : int, the number of object
        self.timers = 0 # type : int, the number of object
        self.items = 0 # tpye : int, the number of object
        self.chasers = [] # tpye : list, information of object
        
        self.grid = [[0 for _ in range(20)] for _ in range(20)] # Initialize 'grid' for object`s position information
        self.start_time = 0 # Initialize 'start_time'
        self.setting_time = game_duration # Initialize 'setting_time'
        self.current_stage = 0 # Initialize 'stage'
        self.score = 0 # Initialize 'score'
        
        # Initialize 'runner'(Main Character)
        self.runner = MainTurtle(self.canvas, current_directory)
        self.runner.penup()

        # Initialize game setting
        self.stage_setting_g = { # 코인 갯수, 테마 아이템 갯수
            1 : [25, 10],
            2 : [25, 10],
            3 : [25, 10]
        }
        self.stage_setting_e = { # 적 개체수(랜덤형, 추적형), (적의 최소 속도, 최대 속도)
            1 : [[1, 0], [12, 16]],
            2 : [[0, 1], [16, 20]],
            3 : [[2, 0], [20, 24]],
        }
        self.stage_setting_i = { # 아이템 최대 갯수, 아이템 드랍 확률
            1 : [1, 0.03],
            2 : [2, 0.03],
            3 : [3, 0.03],
        }

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(self.canvas)
        self.drawer.hideturtle()
        self.drawer.color("ivory")
        self.drawer.speed(0)
        self.drawer.penup()
        
    # update window(tkinter)
    def draw_info(self, time, stage, score):
        self.ob1.delete(0, tk.END)
        self.ob1.insert(0, time)

        self.ob2.delete(0, tk.END)
        self.ob2.insert(0, stage)

        self.ob3.delete(0, tk.END)
        self.ob3.insert(0, score)
        
    # def draw_border(self):
    #     mypen = turtle.RawTurtle(self.canvas)
    #     mypen.penup()
    #     mypen.speed(0)
    #     mypen.setposition(-320, -320)
    #     mypen.pendown()
    #     mypen.pensize(3)
    #     for _ in range(4):
    #         mypen.forward(640)
    #         mypen.left(90)
        
        # mypen.pensize(1)
        # spacing = 40
        # num_lines = 15
        # # 수직선 그리기
        # for i in range(-num_lines//2, num_lines//2 + 1):
        #     mypen.penup()
        #     mypen.goto(i * spacing, -num_lines*spacing/2)
        #     mypen.pendown()
        #     mypen.goto(i * spacing, num_lines*spacing/2)
    
        # # 수평선 그리기
        # for i in range(-num_lines//2, num_lines//2 + 1):
        #     mypen.penup()
        #     mypen.goto(-num_lines*spacing/2, i * spacing)
        #     mypen.pendown()
        #     mypen.goto(num_lines*spacing/2, i * spacing)
            
        # mypen.hideturtle()

        # self.canvas.update()

        # self.start()
        
    def start(self, ai_timer_msec=50):
        self.runner.setpos((0, 0))
        self.runner.setheading(0)
        
        # TODO) You can do something here and follows.
        
        self.drawer.undo()
        self.drawer.setpos(0, 0)
        self.drawer.write(f"Hello Turtle!", align="center", font=("Georgia", 44, "bold"))
        time.sleep(1)
            
        self.start_time = int(time.time())  # 게임 시작 시간
        self.ai_timer_msec = ai_timer_msec
        self.score = 0

        self.current_stage = 1
        self.load_stage(self.current_stage)
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        # for i in self.grid:
        #     print(*i)

    def load_stage(self, stage):
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(0, 0)
        self.drawer.clear()

        ssg = self.stage_setting_g[stage]
        self.coins = 0
        while ssg[0] > self.coins:
            goal_x = random.randint(-7, 6) + 7
            goal_y = random.randint(-7, 6) + 7
            
            if self.grid[goal_x][goal_y]:
                continue
            
            self.grid[goal_x][goal_y] = itm.Coin(self.canvas, self.current_directory)
            goal = self.grid[goal_x][goal_y]
            goal.goto((goal_x - 7) * 40 + 20, (goal_y - 7) * 40 + 20)
                        
            # 생성 개체
            self.coins += 1
            self.drawer.undo()
            self.drawer.write(f"Ready Stage {stage} !", align="center", font=("Georgia", 40, "bold"))
            
        while ssg[1] > self.items:
            goal_x = random.randint(-7, 6) + 7
            goal_y = random.randint(-7, 6) + 7
            
            if self.grid[goal_x][goal_y]:
                continue
            
            if stage == 1:
                self.grid[goal_x][goal_y] = itm.RedMushroom(self.canvas, self.current_directory)
            elif stage == 2:
                self.grid[goal_x][goal_y] = itm.FireFlower(self.canvas, self.current_directory)
            else:
                self.grid[goal_x][goal_y] = itm.Star(self.canvas, self.current_directory)
                
            goal = self.grid[goal_x][goal_y]
            goal.goto((goal_x - 7) * 40 + 20, (goal_y - 7) * 40 + 20)
            self.drawer.undo()
            self.drawer.write(f"Ready Stage {stage} !", align="center", font=("Georgia", 40, "bold"))
                        
            # 생성 개체
            self.items += 1
        
        sse = self.stage_setting_e[stage]
        for _ in range(sse[0][0]):
            chaser = chs.PurpleMushroom(self.canvas, current_directory = self.current_directory, radius=25, step_move=random.randint(sse[1][0], sse[1][1]))
            loc_var = random.randint(1, 4)
            # 생성 위치 설정
            if loc_var == 1:
                chaser.goto((-280, random.randint(-280, 280)))
            elif loc_var == 2:
                chaser.goto((280, random.randint(-280, 280)))
            elif loc_var == 3:
                chaser.goto((random.randint(-280, 280), -280))
            else:
                chaser.goto((random.randint(-280, 280), 280))
            self.chasers.append(chaser)

        for _ in range(sse[0][1]):
            chaser = chs.RottenMushroom(self.canvas, current_directory = self.current_directory, radius=25, step_move=random.randint(sse[1][0], sse[1][1]))
            loc_var = random.randint(1, 4)
            # 생성 위치 설정
            if loc_var == 1:
                chaser.goto((-280, random.randint(-280, 280)))
            elif loc_var == 2:
                chaser.goto((280, random.randint(-280, 280)))
            elif loc_var == 3:
                chaser.goto((random.randint(-280, 280), -280))
            else:
                chaser.goto((random.randint(-280, 280), 280))
            self.chasers.append(chaser)

        self.canvas.update()
        self.drawer.undo()
                
    def end_game(self, code):
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(0, 30)
        self.drawer.pendown()
        self.drawer.write(f"{code}", align="center", font=("Georgia", 40, "bold"))
        time.sleep(1)
        self.drawer.penup()
        self.drawer.setpos(0, -30)
        self.drawer.pendown()
        self.drawer.write(f"Your Score : {self.score}", align="center", font=("Georgia", 40, "bold"))
        time.sleep(3)
        self.drawer.clear()
        self.drawer.penup()
        self.drawer.setpos(0, 0)
        self.drawer.pendown()
        self.drawer.write(f"Thank you for playing!", align="center", font=("Georgia", 40, "bold"))
        time.sleep(3)
        quit()
    
    def clear_game(self):
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(0, 30)
        self.drawer.pendown()
        self.drawer.write(f"Awesome!", align="center", font=("Georgia", 40, "bold"))
        time.sleep(1)
        self.drawer.penup()
        self.drawer.setpos(0, -30)
        self.drawer.pendown()
        self.drawer.write(f"Your Score : {self.score}", align="center", font=("Georgia", 40, "bold"))
        time.sleep(3)
        self.drawer.clear()
        self.drawer.penup()
        self.drawer.setpos(0, 30)
        self.drawer.pendown()
        self.drawer.write(f"You Clear This Game!", align="center", font=("Georgia", 40, "bold"))
        time.sleep(1)
        self.drawer.penup()
        self.drawer.setpos(0, -30)
        self.drawer.pendown()
        self.drawer.write(f"Thank you for playing:)", align="center", font=("Georgia", 40, "bold"))
        time.sleep(3)
        sys.exit(0) 

    def step(self):
        # calculate time
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.setting_time - int(elapsed_time))

        min_str = str(remaining_time // 60).zfill(2)
        sec_str = str(remaining_time % 60).zfill(2)

        self.draw_info(f'{min_str}:{sec_str}', self.current_stage, self.score)

        # TODO) You can do something here and follows.

        # Stage Check
        if self.items < 1:
            if self.current_stage < 3:
                self.setting_time += 4 # offset time
                self.current_stage += 1
                self.load_stage(self.current_stage)
            else:
                self.end_game("Game Clear!")
            
        if remaining_time <= 0:
            self.end_game("Time Over!")

        if self.score >= 7500:
            self.clear_game()

        self.drawer.clear()

        runner_pos = [self.runner.xcor(), self.runner.ycor()]

        # Main Character Action
        runner_head = self.runner.heading()
        # print(f"{runner_pos[0], runner_pos[1]}, {runner_head}")
        if runner_pos[0] <= -300 and runner_pos[1] <= -300 and (runner_head > 180 and runner_head < 270):
            self.runner.backward(10)
            self.runner.left(180)
            self.runner.turn_head()
        elif runner_pos[0] >= 300 and runner_pos[1] <= -300 and (runner_head > 270 and runner_head < 360):
            self.runner.backward(10)
            self.runner.left(180)
            self.runner.turn_head()
        elif runner_pos[0] <= -300 and runner_pos[1] >= 300 and (runner_head > 90 and runner_head < 180):
            self.runner.backward(10)
            self.runner.left(180)
            self.runner.turn_head()
        elif runner_pos[0] >= 300 and runner_pos[1] >= 300 and (runner_head > 0 and runner_head < 90):
            self.runner.backward(10)
            self.runner.left(180)
            self.runner.turn_head()
        else:
            if runner_pos[0] <= -300 and (runner_head > 90 and runner_head < 270):
                self.runner.backward(10)
                self.runner.left(180)
                self.runner.turn_head()
                
            if runner_pos[0] >= 300 and (runner_head < 90 or runner_head > 270):
                self.runner.backward(10)
                self.runner.left(180)
                self.runner.turn_head()
            
            if runner_pos[1] <= -300 and (runner_head < 360 and runner_head > 180):
                self.runner.backward(10)
                self.runner.left(180)
                self.runner.turn_head()
                
            if runner_pos[1] >= 300 and (runner_head < 180 and runner_head > 0):
                self.runner.backward(10)
                self.runner.left(180)
                self.runner.turn_head()
            
        self.runner.forward(self.runner.step_move)

        # Chaser Action
        for chaser in self.chasers:
            if chaser.is_catched(runner_pos):
                self.end_game("Game Over!")
            chaser.run_ai(runner_pos)
        
        # Collision Event
        runner_x = int(runner_pos[0]) // 40 + 7
        runner_y = int(runner_pos[1]) // 40 + 7
        
        if self.grid[runner_x][runner_y]:
            # print(f"type : {type(self.grid[runner_x][runner_y])}")
            # print(f"m : ({runner_x}, {runner_y}), cor : ({self.runner.xcor()}, {self.runner.ycor()}), o : {self.grid[runner_x][runner_y]}, ")

            goal_x = (runner_x - 7) * 40 + 20
            goal_y = (runner_y - 7) * 40 + 20
            self.drawer.penup()
            self.drawer.setpos(goal_x, goal_y)
            self.drawer.pendown()

            if isinstance(self.grid[runner_x][runner_y], itm.Coin):
                self.score += 20
                self.grid[runner_x][runner_y].hideturtle()
                self.grid[runner_x][runner_y] = 0
                self.drawer.write(f"+20", align="center", font=("Arial", 22, "normal"))
            
            elif isinstance(self.grid[runner_x][runner_y], itm.Timer):
                self.timers -= 1
                self.setting_time += 10
                self.grid[runner_x][runner_y].hideturtle()
                self.grid[runner_x][runner_y] = 0
                self.drawer.write(f"Time +10!", align="center", font=("Arial", 22, "normal"))
                
            else:
                self.items -= 1
                if isinstance(self.grid[runner_x][runner_y], itm.RedMushroom):
                    self.score += 100
                    self.grid[runner_x][runner_y].hideturtle()
                    self.grid[runner_x][runner_y] = 0
                    self.drawer.write(f"+100", align="center", font=("Arial", 22, "normal"))
                    
                elif isinstance(self.grid[runner_x][runner_y], itm.FireFlower):
                    self.score += 200
                    self.grid[runner_x][runner_y].hideturtle()
                    self.grid[runner_x][runner_y] = 0
                    self.drawer.write(f"+200", align="center", font=("Arial", 22, "normal"))

                elif isinstance(self.grid[runner_x][runner_y], itm.Star):
                    self.score += 300
                    self.grid[runner_x][runner_y].hideturtle()
                    self.grid[runner_x][runner_y] = 0
                    self.drawer.write(f"+300", align="center", font=("Arial", 22, "normal"))
                    
        # Timer
        if self.timers < self.stage_setting_i[self.current_stage][0]:
            if random.random() <= self.stage_setting_i[self.current_stage][1]:
                current_timers = self.timers + 1
                while self.timers < current_timers:
                    goal_x = random.randint(-7, 6) + 7
                    goal_y = random.randint(-7, 6) + 7
                    
                    if self.grid[goal_x][goal_y]:
                        continue
                    
                    self.grid[goal_x][goal_y] = itm.Timer(self.canvas, self.current_directory)
                    goal = self.grid[goal_x][goal_y]
                    goal.goto((goal_x - 7) * 40 + 20, (goal_y - 7) * 40 + 20)
                    
                    # 생성 개체
                    self.timers += 1
            
        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        