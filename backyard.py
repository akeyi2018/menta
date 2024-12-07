import tkinter as tk
from app_model import Zaiko

class Backyard:
    def __init__(self, root) -> None:
        self.root = root
        self.auto_machine = self.root.auto_machine
        self.key_list = list(self.auto_machine.drink_list.keys())
        self.zaiko_list = []
        
    def open_sub_window(self):
        zaiko = Zaiko()
        sub_win = tk.Toplevel(self.root.master)
        sub_win.title('メンテナンス')
        sub_win.geometry('300x500')

        # フレーム
        self.label_frame = tk.LabelFrame(sub_win, text='在庫', bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.label_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        
        row = 0
        for name in self.key_list:
            lbl = tk.Label(self.label_frame, text=name +':')
            txt = str(zaiko.get_product_size(name))
            zaiko_lbl = tk.Label(self.label_frame,text=txt)
            btn = tk.Button(self.label_frame,text='add', command=lambda n=name:self.add_inventory(n))
            lbl.grid(row=row, column=0, padx=5, pady=5)
            zaiko_lbl.grid(row=row, column=1, padx=5, pady=5)
            btn.grid(row=row, column=2, padx=5, pady=5)
            self.zaiko_list.append(zaiko_lbl)
            row += 1

        # 閉じるボタンの追加
        close_button = tk.Button(sub_win, text="閉じる", command=sub_win.destroy)
        close_button.grid(row=1, column=0, padx=10, pady=10)

    def add_inventory(self, name):
        zaiko = Zaiko()
        zaiko.add_product(name)
        self.update_zaiko_label(name)


    def update_zaiko_label(self, name):
        for n, v in zip(self.key_list, self.zaiko_list):
            if name == n:
                zaiko = Zaiko()
                txt = str(zaiko.get_product_size(name))
                v.config(text=txt)

