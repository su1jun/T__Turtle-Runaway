import os, turtle
import tkinter as tk
from runawayGame import RunawayGame

def draw_info(time, score):
    frame1_ety1.delete(0, tk.END)
    frame1_ety1.insert(0, time)

    frame1_ety2.delete(0, tk.END)
    frame1_ety2.insert(0, score)

if __name__ == '__main__':
    try:
        # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
        root = tk.Tk()
        root.resizable(width=False, height=False)
        frame1 = tk.Frame(root)
        frame1.pack(fill="x", padx=5, pady=5, ipady=8)
        
        my_font = ("Garamond", 12)

        frame1_lbl1 = tk.Label(frame1, text=" Time : ", font=my_font)
        frame1_lbl1.pack(side="left", padx=20, pady=2)

        frame1_ety1 = tk.Entry(frame1, font=my_font, width=14)
        frame1_ety1.pack(side="left", padx=6, pady=2)

        frame1_lbl2 = tk.Label(frame1, text="  Stage : ", font=my_font)
        frame1_lbl2.pack(side="left", padx=20, pady=2)
        
        frame1_ety2 = tk.Entry(frame1, font=my_font, width=14)
        frame1_ety2.pack(side="left", padx=6, pady=2)

        frame1_lbl3 = tk.Label(frame1, text="  Score : ", font=my_font)
        frame1_lbl3.pack(side="left", padx=20, pady=2)
        
        frame1_ety3 = tk.Entry(frame1, font=my_font, width=14)
        frame1_ety3.pack(side="left", padx=6, pady=2)
        
        current_directory = os.getcwd()
        # os.pardir
        current_directory = os.path.join(current_directory, 'assets')

        root.title("Turtle Runaway")
        canvas = tk.Canvas(root, width=700, height=700)
        canvas.pack()
        screen = turtle.TurtleScreen(canvas)
        screen.bgpic(os.path.join(current_directory, 'background.gif'))

        file_list = ['red_mushroom', 'green_mushroom',
                    'purple_mushroom', 'fire_flower',
                    'rotten_mushroom', 'star', 'timer', 'coin']
        turtle_imgs = ['turtle_' + str(i) + '.gif' for i in range(0, 360, 15)]
        
        for fime_name in file_list:
            fime_name += '.gif'
            screen.addshape(os.path.join(current_directory, fime_name))
        
        for fime_name in turtle_imgs:
            screen.addshape(os.path.join(current_directory, fime_name))

        # TODO) Change the follows to your turtle if necessary
        game = RunawayGame(screen, root, frame1_ety1, frame1_ety2, frame1_ety3, current_directory)
        game.start()
        screen.mainloop()
    except Exception as e:
        pass
        # print(f"An error occurred: {e}")
    finally:
        try:
            # turtle 창 상태 확인 후 해제
            if turtle.getscreen():
                turtle.bye()
        except tk.TclError:
            pass  # 이미 닫힌 경우 오류 무시

        try:
            # tkinter 창 상태 확인 후 해제
            if root.winfo_exists():
                root.destroy()
        except tk.TclError:
            pass  # 이미 닫힌 경우 오류 무시