# -*- coding: UTF8 -*-

class MatchOdds:
    def __init__(self):
        # 主队
        self.home = ''
        # 客队
        self.away = ''
        # 各大公司赔率列表
        self.odds = []

class Odds:
    def __init__(self):
        # 公司名
        self.company = ''
        # 亚盘水位
        self.asian = []
        # 大小水位
        self.over = []
        # 欧赔水位
        self.euro = []
