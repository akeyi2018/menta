import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import random

class Roulette:
    def __init__(self, parent) -> None:
        self.root = parent.master
        self.roulette_list = []
        self.add_roulette_ui()
        self.pos_r = 0

    def add_roulette_ui(self):
        # "回す"ボタン
        # self.mv = tk.Button(self.root, text="回す", command=self.roll_roulette)
        # self.mv.place(x=100, y=10)
        self.lbl = tk.Label(self.root, text='当たり')
        self.lbl.place(x=175, y=30)

        # 初期のイメージ設定
        original_image = Image.open("en2.png")
        resized_image = original_image.resize((25, 23))
        self.loadimage = ImageTk.PhotoImage(resized_image)

        # ボタンを10個生成してリストに追加
        for r in range(9):
            btn = tk.Button(self.root, image=self.loadimage)
            btn["border"] = "0"
            btn.place(x=30 * r, y=50)
            self.roulette_list.append(btn)

    def roll_roulette(self):
        # ランダムに1から10の回数でルーレットを回す
        self.steps = random.randint(30, 40)
        self.pos_r = 0
        self.roll_step()  # ステップごとに呼び出す
        

    def roll_step(self):
        if self.steps > 0:
            self.roll()  # 1回のルーレット更新
            self.steps -= 1
            # 100ミリ秒 (1秒) 後に再度この関数を呼び出す
            self.root.after(100, self.roll_step)
        else:
            if self.pos_r == 6:
                print('当たりました')
            else:
                print('ざんねん')


    def roll(self):
        # 現在のボタンの画像を変更する (en2.png)
        original_image = Image.open("en2.png")
        resized_image = original_image.resize((25, 23))
        self.loadimage = ImageTk.PhotoImage(resized_image)
        self.roulette_list[self.pos_r].config(image=self.loadimage)
        self.roulette_list[self.pos_r].image = self.loadimage

        # 次のボタンの画像を変更する (en1.png)
        new_image = Image.open("en1.png")
        resized_new_image = new_image.resize((25, 23))
        self.loadimage2 = ImageTk.PhotoImage(resized_new_image)

        # 次のボタンの画像に更新
        self.pos_r += 1
        if self.pos_r >= 9: 
            self.pos_r = 0

        self.roulette_list[self.pos_r].config(image=self.loadimage2)
        self.roulette_list[self.pos_r].image = self.loadimage2
   

class VMoney:
    def __init__(self, parent) -> None:

        self.root = parent.master
        self.font = parent.font
        self.current_money = 0
        self.p = parent
        self.entry_money()
        self.v_drink = parent.v_drink

    # 入金表示用
    def entry_money(self):

        # 入金合計額
        self.money_lbl = ttk.Label(self.root, text='入れた金額： ' + '0', font=self.font, anchor=tk.W)
        self.money_lbl.place(x= 100, y=100)

        # 入金ボタン
        self.m_100 = tk.Button(self.root, text="Enter 100 Yen", font=self.font, command=self.enter_money_100)
        self.m_100.place(x= 100, y=140)

        self.m_1000 = tk.Button(self.root, text="Enter 1000 Yen", font=self.font, command=self.enter_money_1000)
        self.m_1000.place(x=100, y= 190)

        # 売上ボタン
        self.total_sales = tk.Button(self.root, text="売上", font=self.font, command=self.show_total_sales)
        
        # 売上ラベル
        self.total_sales_label = ttk.Label(self.root, text='売上： ' + '0', font=self.font, anchor=tk.W)
        

    def update_maintenance_menu(self):
        if self.p.maintenance_flag:
            self.total_sales.place(x=100, y= 350)
            self.total_sales_label.place(x= 100, y=400)
        else:
            self.total_sales.place_forget()
            self.total_sales_label.place_forget()


    def show_total_sales(self):
        self.m_money = self.p.m_money 
        print(f'売上合計：{self.m_money.get_total_money()}')
        self.total_sales_label.config(text=str(self.m_money.get_total_money()))

    def enter_money_1000(self):
        self.current_money += 1000
        self.update_enter_money()
    
    def enter_money_100(self):
        self.current_money += 100
        self.update_enter_money()

    def update_enter_money(self):
        # 入れたお金の更新
        m_txt = '入れた金額： ' + str(self.current_money)
        self.money_lbl.config(text=m_txt)

        # ドリンクボタンの更新
        self.v_drink.update(self.current_money)

