import json
import os
import threading
from filelock import FileLock
lock = threading.Lock()
PATH = 'C:\\Users\\ZhaoLiu\\Desktop\\bilibili\\dxg'


class dxg_danmu():
    def __init__(self):
        self.gift_path = os.path.join(PATH, 'gift.json')
        self.danmu_path = os.path.join(PATH, 'danmu.json')

    def write_json(self, new_data, path):
        with FileLock(path+'.lock'):
            with open(path, 'r+', encoding='utf-8') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                # Join new_dat3a with file_data
                file_data.append(new_data)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, ensure_ascii=False)
        """lock.acquire()
        with open(path, 'r+', encoding='utf-8') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_dat3a with file_data
            file_data.append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, ensure_ascii=False)
        lock.release()"""
    def step(self, data, msg_type):
        if msg_type == 'SEND_GIFT':
            d = {}
            d['uid'] = str(data['uid'])
            d['name'] = data['uname']
            d['coin'] = data['num'] * data['price']
            d['gold'] = True if data['coin_type'] == 'gold' else False
            d['guard'] = data['guard_level']
            d['gift_name'] = data['giftName']
            # d['medal'] = True if data['medal_info'] and data['medal_info']['target_id'] == 1263732318 else False
            print(d)
            try:
                self.write_json(d, self.gift_path)
            except:
                print('gift save failed')
        elif msg_type == 'DANMU_MSG':
            data = data['info']
            d = {}
            d['uid'] = str(data[2][0])
            d['name'] = data[2][1]
            d['text'] = data[1].strip()
            print(d)
            try:
                self.write_json(d, self.danmu_path)
            except:
                print('danmu save failed')
