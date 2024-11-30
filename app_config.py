import os,json

class DrinkConfig():
    
    def __init__(self, info) -> None:
        # 情報を管理するJson
        self.info = info
        self.category_info = os.path.join(os.getcwd(), self.info)

    def get_json_info(self):
        with open(self.category_info, mode='r', encoding='utf-8') as json_file:
            return json.load(json_file)
    
    def set_json_info(self, category_key, category_value):
        try:
            # jsonファイルの読み込み
            with open(self.category_info,'r', encoding='cp932') as json_file:
                json_data = json.load(json_file)
                json_data[category_key] = category_value
            # jsonファイルの更新
            with open(self.category_info, 'w', encoding='cp932') as json_file:
                json.dump(json_data, json_file, indent=4)
        except:
            print('jsonファイル更新失敗しました。')

    def del_json_info(self, category_value):
        try:
            # jsonファイルの読み込み
            with open(self.category_info,'r', encoding='cp932') as json_file:
                json_data = json.load(json_file)
                keys = [k for k, v in json_data.items() if v== category_value]
                if not keys is None:
                    for k in keys:
                        del(json_data[k])
                        
            # jsonファイルの更新
            with open(self.category_info, 'w', encoding='cp932') as json_file:
                json.dump(json_data, json_file, indent=4)
        except:
            print('jsonファイル更新失敗しました。')

    def initial_json(self):
        json_data = {
            "TEA": 100
        }
        with open(self.category_info, 'w', encoding='cp932') as json_file:
                json.dump(json_data, json_file, indent=4)

def regsite_drink():
    # ドリンク情報の登録
    ins = DrinkConfig('drink_info.json')
    # ins.initial_json()
    # print(ins.get_json_info())
    ins.set_json_info('BEER',300)
    ins.set_json_info('COFFEE', 150)
    ins.set_json_info('JUICE_01', 130)
    ins.set_json_info('JUICE_02', 130)
    ins.set_json_info('JUICE_03', 130)
    ins.set_json_info('JUICE_04', 130)
    ins.set_json_info('JUICE_05', 130)

def regsite_zaiko():
    # ドリンク情報の登録
    ins = DrinkConfig('inventory_info.json')
    ins.initial_json()
    # print(ins.get_json_info())
    ins.set_json_info('BEER',50)
    ins.set_json_info('COFFEE', 100)
    ins.set_json_info('JUICE_01', 100)
    ins.set_json_info('JUICE_02', 100)
    ins.set_json_info('JUICE_03', 100)
    ins.set_json_info('JUICE_04', 100)
    ins.set_json_info('JUICE_05', 100)


if __name__ == '__main__':
    # 単体テスト
    regsite_drink()
    regsite_zaiko()