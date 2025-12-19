import tkinter as tk
import socket
from loguru import logger
from common_proc import set_config

class Application(tk.Frame):

    IP = '127.0.0.1'
    port_01 = 5051
    port_02 = 5052
    port_03 = 5053
    port_04 = 5054
    port_05 = 5055
    port_06 = 5056

    SEND_INTERVAL = 10  # ms（例: 100msごとに送信）

    def __init__(self, master=None):
        super().__init__(master)

        # 設定情報
        self.config_data = set_config()
        self.ball_count_min, self.ball_count_max = self.config_data["BALL_COUNT_MIN"], self.config_data["BALL_COUNT_MAX"]
        self.radius_min, self.radius_max = self.config_data["RADIUS_MIN"], self.config_data["RADIUS_MAX"]  

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.master.title("Python Sender")
        self.master.geometry("1100x500")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.chanel_01 = tk.LabelFrame(self.master, text=self.port_01)
        self.chanel_01.grid(row=0, column=0, padx=10, pady=10)

        self.chanel_02 = tk.LabelFrame(self.master, text=self.port_02)
        self.chanel_02.grid(row=0, column=1, padx=10, pady=10)

        self.chanel_03 = tk.LabelFrame(self.master, text=self.port_03)
        self.chanel_03.grid(row=0, column=2, padx=10, pady=10)

        self.chanel_04 = tk.LabelFrame(self.master, text=self.port_04)
        self.chanel_04.grid(row=1, column=0, padx=10, pady=10)

        self.chanel_05 = tk.LabelFrame(self.master, text=self.port_05)
        self.chanel_05.grid(row=1, column=1, padx=10, pady=10)

        self.chanel_06 = tk.LabelFrame(self.master, text=self.port_06)
        self.chanel_06.grid(row=1, column=2, padx=10, pady=10)

        self.scale_val_one = tk.IntVar()
        self.scale_val_two = tk.IntVar()
        self.roll_x = tk.IntVar()
        self.roll_y = tk.IntVar()
        self.roll_z = tk.IntVar()

        self.scale_roll_x = tk.IntVar()
        self.scale_roll_y = tk.IntVar()
        self.scale_roll_z = tk.IntVar()
        self.alpha_scale = tk.IntVar()

        self.scale_val_three = tk.IntVar()
        self.scale_val_four = tk.IntVar()

        self.initial_scale()

        self.scale_roll_x.set(128)
        self.scale_roll_y.set(128)
        self.scale_roll_z.set(128)
        self.alpha_scale.set(128)

        self.scale_val_three.set(int(abs(self.radius_max-self.radius_min)/2))

        # 定期送信を開始
        self.periodic_send()

    def initial_scale(self):

        # チャンネル01
        tk.Label(self.chanel_01, text='球体：左右').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.chanel_01, text='球体：前後').grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.chanel_01, text='回転：X').grid(row=0, column=2, padx=10, pady=10)
        tk.Label(self.chanel_01, text='回転：Y').grid(row=2, column=2, padx=10, pady=10)
        tk.Label(self.chanel_01, text='回転：Z').grid(row=4, column=2, padx=10, pady=10)


        # チャンネル02
        tk.Label(self.chanel_02, text='球体色: R').grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.chanel_02, text='球体色: G').grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.chanel_02, text='球体色: B').grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self.chanel_02, text='球体透明度: A').grid(row=6, column=0, padx=10, pady=5)

        # チャンネル03
        tk.Label(self.chanel_03, text='球体: 半径').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.chanel_03, text='球体: 個数').grid(row=2, column=0, padx=10, pady=10)

        # チャンネル01 配下
        tk.Scale(self.chanel_01, from_=-100, to=100, length=200, orient='horizontal',
                 variable=self.scale_val_one, sliderlength=30, width=30, 
                 showvalue=True).grid(row=1,column=0, rowspan=6, padx=10, pady=10)
        
        tk.Scale(self.chanel_01, from_=100, to=-100, length=200, variable=self.scale_val_two,
                 sliderlength=30, width=30, 
                 showvalue=True).grid(row=1,column=1, rowspan=6, padx=10, pady=10)
        
        tk.Scale(self.chanel_01, from_=-100, to=100, length=200, orient='horizontal',
                 variable=self.roll_x, sliderlength=30, width=30, 
                 showvalue=True).grid(row=1,column=2, padx=10, pady=5)
        tk.Scale(self.chanel_01, from_=-100, to=100, length=200, orient='horizontal',
                 variable=self.roll_y, sliderlength=30, width=30, 
                 showvalue=True).grid(row=3,column=2, padx=10, pady=5)
        tk.Scale(self.chanel_01, from_=-100, to=100, length=200, orient='horizontal',
                 variable=self.roll_z, sliderlength=30, width=30, 
                 showvalue=True).grid(row=5,column=2, padx=10, pady=5)
        
        # チャンネル02 配下
        tk.Scale(self.chanel_02, from_=0, to=255, length=200, orient='horizontal',
                 variable=self.scale_roll_x, sliderlength=30, width=30, 
                 showvalue=True).grid(row=1,column=0, padx=10, pady=5)
        tk.Scale(self.chanel_02, from_=0, to=255, length=200, orient='horizontal',
                 variable=self.scale_roll_y, sliderlength=30, width=30, 
                 showvalue=True).grid(row=3,column=0, padx=10, pady=5)
        tk.Scale(self.chanel_02, from_=0, to=255, length=200, orient='horizontal',
                 variable=self.scale_roll_z, sliderlength=30, width=30, 
                 showvalue=True).grid(row=5,column=0, padx=10, pady=5)
        tk.Scale(self.chanel_02, from_=0, to=255, length=200, orient='horizontal',
                 variable=self.alpha_scale, sliderlength=30, width=30, 
                 showvalue=True).grid(row=7,column=0, padx=10, pady=5)
        
        # チャンネル03 配下
        tk.Scale(self.chanel_03, from_=self.radius_min, to=self.radius_max, 
                 length=200, orient='horizontal',
                 variable=self.scale_val_three, sliderlength=50, width=50, 
                 showvalue=True).grid(row=1,column=0, padx=10, pady=10)
        
        tk.Scale(self.chanel_03, from_=self.ball_count_min, to=self.ball_count_max,
                 length=200, orient='horizontal',
                 variable=self.scale_val_four, sliderlength=50, width=50, 
                 showvalue=True).grid(row=3,column=0, padx=10, pady=10)
        
    def func_normalize(self, value, input_min, input_max, output_min, output_max):
        """
        入力値を指定された範囲に正規化する関数
        """
        # 線形変換を使用して値を正規化
        normalized_value = ((value - input_min) / (input_max - input_min)) * (output_max - output_min) + output_min
        return normalized_value
        
    def periodic_send(self):
        sensive = 0.01
        # chanel_01送信
        x = float(self.scale_val_one.get())
        y = float(self.scale_val_two.get())
        ro_x = float(self.roll_x.get()*sensive)
        ro_y = float(self.roll_y.get()*sensive)
        ro_z = float(self.roll_z.get()*sensive)
        message = f'{x} {y} {ro_x} {ro_y} {ro_z}'
        self.sock.sendto(message.encode('utf-8'), (self.IP, self.port_01))

        # chanel_02送信
        # 正規化
        roll_x = self.func_normalize(
            self.scale_roll_x.get(),
            0,
            255,
            0,
            1.0)
        roll_y = self.func_normalize(
            self.scale_roll_y.get(),
            0,
            255,
            0,
            1.0)
        roll_z = self.func_normalize(
            self.scale_roll_z.get(),
            0,
            255,
            0,
            1.0)
        alpha = self.func_normalize(
            self.alpha_scale.get(),
            0,
            255,
            0,
            1.0
        )
        message2 = f'{float(roll_x)} {float(roll_y)} {float(roll_z)} {float(alpha)}'

        self.sock.sendto(message2.encode('utf-8'), (self.IP, self.port_02))

        # chanel_03送信
        # radius = self.func_normalize(
            # self.scale_val_three.get(),
        #     self.radius_min, self.radius_max,
        #     0.05,
        #     0.5)
        radius = self.scale_val_three.get()
        ball_count = self.scale_val_four.get()
        message3 = f'{int(radius)} {int(ball_count)}'
        self.sock.sendto(message3.encode('utf-8'), (self.IP, self.port_03))

        # 次回予約
        self.master.after(self.SEND_INTERVAL, self.periodic_send)

    def on_close(self):
        self.sock.close()
        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()