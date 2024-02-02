import json
import time
import os

from typing import List, Dict

plugin_dir:str = os.path.dirname(__file__)

class ChartFilter:
    def __init__(self, data, musicdata):
        self.musicdata:List[Dict] = musicdata
        self.data:Dict = self._chartfilter(data)

    def _computeRa(self, ds: float, achievement: float) -> int:
        baseRa = 22.4 
        if achievement < 50:
            baseRa = 7.0
        elif achievement < 60:
            baseRa = 8.0 
        elif achievement < 70:
            baseRa = 9.6 
        elif achievement < 75:
            baseRa = 11.2 
        elif achievement < 80:
            baseRa = 12.0 
        elif achievement < 90:
            baseRa = 13.6 
        elif achievement < 94:
            baseRa = 15.2 
        elif achievement < 97:
            baseRa = 16.8 
        elif achievement < 98:
            baseRa = 20.0 
        elif achievement < 99:
            baseRa = 20.3
        elif achievement < 99.5:
            baseRa = 20.8 
        elif achievement < 100:
            baseRa = 21.1 
        elif achievement < 100.5:
            baseRa = 21.6 

        return int(ds * (min(100.5, achievement) / 100) * baseRa)

    def _computeRate(self, achievement: float) -> str:
        rate = ['d', 'c', 'b', 'bb', 'bbb', 'a', 'aa', 'aaa', 's', 'sp', 'ss', 'ssp', 'sss', 'sssp']
        index = 13
        if achievement < 50:
            index = 0
        elif achievement < 60:
            index = 1
        elif achievement < 70:
            index = 2
        elif achievement < 75:
            index = 3
        elif achievement < 80:
            index = 4
        elif achievement < 90:
            index = 5
        elif achievement < 94:
            index = 6
        elif achievement < 97:
            index = 7
        elif achievement < 98:
            index = 8
        elif achievement < 99:
            index = 9
        elif achievement < 99.5:
            index = 10
        elif achievement < 100:
            index = 11
        elif achievement < 100.5:
            index = 12

        return rate[index]
    
    def _chartfilter(self, data:Dict) -> Dict:
        song_id = data["id"]
        level_index = data["level_index"]
        # song_id,ds,ra,rate
        data["song_id"] = str(song_id)
        for music in self.musicdata:
            if music["id"] == str(song_id):
                data["ds"] = music["ds"][level_index]
                break
        data["ra"] = self._computeRa(data["ds"],data["achievements"])
        data["rate"] = self._computeRate(data["achievements"]) 
        return data
    

class ChartFilter_b40:
    def __init__(self, data):
        self.data:Dict = self._chartfilter(data)

    def _computeRa(self, ds: float, achievement:float) -> int:
        baseRa = 14.0
        if achievement >= 50 and achievement < 60:
            baseRa = 5.0
        elif achievement < 70:
            baseRa = 6.0
        elif achievement < 75:
            baseRa = 7.0
        elif achievement < 80:
            baseRa = 7.5
        elif achievement < 90:
            baseRa = 8.0
        elif achievement < 94:
            baseRa = 9.0
        elif achievement < 97:
            baseRa = 10.5
        elif achievement < 98:
            baseRa = 12.5
        elif achievement < 99:
            baseRa = 12.7
        elif achievement < 99.5:
            baseRa = 13.0
        elif achievement < 100:
            baseRa = 13.2
        elif achievement < 100.5:
            baseRa = 13.5

        return int(ds * (min(100.5, achievement) / 100) * baseRa)

        rate = ['d', 'c', 'b', 'bb', 'bbb', 'a', 'aa', 'aaa', 's', 'sp', 'ss', 'ssp', 'sss', 'sssp']
        index = 13
        if achievement < 50:
            index = 0
        elif achievement < 60:
            index = 1
        elif achievement < 70:
            index = 2
        elif achievement < 75:
            index = 3
        elif achievement < 80:
            index = 4
        elif achievement < 90:
            index = 5
        elif achievement < 94:
            index = 6
        elif achievement < 97:
            index = 7
        elif achievement < 98:
            index = 8
        elif achievement < 99:
            index = 9
        elif achievement < 99.5:
            index = 10
        elif achievement < 100:
            index = 11
        elif achievement < 100.5:
            index = 12

        return rate[index]
    
    def _chartfilter(self, data:Dict) -> Dict:
        data["ra"] = self._computeRa(data["ds"],data["achievements"])
        return data
    

