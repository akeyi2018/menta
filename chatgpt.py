import tkinter as tk

class DrinkMachineApp:
    def __init__(self, root, auto_machine):
        self.root = root
        self.auto_machine = auto_machine
        self.font = ('Arial', 12)
        self.drink_button_list = []
        self.create_drink()

    def purchase(self, price, name):
        print(f"Purchased {name} for {price} yen")

    def create_drink(self):
        # フレーム
        self.label_frame = tk.LabelFrame(self.root, text='Drinks', bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.label_frame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")

        max_flap = 5
        flap = 0
        row = 0
        col = 0

        for name, price in self.auto_machine.drink_list.items():
            lbl = tk.Label(self.label_frame, text=name, font=self.font)
            btn = tk.Button(self.label_frame, text=str(price), font=self.font, 
                            command=lambda p=price, n=name: self.purchase(p, n))
            btn['state'] = tk.NORMAL  # ボタンの状態

            # グリッド配置
            lbl.grid(row=row, column=col * 2, padx=5, pady=5)
            btn.grid(row=row, column=col * 2 + 1, padx=5, pady=5)

            self.drink_button_list.append(btn)
            flap += 1
            col += 1

            if flap == max_flap:
                row += 1
                flap = 0
                col = 0
