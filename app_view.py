import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import random
import qrcode

class Roulette:
    def __init__(self, parent) -> None:
        self.root = parent.master
        self.roulette_list = []
        self.add_roulette_ui()
        self.pos_r = 0

    def add_roulette_ui(self):

        # フレーム
        self.label_frame = tk.LabelFrame(self.root, text='ルーレット', bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.label_frame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

        # "回す"ボタン
        # self.mv = tk.Button(self.root, text="回す", command=self.roll_roulette)
        # self.mv.place(x=100, y=10)
        self.lbl = tk.Label(self.label_frame, text='当たり')
        # self.lbl.place(x=175, y=30)
        self.lbl.grid(column=6,row=0,padx=5, pady=5)

        # 初期のイメージ設定
        original_image = Image.open("en2.png")
        resized_image = original_image.resize((25, 23))
        self.loadimage = ImageTk.PhotoImage(resized_image)

        # ボタンを10個生成してリストに追加
        for r in range(9):
            btn = tk.Button(self.label_frame, image=self.loadimage if self.loadimage else None)
            btn["border"] = "0"
            btn.grid(column=r, row=1, padx=5, pady=5)  # ボタンを1行目に配置
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

        # フレーム
        self.label_frame = tk.LabelFrame(self.root, text='決済', bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.label_frame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

        # 現金
        self.label_frame_real_money = tk.LabelFrame(self.label_frame, text='現金', bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.label_frame_real_money.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        # 入金合計額
        self.money_lbl = ttk.Label(self.label_frame_real_money, text='入れた金額： ' + '0', font=self.font, anchor=tk.W)
        self.money_lbl.grid(row=0,column=0,padx=10,pady=10)

        # 入金ボタン
        self.m_100 = tk.Button(self.label_frame_real_money, text="Enter 100 Yen", font=self.font, command=self.enter_money_100)
        self.m_100.grid(row=1,column=0,padx=10,pady=10)

        self.m_1000 = tk.Button(self.label_frame_real_money, text="Enter 1000 Yen", font=self.font, command=self.enter_money_1000)
        self.m_1000.grid(row=2,column=0,padx=10,pady=10)

        # QR Code
        self.label_frame_digital_money = tk.LabelFrame(self.label_frame, text='電子マネー', bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.label_frame_digital_money.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

        self.imgtk = ImageTk.PhotoImage(self.makeQR('____'))
        self.qr_lbl = ttk.Label(self.label_frame_digital_money,text='',image=self.imgtk)
        # self.qr_lbl = ttk.Label(self.label_frame_digital_money,text='電子決済')
        self.qr_lbl.grid(row=0,column=0,padx=10,pady=10)

    def makeQR(self, text):
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(text)
        qr.make(fit=True)
        if text == '____':
            img = qr.make_image(fill_color="white", back_color="white")
        else:
            img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((100,100))
        return img

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
        # self.v_drink.update(self.current_money)

class VDrink:
    def __init__(self, parent) -> None:
        self.p = parent
        self.root = parent.master
        self.font = parent.font
        self.auto_machine = parent.auto_machine
        self.drink_button_list = []
        self.add_drink_list = []
        self.create_drink()
        self.update()
        self.zaiko = parent.zaiko

    # 飲み物ボタンを配置
    def create_drink(self):
        
        # フレーム
        self.label_frame = tk.LabelFrame(self.root, text='Drinks', bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.label_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        max_flap = 5
        flap = 0
        row = 0
        col = 0
        for name, price in self.auto_machine.drink_list.items():
            lbl = tk.Label(self.label_frame, text=name, font=self.font)
            btn = tk.Button(self.label_frame, text=str(price), font=self.font, bg='white',
                            command=lambda p=price, n=name: self.purchase(p,n))

            btn['state'] = tk.DISABLED

            # グリッド配置
            lbl.grid(row=row, column=col * 2, padx=5, pady=5)
            btn.grid(row=row+1, column=col * 2, padx=5, pady=5)

            self.drink_button_list.append(btn)
            flap += 1
            col += 1

            if flap == max_flap:
                row += 2
                flap = 0
                col = 0


    def add_zaiko(self, name):
        print(f'在庫追加:{name}')
        self.zaiko.add_product(name)
        # 在庫更新
        self.update_zaiko(name)
    
    # 飲み物更新
    def update(self):
        # お金が充足した場合、ボタンを有効にする
        for btn in self.drink_button_list:
            if btn.cget("text") == '在庫切れ':
                pass
            # elif val >= int(btn.cget("text")):
                # btn['state'] = tk.NORMAL
            else:
                btn['state'] = tk.NORMAL

    def pay_cash(self, name, price):
        # ルーレット
        self.ru = self.p.ru
        self.ru.roll_roulette()

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


    # 商品購入
    def purchase(self, price, name):
        
        # 現金を入れているかを判断
        self.v_money = self.p.v_money
        # print(int(self.v_money))
        if self.v_money.current_money >= price:
            self.pay_cash(name, price)

        # 電子決済
        else:
            # 選択したボタンの色の変更
            self.update_btn(name)
            
            # QR code更新
            self.img = ImageTk.PhotoImage(self.v_money.makeQR(name))
            self.v_money.qr_lbl.config(image=self.img)
            self.v_money.qr_lbl.update()

      

    def update_btn(self, t_name):
        key_list = list(self.auto_machine.drink_list.keys())
        for name, btn in zip(key_list, self.drink_button_list):
            if name == t_name:
                btn['bg'] = 'blue'
            else:
                btn['bg'] = 'white'

    # 在庫更新
    def update_zaiko(self, name):

        key_list = list(self.auto_machine.drink_list.keys())
        val_list = list(self.auto_machine.drink_list.values())
        for name, price, btn in zip(key_list, val_list, self.drink_button_list):
            if self.zaiko.check_product(name) > 0:
                btn['text'] = price
            else:
                btn['text'] = '在庫切れ'
                btn['state'] = tk.DISABLED