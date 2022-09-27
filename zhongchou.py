import pickle
import json
import threading

lock = threading.Lock()


class zhongchou:
    def __init__(self):
        with open('data_zhongchou\\current.txt', 'r', encoding='utf-8') as f:
            n = f.read()
        self.now = float(n.split(': ')[1].split('/')[0])

    def save(self, data):
        lock.acquire()
        with open('data_zhongchou\\gift_history.json', 'r',
                  encoding='utf-8') as f:
            d = json.load(f)
        with open('data_zhongchou\\gift_history.json', 'w',
                  encoding='utf-8') as f:
            d.append(data)
            json.dump(d, f, ensure_ascii=False)
        lock.release()

    def step(self, data, type):
        if type == 'DANMU_MSG':
            return
        self.now += data['num'] * data['price'] / 1000
        self.save(data)
        print('+' + str(data['num'] * data['price'] / 1000))
        with open('data_zhongchou\\current.txt', 'w', encoding='utf-8') as f:
            f.write('超级游艇: ' + str(round(self.now, 2)) + '/100000000')
