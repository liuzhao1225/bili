import random
from datetime import datetime
import time
from pypinyin import lazy_pinyin as pinyin
from pypinyin import load_phrases_dict
import string
from jielong_level import lv
import pickle
import json
import requests
import threading
CD = 20

load_phrases_dict({'下自成蹊':[['xià'], ['zì'], ['chéng'], ['xī']]})
load_phrases_dict({'长相厮守':[['cháng'], ['xiàng'], ['sī'], ['shǒu']]})
class jielong:
    def __init__(self):
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.guessed = set()
        self.word = '游戏开始'
        self.py = pinyin(self.word)
        self.lock = threading.Lock()
        self.run = False
        self.players = json.load(
            open('data_jielong\\players.json', 'r', encoding='utf-8'))
        self.words = pickle.load(open('data_jielong\\word.pkl', 'rb'))
        self.punctuation = string.punctuation + '！@#￥%……&*（）《》？：“{}【】；’，。、-=——+、|·~'
        try:
            self.wsyw = pickle.load(open('data_jielong\\wsyw.pkl', 'rb'))
        except:
            self.wsyw = []
        self.same = ['冠上加冠',
                     '以夷伐夷',
                     '地丑力敌',
                     '日慎一日',
                     '见所未见',
                     '头痛治头',
                     '相门有相',
                     '适逢其时',
                     '轮扁斫轮',
                     '床上安床',
                     '豆萁燃豆',
                     '金吾不禁',
                     '床上叠床',
                     '束手无术',
                     '闻所不闻',
                     '猿啼鹤怨',
                     '足痛治足',
                     '极深研幾',
                     '以铢程镒',
                     '箕裘相继',
                     '计穷虑极',
                     '积劳成疾',
                     '惟所欲为',
                     '行险徼幸',
                     '头上著头',
                     '欺人自欺',
                     '以辞害意',
                     '钟鸣鼎重',
                     '以词害意',
                     '新益求新',
                     '精益求精',
                     '剪恶除奸',
                     '唯所欲为',
                     '猿惊鹤怨',
                     '神乎其神',
                     '枝外生枝',
                     '返辔收帆',
                     '一定不易',
                     '木公金母',
                     '负固不服',
                     '断长补短',
                     '烟云过眼',
                     '行崄侥幸',
                     '欲取姑予',
                     '头痛灸头',
                     '以防万一',
                     '吁咈都俞',
                     '天外有天',
                     '见所不见',
                     '矫尾厉角',
                     '盗亦有道',
                     '举不胜举',
                     '是非得失',
                     '大吹大打',
                     '人无完人',
                     '一脚不移',
                     '为所欲为',
                     '头上着头',
                     '将门有将',
                     '失时落势',
                     '一劳久逸',
                     '脚痛医脚',
                     '一字不易',
                     '朝奏暮召',
                     '忍无可忍',
                     '断长续短',
                     '奉扬仁风',
                     '离题万里',
                     '以夷攻夷',
                     '床上迭床',
                     '福倚祸伏',
                     '积谷防饥',
                     '一成不易',
                     '映雪囊萤',
                     '数不胜数',
                     '以疑决疑',
                     '花信年华',
                     '感人肺肝',
                     '以夷制夷',
                     '年复一年',
                     '屋下架屋',
                     '以铢称镒',
                     '话中有话',
                     '美益求美',
                     '防不胜防',
                     '屋下盖屋',
                     '话里有话',
                     '难乎其难',
                     '极深研几',
                     '讹以滋讹',
                     '防不及防',
                     '畏头畏尾',
                     '仁者见仁',
                     '猿悲鹤怨',
                     '筋疲力尽',
                     '适当其时',
                     '狐埋狐搰',
                     '不无小补',
                     '百战百败',
                     '国将不国',
                     '依心像意',
                     '孤鸾寡鹄',
                     '节中长节',
                     '计穷力极',
                     '一心一意',
                     '一览无遗',
                     '痛定思痛',
                     '十目所视',
                     '日复一日',
                     '以夷治夷',
                     '遭家不造',
                     '智者见智',
                     '屋下作屋',
                     '头痛医头',
                     '脚痛灸脚',
                     '跻峰造极',
                     '粒米狼戾',
                     '孤鸿寡鹄',
                     '易于拾遗',
                     '日甚一日',
                     '一谦四益',
                     '讹以传讹',
                     '床下安床',
                     '竭诚尽节',
                     '旧瓶新酒',
                     '损之又损',
                     '玄之又玄',
                     '畏首畏尾',
                     '贼喊捉贼',
                     '己溺己饥',
                     '以肉去蚁',
                     '衣锦褧衣',
                     '床上施床',
                     '瘠人肥己',
                     '适俗随时',
                     '移情遣意',
                     '积忧成疾',
                     '一身两役',
                     '相门出相',
                     '一定不移',
                     '师心自是',
                     '刑期无刑',
                     '微乎其微',
                     '一劳永逸',
                     '綦溪利跂',
                     '以骨去蚁',
                     '失张冒势',
                     '梦中说梦',
                     '亲上做亲',
                     '事无常师',
                     '计穷智极',
                     '实事求是',
                     '闻所未闻',
                     '头上安头',
                     '朝奏夕召',
                     '时不可失',
                     '仁者能仁',
                     '鸮啼鬼啸',
                     '俯首就缚',
                     '言笑晏晏',
                     '眉下添眉',
                     '知足知止',
                     '亲上成亲']
        self.final = '为所欲为'
        with open('data_jielong\\结束词.txt', 'r', encoding='utf-8') as f:
            self.final = f.read().strip()
        print(self.final)
        self.notification_cd = time.time()
        self.show_wsyw()
        #self.update_final()

    def show_wsyw(self):
        s = ' '
        for name in self.wsyw:
            s += name + ' '
        with open('data_jielong\\wsyw.txt', 'w') as f:
            f.write(s)
        with open('data_jielong\\wsyw.pkl', 'wb') as f:
            pickle.dump(self.wsyw, f)

    def send(self, msg):
        url = 'https://api.live.bilibili.com/msg/send'
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
        cookies = {
            "cookie": "_uuid=6B3ECB7C-DD4B-21AF-65A5-4BB506A6E0F002371infoc; CURRENT_FNVAL=80; blackside_state=1; LIVE_BUVID=AUTO1816026325402278; rpdid=|(uk||llukRR0J'uY|Jkmkm|Y; buivd_fp=2EE2E491-9C29-4FF7-AEBE-3A02DB9F6E90143109infoc; buvid3=DDFF53DC-6076-44DA-911A-9EFB245CEE06184979infoc; SESSDATA=e37bcd64%2C1636259297%2Ce7d09%2A51; bili_jct=990d8defd3bf9da98c1bdaf656c69188; DedeUserID=1263732318; DedeUserID__ckMd5=0e1ee809adf64347; sid=kbq9q1qw; buvid_fp=DDFF53DC-6076-44DA-911A-9EFB245CEE06184979infoc; buvid_fp_plain=DDFF53DC-6076-44DA-911A-9EFB245CEE06184979infoc; CURRENT_QUALITY=64; fingerprint=fbc86531c9f2fa70fba4e5f991630885; fingerprint3=a0bf239e49f8d88bb28304a13fa8a82a; fingerprint_s=409f77c6ff87242003fe83f7d4436751; bp_t_offset_1263732318=535843998211146584; bp_video_offset_1263732318=537701472785913975; _dfcaptcha=5eac464687b0a90a6d49b301474fe248; PVID=6; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1622325347,1622396422,1622482945,1624200138; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1624200138",
        }
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
            print("msg failed")

    def start(self):
        self.check_new_date()
        self.run = True
        self.word = random.sample(self.words, k=1)[0]
        self.py = pinyin(self.word)
        self.guessed = set()
        self.send('开始查询受教育程度!')
        self.send('新成语：' + self.word)
        with open('data_jielong\\今日.txt', 'w', encoding='utf-8') as f:
            f.write('当前成语：'+self.word +'\n接龙结束词：' + self.final)
        print(self.final)

    def step(self, data, type):
        if type != 'DANMU_MSG':
            return
        data = data['info']
        text = data[1].strip()
        uid = str(data[2][0])
        name = data[2][1]
        medal = True if data[3] and data[3][3] == 23071024 else False
        if '查询' in text[:2]:
            self.chaxun(text, uid, name)
            return

        if '成语接龙' in text:
            if self.run:
                self.notify()
            else:
                self.start()
            return

        if not self.run:
            return

        word = text.translate(str.maketrans('', '', self.punctuation))
        if len(word) != 4:
            return
        self.lock.acquire()
        if pinyin(word)[0] == self.py[-1]:
            if word == self.final:
                self.end_game(text, word, uid, name, medal)
                print(name + ' 终结比赛')
                return
            if word in self.guessed:
                self.lock.release()
                self.replicate(text)
                return
            if word in self.words:
                self.correct(text, word, uid, name, medal)
                return
            self.lock.release()
            self.not_word(text)
            return
        self.lock.release()
        self.notify()

    def replicate(self, text):
        self.send('「' + text + '」说过啦！')

    def not_word(self, text):
        self.send('「' + text + '」不是成语')

    def notify(self):
        if time.time() - self.notification_cd < CD:
            return
        self.send('当前成语：' + self.word)
        self.notification_cd = time.time()

    def correct(self, text, word, uid, name, medal):
        if not medal:
            keys = [name, uid]
            for k in keys:
                if k in self.players.keys() and self.players[k]['等级'] > 3:
                    self.lock.release()
                    self.send('请佩戴「朝聞道」勋章进行小学以上学习')
                    return
        self.notification_cd = time.time()
        self.update(uid, name, '接龙')
        self.guessed.add(word)
        self.py = pinyin(word)
        self.word = text
        self.lock.release()
        self.send('恭喜「' + name + '」答对啦！')
        self.send('新成语：' + text)
        with open('data_jielong\\今日.txt', 'w', encoding='utf-8') as f:
            f.write('当前成语：'+self.word +'\n接龙结束词：' + self.final)

    def update(self, uid, name, type):
        if uid in self.players.keys():
            self.players[name] = self.players[uid]
            d = self.players[uid]
            d['昵称'] = name
        elif name in self.players.keys():
            self.players[uid] = self.players[name]
            d = self.players[uid]
            d['uid'] = uid
        else:
            d = {
                'uid': uid,
                '昵称': name,
                '等级': 0,
                '接龙': 0,
                '终结': 0,
                '接龙经验': 0,
                '终结经验': 0,
                '升级需求': '接龙经验',
                '升级经验': 1
            }
            self.players[name] = d
            self.players[uid] = d

        d['接龙'] += 1
        d['接龙经验'] += 1
        if type == '终结':
            d['终结'] += 1
            d['终结经验'] += 1
        self.levelup(uid)
        json.dump(self.players,
                  open('data_jielong\\players.json', 'w', encoding='utf-8'),
                  ensure_ascii=False)

    def check_new_date(self):
        new = datetime.today().strftime('%Y-%m-%d')
        if new != self.date:
            self.date = new
            self.update_final()

    def update_final(self):
        self.final = random.choice(self.same)
        self.wsyw = []
        print('新词：' + self.final)
        with open('data_jielong\\结束词.txt', 'w', encoding='utf-8') as f:
            f.write(self.final)
        with open('data_jielong\\今日.txt', 'w', encoding='utf-8') as f:
            f.write('输入成语接龙开始游戏')
        self.show_wsyw()

    def levelup(self, uid):
        user = self.players[uid]
        userid = user['昵称']
        print(userid + '(' + str(user[user['升级需求']]) + '/' + str(
            user['升级经验']) + ')')
        if uid == "1263732318":
            return
        if user[user['升级需求']] >= user['升级经验']:
            level = user['等级']
            finished = lv[level][0]
            to_study = lv[level + 1][0]

            level_ = level + 1
            user['等级'] = level_
            user['升级需求'] = lv[level_][1]
            user['升级经验'] = lv[level_][2]
            user['接龙经验'] = 0
            user['终结经验'] = 0
            if level < 25:
                self.send(
                    '恭喜「' + userid + '」完成' + finished + '!')
                self.send('开始' + to_study + '学习！')
            elif level < 31:
                self.send('恭喜「' + userid + '」升职，成为' + to_study + '！')
            else:
                self.send(userid + '，' + to_study + '！')

            print(userid + ' level up!')

    def chaxun(self, text, name, uid):
        if text != '查询':
            name = text.split('查询')[1].strip()
            if name == '打卡' or name == '签到':
                return
            user = self.players.get(name)
        else:
            user = self.players.get(uid)
            if not user:
                user = self.players.get(name)
        if user:
            xueli = lv[user['等级']][0]
            jielong = user['接龙']
            zhongjie = user['终结']
            first_half = user['昵称'] + '：'
            second_half = xueli + ' (' + str(user[user['升级需求']]) + '/' + str(
                user['升级经验']) + ')'
            if len(first_half) + len(second_half) > 20:
                self.send(first_half)
                self.send(second_half)
            else:
                self.send(first_half + second_half)
            self.send('完成' + str(jielong) + '次接龙，终结' + str(zhongjie) + '次游戏')
        else:
            self.send(name + '：尚未完成胎教')

    def end_game(self, text, word, uid, name, medal):
        if not medal:
            keys = [name, uid]
            for k in keys:
                if k in self.players.keys() and self.players[k]['等级'] > 3:
                    self.lock.release()
                    self.send('请佩戴「朝聞道」勋章进行小学以上学习')
                    return
        self.run = False
        self.wsyw.append(name)
        print(name + ' 终结')
        self.update(uid, name, '终结')
        self.show_wsyw()
        self.lock.release()
        self.send(self.final + '！游戏结束！')
        self.send('恭喜「' + name + '」终结比赛！')
