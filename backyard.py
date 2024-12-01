import tkinter as tk


class Backyard:
    def __init__(self, root) -> None:
        self.root = root
        

    def open_sub_window(self):
        sub_win = tk.Toplevel(self.root)
        sub_win.title('メンテナンス')
        sub_win.geometry('300x200')

        # ラベルの追加
        label = tk.Label(sub_win, text="これはToplevelウィンドウです")
        label.pack(pady=20)

        # 閉じるボタンの追加
        close_button = tk.Button(sub_win, text="閉じる", command=sub_win.destroy)
        close_button.pack(pady=10)

