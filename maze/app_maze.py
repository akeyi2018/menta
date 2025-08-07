import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from astar_with_route import *
from layout_config import Layout
import time

class MainGUI(tk.Frame):

    def __init__(self, master=None) -> None:

        super().__init__(master)

        self.master.title('Maze')
        self.master.geometry(f'{Layout.win_width}x{Layout.win_height}')

        self.ch = None
        self.goal_lbl = None

        # 迷路
        self.maze = Maze()

        self.image = self.set_image()

        # cal
        self.main = Main()

        self.set_canvas()

        self.view_maze(self.maze.maze)

        self.view_init()

        self.create_button()

    def set_canvas(self):
        x_len = len(self.maze.maze) + 2
        y_len = len(self.maze.maze[0]) + 2
        self.canvas = tk.Canvas(root, 
                                width=x_len*Layout.tile_size,
                                height=y_len*Layout.tile_size)
        self.canvas.create_rectangle(0,0,x_len*Layout.tile_size,
                                     y_len*Layout.tile_size,
                                     width=Layout.tile_size*2, outline='blue')
        self.canvas.place(x=0,y=0)

    def create_button(self):
        span = 40
        for x, g in enumerate(self.main.goals):
            btn = ttk.Button(root, text='Route:' + str(x), command=lambda p=x: self.view_route(p))
            btn.place(x=Layout.button_x, y= 100 + span*x)

    def set_image(self):
        image_path = './images/ch.png'
        pil_image = Image.open(image_path)
        self.pil_image = pil_image.resize((Layout.tile_size, Layout.tile_size), Image.LANCZOS)
        return ImageTk.PhotoImage(self.pil_image)

    def view_maze(self, maze):
        image_path = ['./images/bk.png',
                      './images/wall.png']
        
        for y, outer in enumerate(maze):
            for x, inner in enumerate(outer):
                image = Image.open(image_path[inner])
                image = image.resize((Layout.tile_size, Layout.tile_size), Image.LANCZOS)
                image.putalpha(int(0.5*255))
                image_tk = ImageTk.PhotoImage(image)
                lbl = ttk.Label(root, image=image_tk)
                lbl.image = image_tk
                lbl.place(x=(x+1)*Layout.tile_size, y=(y+1)*Layout.tile_size)

    def view_init(self):
        self.ch = ttk.Label(root, image=self.image)
        self.ch.place(x=Layout.tile_size, y=Layout.tile_size)

    def set_goal(self, x, y):
        if self.goal_lbl:
            self.goal_lbl.destroy()
        image = Image.open('./images/g.png')
        image = image.resize((Layout.tile_size, Layout.tile_size), Image.LANCZOS)
        image.putalpha(int(0.5*255))
        image_tk = ImageTk.PhotoImage(image)
        self.goal_lbl = ttk.Label(root, image=image_tk)
        self.goal_lbl.image = image_tk
        self.goal_lbl.place(x=(x+1)*Layout.tile_size, y=(y+1)*Layout.tile_size)

    def view_route(self, x):
        paths = self.main.get_results()
        goals = self.main.goals
        self.set_goal(goals[x][1], goals[x][0])
        root.update()
        for p in paths[x]:
            x = p[0]
            y = p[1]

            # 移動するタイルの画像を設定する
            if self.ch is None:
                self.image = self.set_image()
                self.ch = ttk.Label(root, image=self.image)
                self.ch.image = self.image
                self.ch.place(x=(y+1) * Layout.tile_size, y=(x+1) * Layout.tile_size)
            else:
                self.ch.place(x=(y+1) * Layout.tile_size, y=(x+1) * Layout.tile_size)

            self.ch.lift()

            self.ch.image = self.image
            root.update()

            time.sleep(0.1)

if __name__ == "__main__":

    root = tk.Tk()
    app = MainGUI(master=root)

    app.mainloop()
