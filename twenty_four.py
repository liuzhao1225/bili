from random import randint
import requests
import threading
import re
from itertools import permutations
import operator
import os
import time
lock = threading.Lock()
NOTIFICATION_CD = 10


class TwentyFour():
    def __init__(self):
        self.num = [0, 0, 0, 0]
        self.generate_game()
        self.last_notification = time.time()

    def generate_game(self):
        has_solution = False
        lock.acquire()
        while not has_solution:
            self.num = [randint(1, 10), randint(1, 10), randint(1, 10),
                        randint(1, 10)]
            self.num.sort()
            has_solution = self.find_solution()
        lock.release()

        with open(os.path.join('data_24', 'timu.txt'), 'w',
                  encoding='utf-8') as f:
            f.write('24点:')
            for i in self.num:
                f.write(' ' + str(i))

    def find_solution(self):
        perms = permutations(self.num)
        for perm in perms:
            if self.find_solution_helper(perm[0], perm[1:]):
                return True
        return False

    def find_solution_helper(self, curr, nums):
        if len(nums) == 0:
            return curr == 24
        next = nums[0]
        nums = nums[1:]
        if self.find_solution_helper(curr + next, nums):
            return True
        if self.find_solution_helper(curr - next, nums):
            return True
        if self.find_solution_helper(next - curr, nums):
            return True
        if self.find_solution_helper(curr * next, nums):
            return True
        if next != 0 and self.find_solution_helper(curr / next, nums):
            return True
        if curr != 0 and self.find_solution_helper(next / curr, nums):
            return True
        return False

    def strQ2B(self, ustring):
        """全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (
                    inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248

            rstring += chr(inside_code)
        return rstring

    def send(self, msg):
        url = 'https://api.live.bilibili.com/msg/send'
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
        cookies = {
            "cookie": "_uuid=6B3ECB7C-DD4B-21AF-65A5-4BB506A6E0F002371infoc; CURRENT_FNVAL=80; blackside_state=1; LIVE_BUVID=AUTO1816026325402278; rpdid=|(uk||llukRR0J'uY|Jkmkm|Y; buivd_fp=2EE2E491-9C29-4FF7-AEBE-3A02DB9F6E90143109infoc; buvid3=DDFF53DC-6076-44DA-911A-9EFB245CEE06184979infoc; CURRENT_QUALITY=80; bp_t_offset_7361074=522629698098735394; bp_video_offset_7361074=523077049004079217; SESSDATA=e37bcd64%2C1636259297%2Ce7d09%2A51; bili_jct=990d8defd3bf9da98c1bdaf656c69188; DedeUserID=1263732318; DedeUserID__ckMd5=0e1ee809adf64347; sid=kbq9q1qw; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1619799420,1619838650,1620448107,1620824168; fingerprint3=a0bf239e49f8d88bb28304a13fa8a82a; fingerprint=04c60af673a4da94223bbced27d527b4; fingerprint_s=51d289f2f4e248ae198dbdc38311fd40; buvid_fp=DDFF53DC-6076-44DA-911A-9EFB245CEE06184979infoc; buvid_fp_plain=DDFF53DC-6076-44DA-911A-9EFB245CEE06184979infoc; bp_video_offset_1263732318=523946354684448548; bp_t_offset_1263732318=523986147560849667; _dfcaptcha=5d369f0fca77f205ab5bb646fdb52a53; PVID=2"}
        data = {
            'bubble': 0,
            'msg': msg,
            'color': 16777215,
            'mode': 1,
            'fontsize': 25,
            'rnd': 1619860406,
            'roomid': 23071024,
            'csrf': '990d8defd3bf9da98c1bdaf656c69188',
            'csrf_token': '990d8defd3bf9da98c1bdaf656c69188'
        }
        try:
            requests.post(url, data=data, cookies=cookies, headers=header)
        except:
            print('message failed')

    def calculate(self, msg):
        try:
            if round(eval(msg), 5) == 24:
                return 'Correct'
            return 'Wrong'
        except:
            return False

    def step(self, data, type):
        if type != 'DANMU_MSG':
            return
        data = data['info']
        text = self.strQ2B(data[1].strip()).replace(' ', '')
        if text == '加一块' or text == '全加':
            text = '+'.join([str(n) for n in self.num])
        elif text == '乘一块' or text == '全乘':
            text = '*'.join([str(n) for n in self.num])
        else:
            text = text.replace('加',
                                                                         '+').replace(
                '减', '-').replace('乘以', '*').replace('乘', '*').replace('除以','/').replace('除', '/').replace('^',
                                                                      '**').replace('幂', '**').replace(
                '左括号', '(').replace('右括号', ')').replace('左', '(').replace('右', ')').replace('一', '1').replace('二', '2').replace('三', '3').replace('四', '4').replace('五', '5').replace('六', '6').replace('七', '7').replace('八', '8').replace('九', '9').replace('十', '10')
        res = self.calculate(text)
        if not res:
            return
        res_nums = [int(i) for i in re.findall(r'\d+', text)]
        res_nums.sort()
        if len(res_nums) != 4:
            return
        if res_nums != self.num:
            if time.time() - self.last_notification > NOTIFICATION_CD:
                self.send('请使用题目提供的数进行计算')
                self.last_notification = time.time()
            return
        if res == 'Wrong':
            self.send('“' + text + '”结果不为24哦')
            return

        uid = str(data[2][0])
        name = data[2][1]

        self.send(text + '=24')
        self.send('恭喜「' + name + '」算对啦！')
        self.last_notification = time.time()
        self.generate_game()


if __name__ == '__main__':
    game = TwentyFour()
