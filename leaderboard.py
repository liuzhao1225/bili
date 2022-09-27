import json

GOD_GIFT = '超级战舰'
BOARD_NUM = 5
EUROPE_THREASHOLD = 10
AFRICA_THREASHOLD = 5


class leaderboard:
    def __init__(self):
        self.players = json.load(
            open('data_leaderboard\\players.json', 'r', encoding='utf-8'))
        self.god = json.load(
            open('data_leaderboard\\god.json', 'r', encoding='utf-8'))
        self.show()
    def step(self, data, type):
        if type != 'SEND_GIFT':
            return
        if not data['blind_gift']:
            return

        value = data['combo_total_coin']
        cost = data['total_coin']
        num = data['num']
        uid = str(data['uid'])
        name = data['uname']
        gift = data['giftName']
        print(name + ': ' + gift + 'x' + str(num) + '; ' + str(value) + '/' + str(
            cost))
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
                'num': 0,
                'value': 0,
                'cost': 0,
                'rate': 0
            }
            self.players[name] = d
            self.players[uid] = d

        d['num'] += num
        d['value'] += value/1000
        d['cost'] += cost/1000
        d['rate'] = d['value'] / d['cost']
        json.dump(self.players,
                  open('data_leaderboard\\players.json', 'w', encoding='utf-8'),
                  ensure_ascii=False)
        if gift == GOD_GIFT:
            self.god.append(name)
            json.dump(self.god,
                      open('data_leaderboard\\god.json', 'w', encoding='utf-8'),
                      ensure_ascii=False)
        self.show()

    def god_board(self):
        f = open('data_leaderboard\\god.txt', 'w', encoding='utf-8')
        f.write('封神: ')
        for god in self.god:
            f.write('%s ' % god)
        f.close()

    def show_board(self, filename, players):
        #print(players)
        if filename == 'europe.txt':
            s = '欧洲榜'
        elif filename == 'africa.txt':
            s = '非洲榜'
        else:
            s = '中东榜'
            f = open('data_leaderboard\\' + filename, 'w', encoding='utf-8')
            f.write(s)
            count = 1
            for player in players:
                f.write('\n' + str(count) + '.' + player + ': ' + str(
                    int(self.players[player]['num'])) + '发')
                count += 1
            for i in range(count, BOARD_NUM+1):
                f.write('\n' + str(i) + '.  虚位以待')
            f.close()
            return

        f = open('data_leaderboard\\' + filename, 'w', encoding='utf-8')
        f.write(s)
        count = 1
        for player in players:
            f.write('\n' + str(count) + '.' + player + ': ' + str(
                round(self.players[player]['rate'], 2)))
            count += 1
        for i in range(count, BOARD_NUM+1):
            f.write('\n' + str(i) + '.  虚位以待')
        f.close()

    def europe_board(self):
        d = dict(
            (k, v) for k, v in self.players.items() if
            v['num'] >= EUROPE_THREASHOLD and k != v['uid'])
        players = sorted(d, key=lambda x: (d[x]['rate']), reverse=True)[
                  :BOARD_NUM]
        self.show_board('europe.txt', players)

    def africa_board(self):
        d = dict(
            (k, v) for k, v in self.players.items() if
            v['num'] >= AFRICA_THREASHOLD and k != v['uid'])
        players = sorted(d, key=lambda x: (d[x]['rate']), reverse=False)[
                  :BOARD_NUM]
        self.show_board('africa.txt', players)

    def mideast_board(self):
        d = dict((k, v) for k,v in self.players.items() if k != v['uid'])
        players = sorted(d, key=lambda x: (self.players[x]['num']),
                         reverse=True)[
                  :BOARD_NUM]
        self.show_board('mideast.txt', players)

    def show(self):
        self.europe_board()
        self.africa_board()
        self.mideast_board()
        self.god_board()
