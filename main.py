from bilibili_api.live import LiveDanmaku
from bilibili_api import Verify
from bilibili_api import live
from datetime import datetime
from jielong import jielong
from leaderboard import leaderboard
from zhongchou import zhongchou
from twenty_four import TwentyFour
from dxg_danmu import dxg_danmu
import threading
verify = Verify(sessdata='9a00249e%2C1651844459%2C9fd0a*b1',
                csrf='990d8defd3bf9da98c1bdaf656c69188')
room = LiveDanmaku(room_display_id=23071024, verify=verify)
#room = LiveDanmaku(room_display_id=23108224, verify=verify)

programs = []

@room.on('DANMU_MSG')
async def on_danmu(message):
    # print(message)
    # print()
    data = message['data']
    for p in programs:
        threading.Thread(target=p.step, args=(data, 'DANMU_MSG',)).start()



@room.on('SEND_GIFT')
async def on_gift(gift):
    data = gift['data']['data']
    for p in programs:
        threading.Thread(target=p.step, args=(data, 'SEND_GIFT',)).start()


if __name__ == '__main__':
    programs.append(jielong())
    programs.append(leaderboard())
    programs.append(zhongchou())
    programs.append(TwentyFour())
    programs.append(dxg_danmu())
    while True:
        try:
            room.connect()
        except:
            pass