class VDrink:
    def __init__(self, parent) -> None:
        self.p = parent
        self.root = parent.master
        self.font = parent.font
        self.auto_machine = parent.auto_machine
        self.drink_button_list = []
        self.add_drink_list = []
        self.create_drink()
        self.add_drink()
        self.zaiko = parent.zaiko
        self.update_maintenance_menu()

    # 飲み物ボタンを配置
    def create_drink(self):
        
        x_span = 100
        y_span = 100
        max_flap = 5
        flap = 0
        for name, price in self.auto_machine.drink_list.items():
            lbl = tk.Label(self.root, text=name, font=self.font)
            btn = tk.Button(self.root, text=str(price), font=self.font, command=lambda p=price, n=name: self.purchase(p,n))

            btn['state'] = tk.DISABLED
            lbl.place(x= 300 + x_span, y = y_span)
            btn.place(x= 300 + x_span, y = 50 + y_span)

            self.drink_button_list.append(btn)
            x_span += 100
            flap += 1
            if flap == max_flap:
                y_span += 100
                flap = 0
                x_span = 100

    # 在庫追加ボタン
    def add_drink(self):
        span = 100
        for name, _ in self.auto_machine.drink_list.items():
            btn = tk.Button(self.root, text=str("追加:" + name), font=self.font, command=lambda n=name: self.add_zaiko(n))
            
            btn.place(x= 300 + span, y = 350)
            self.add_drink_list.append(btn)
            span += 200

    def add_zaiko(self, name):
        print(f'在庫追加:{name}')
        self.zaiko.add_product(name)
        # 在庫更新
        self.update_zaiko(name)
    
    # 飲み物更新
    def update(self, val):
        # print(val)
        # お金が充足した場合、ボタンを有効にする
        for btn in self.drink_button_list:
            if btn.cget("text") == '在庫切れ':
                pass
            elif val >= int(btn.cget("text")):
                btn['state'] = tk.NORMAL
            else:
                btn['state'] = tk.DISABLED

    # 商品購入
    def purchase(self, price, name):

        # ルーレット
        self.ru = self.p.ru
        self.ru.roll_roulette()
        # if self.ru.pos_r == 6:
        #     print('当たりました')
        # else:
        #     print('ざんねん')

        # ログ出力
        print(f'購入商品：{name}, 購入金額:{price}')

        # おつりの計算(入金の減算)
        self.v_money = self.p.v_money
        self.v_money.current_money -= price

        # 残金確認
        self.v_money.update_enter_money()
        
        # 売上集計
        self.m_money = self.p.m_money
        self.m_money.cal_total(price)        

        # 在庫減らす
        self.zaiko.decrease_inventory(name)

        # 在庫更新
        self.update_zaiko(name)

    def update_maintenance_menu(self):
        
        if self.p.maintenance_flag:
            self.add_drink()
        else:
            for btn in self.add_drink_list:
                btn.place_forget()

    # 在庫確認
    def update_zaiko(self, name):

        key_list = list(self.auto_machine.drink_list.keys())
        val_list = list(self.auto_machine.drink_list.values())
        for name, price, btn in zip(key_list, val_list, self.drink_button_list):
            if self.zaiko.get_product_size(name) > 0:
                btn['text'] = price
            else:
                btn['text'] = '在庫切れ'
                btn['state'] = tk.DISABLED