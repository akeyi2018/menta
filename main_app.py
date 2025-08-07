import tkinter as tk
import tkinter.ttk as ttk

from app_model import Zaiko, Money, Auto_machine
from app_view import VMoney, VDrink, Roulette
from backyard import Backyard

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.master.title("自動販売機")       # ウィンドウタイトル
        # self.master.geometry("1200x500") # ウィンドウサイズ(幅x高さ)
        self.font = ("MSゴシック", "14")

        # ルーレット
        self.ru = Roulette(self)

        # 商品リスト
        self.auto_machine = Auto_machine()

        # 在庫クラス
        self.zaiko = Zaiko()

        # 飲み物クラス
        self.v_drink = VDrink(self)

        # お金クラス
        self.initial_money()

        # メンテナンス切り替        
        self.maintenance_button()

        self.adjust_window_size()

    def initial_money(self):
        self.m_money = Money()
        self.v_money = VMoney(self)

    def maintenance_button(self):
        self.frame_lbl = tk.LabelFrame(root, text='メンテナンス', bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.frame_lbl.grid(column=1, row=1, padx=10, pady=10, sticky="nsew")
        # 売上ボタン
        self.total_sales = tk.Button(self.frame_lbl, text="maintenance", font=self.font, command=self.mainte)
        self.total_sales.grid(padx=5,pady=5)

    def mainte(self):
        back_yard = Backyard(self)
        back_yard.open_sub_window()

    def adjust_window_size(self):
        # レイアウトを更新
        self.master.update_idletasks()

        # フレームの右端と下端を計算
        frames = [self.frame_lbl]
        max_width = 0
        max_height = 0

        for frame in frames:
            x = frame.winfo_x()
            y = frame.winfo_y()
            width = frame.winfo_width()
            height = frame.winfo_height()

            # 右端と下端の最大値を計算
            max_width = max(max_width, x + width)
            max_height = max(max_height, y + height)
        
        
        # 親ウィンドウのサイズを調整
        self.master.geometry(f"{max_width + 20}x{max_height + 20}")  # 余白を追加

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()