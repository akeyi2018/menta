import tkinter as tk
import tkinter.ttk as ttk

from app_model import Zaiko, Money, Auto_machine
from app_view import VMoney, VDrink, Roulette

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.master.title("自動販売機")       # ウィンドウタイトル
        self.master.geometry("1200x500") # ウィンドウサイズ(幅x高さ)
        self.font = ("MSゴシック", "14")

        # maintenance
        self.maintenance_flag = False

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

    def initial_money(self):
        self.m_money = Money()
        self.v_money = VMoney(self)

    def maintenance_button(self):
        # 売上ボタン
        self.total_sales = tk.Button(root, text="maintenance", font=self.font, command=self.mainte)
        self.total_sales.place(x=100, y= 280)

    def mainte(self):
        if self.maintenance_flag:
            self.maintenance_flag = False
        else:
            self.maintenance_flag = True

        self.v_money.update_maintenance_menu()
        self.v_drink.update_maintenance_menu()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()