class ChartInfo:
    '''单曲信息'''
    def __init__(self, idNum:str, diff:int, tp:str, achievement:float, ra:int, comboId:int, syncId:int, scoreId:int,
                 title:str, ds:float, lv:str):
        self.idNum = idNum
        self.diff = diff
        self.tp = tp
        self.achievement = achievement
        self.ra = ra
        self.comboId = comboId
        self.syncId = syncId
        self.scoreId = scoreId
        self.title = title
        self.ds = ds
        self.lv = lv

    def __eq__(self, other):
        return self.ra == other.ra
    
    def __lt__(self, other):
        return self.ra < other.ra
    

    @classmethod
    def from_b50json(cls, data):
        rate = ['d', 'c', 'b', 'bb', 'bbb', 'a', 'aa', 'aaa', 's', 'sp', 'ss', 'ssp', 'sss', 'sssp']
        ri = rate.index(data["rate"])
        fc = ['', 'fc', 'fcp', 'ap', 'app']
        fi = fc.index(data["fc"])
        fs = ['', 'fs', 'fsp', 'fsd', 'fsdp']
        fsi = fs.index(data["fs"])
        return cls(
            idNum=str(data["song_id"]),
            title=data["title"],
            diff=data["level_index"],
            ra=data["ra"],
            ds=data["ds"],
            comboId=fi,
            syncId=fsi,
            scoreId=ri,
            lv=data["level"],
            achievement=data["achievements"],
            tp=data["type"]
        )
    
    @classmethod
    def from_totalScorejson(cls, data, musicdata):
        return cls.from_b50json(ChartFilter(data, musicdata).data)


class BestList:
    def __init__(self, size:int):
        self.data:List[ChartInfo] = []
        self.size = size
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]
    
    def push_ra(self, elem:ChartInfo):
        if len(self.data) >= self.size and elem < self.data[-1]:
            return
        self.data.append(elem)
        self.data.sort()
        self.data.reverse()
        while(len(self.data) > self.size):
            del self.data[-1]

    def push_ach(self, elem:ChartInfo):
        if len(self.data) >= self.size and elem.achievement < self.data[-1].achievement:
            return
        self.data.append(elem)
        self.data.sort(key=lambda a:a.achievement)
        self.data.reverse()
        while(len(self.data) > self.size):
            del self.data[-1]

    def pop(self):
        del self.data[-1]


class UserInfo:
    def __init__(self, username:str, qq:str, rating_trend:Dict, frame_id:str, score_type:str, times:int, data:List[Dict], isnewuser:bool):
        self.username = username
        self.qq = qq
        self.rating_trend = rating_trend
        self.frame_id = frame_id
        self.score_type = score_type
        self.times = times
        self.data = data
        self.isnewuser = isnewuser

    def set_qq(self, qq:str):
        self.qq = qq

    def set_frame_id(self, frame_id:str):
        self.frame_id = frame_id

    def set_score_type(self, score_type:str):
        self.score_type = score_type

    def add_rating(self, rating:int):
        if len(self.rating_trend['date']) == 0 or self.rating_trend['rating'][-1] < rating:
            self.rating_trend['date'].append(int(time.time()))
            self.rating_trend['rating'].append(rating)

    def save_user(self):
        newuser = True
        for user in self.data:
            if user['username'] == self.username:
                newuser = False
                user['qq'] = self.qq
                user["rating_trend"] = self.rating_trend
                user["frame_id"] = self.frame_id
                user['score_type'] = self.score_type
                user['times'] = self.times + 1
        if newuser:
            userinfo = {}
            userinfo['username'] = self.username
            userinfo['qq'] = self.qq
            userinfo["rating_trend"] = self.rating_trend
            userinfo["frame_id"] = self.frame_id
            userinfo['score_type'] = self.score_type
            userinfo['times'] = 1
            self.data.append(userinfo)
        with open(plugin_dir + '/static/user_info.json', 'w', encoding='utf-8') as r:
            json.dump(self.data, r, indent=4, ensure_ascii=False)
    
    @classmethod
    def find_user(cls, username:str):
        with open(plugin_dir + '/static/user_info.json', 'r', encoding='utf-8') as f:
            json1: List[Dict] = json.load(f)

            for user in json1:
                if user['username'] == username:
                    return cls(
                        username = user["username"],
                        qq = user["qq"],
                        rating_trend = user["rating_trend"],
                        frame_id = user["frame_id"],
                        score_type = user["score_type"],
                        times = user["times"],
                        data = json1,
                        isnewuser = False
                    )
            # 未找到，返回新用户默认值
            return cls(
                username = username,
                qq = "",
                rating_trend = {"date":[], "rating":[]},
                frame_id = "209507",
                score_type = "TTR",
                times = 0,
                data = json1,
                isnewuser = True
            )
        

                
