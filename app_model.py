import queue
from app_config import DrinkConfig

# 自動販売機クラス
class Auto_machine:

    def __init__(self):
        drink_info = 'drink_info.json'
        
        ins = DrinkConfig(drink_info)
        self.drink_list = ins.get_json_info()

class Money:

    def __init__(self) -> None:
        self.total_money = 0

    def cal_total(self, val):
        self.total_money += val

    def get_total_money(self):
        return self.total_money

class Zaiko:

    def __init__(self) -> None:
        inventory_info ='inventory_info.json'
        self.ins = DrinkConfig(inventory_info)
        self.product_list = self.ins.get_json_info()

    # 
    def decrease_inventory(self, name):
        if self.product_list[name] > 0:
            new_size = self.product_list[name] - 1
            self.ins.set_json_info(name, new_size)

    # 在庫数取得
    def get_product_size(self, name):
        if self.product_list[name] > 0:
            return True
        else:
            return False
    # 在庫追加
    def add_product(self, name):
        self.li[name].put(name)

class Zaiko_old:

    def __init__(self) -> None:
        self.tea = queue.Queue()
        self.juice = queue.Queue()
        self.beer = queue.Queue()
        self.li = {'TEA': self.tea, 'JUICE': self.juice, 'BEER': self.beer}

        # 初期在庫
        self.zaiko_num = 5
        for _ in range(self.zaiko_num):
            self.tea.put('TEA')

        for _ in range(self.zaiko_num):
            self.juice.put('JUICE')

        for _ in range(self.zaiko_num):
            self.beer.put('BEER')

    def get_product(self, name):
        if self.li[name].qsize() > 0:
            self.li[name].get()

    def get_product_size(self, name):
        if self.li[name].qsize() > 0:
            return True
        else:
            return False
    # 在庫追加
    def add_product(self, name):
        self.li[name].put(name)
        

if __name__ == '__main__':

    q = Zaiko()

    for i in range(5):
        q.get_product('TEA')

    for i in range(5):
        q.get_product('BEER')

    if q.get_product_size('TEA'):
        print(f'お茶の在庫あり')
    else:
        print(f'お茶売り切れ')

    if q.get_product_size('BEER'):
        print(f'ビールの在庫あり')
    else:
        print(f'ビール売り切れ')
    