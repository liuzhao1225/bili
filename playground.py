import time
from test1 import test1
from test2 import test2
import threading
class play():
    def __init__(self):
        pass

    def recieve_message(self, msg):
        print(msg)
        print()

    def recieve_gift(self, gift):
        print(gift)
        print()

    async def f1(self):
        print('f1')
        time.sleep(5)

    async def f2(self):
        print('f2')
        time.sleep(5)

if __name__ == '__main__':
    programs = []
    programs.append(test1())
    programs.append(test2())
    count = 0
    for p in programs:
        threading.Thread(target=p.step, args=(count,)).start()
        count += 1
