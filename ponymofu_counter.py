"""
1日の発言を収集して，ぽにてをモフった数を数える
"""

from mastodon import Mastodon
from pytz import timezone
from pathlib import Path
import datetime as dt
import pandas as pd
import re

def extract_content(text):
        #HTMLタグ, URL, LSEP,RSEP, HTML特殊文字を取り除く
        text = re.sub(r"<[^>]*?>", "", text)
        text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "", text)
        text = re.sub(r"[  ]", "", text)
        return(text)

class Ponytail_Counter(Mastodon):
    def __init__(self, id=22674):
        self.path = Path(__file__).parent.resolve()
        self.id = id
        self.ponytail = 0
        self.kedama = 0

        today = dt.date.today()
        self.yesterday = today - dt.timedelta(days=1)
        #1日の始まりの時刻(JST)
        self.day_start = timezone("Asia/Tokyo").localize(dt.datetime(self.yesterday.year, self.yesterday.month, self.yesterday.day, 0, 0, 0, 0))
        #1日の終わりの時刻(JST)
        self.day_end = timezone("Asia/Tokyo").localize(dt.datetime(today.year, today.month, today.day, 0, 0, 0, 0))

        super(Ponytail_Counter, self).__init__(
            client_id = self.path/"token"/"clientcred.secret",
            access_token = self.path/"token"/"usercred.secret",
            api_base_url = "https://mstdn.poyo.me"
        )

    def get_toots(self):
        #tootの取得
        toots = self.account_statuses(id=self.id, limit=40)
        while toots[-1]["created_at"].astimezone(timezone("Asia/Tokyo")) > self.day_start:
            toots += self.account_statuses(id=self.id, max_id=toots[-1]["id"]-1, limit=40)
        return(toots)

    def count_ponytail(self):
        toots = self.get_toots()

        temp = []
        t_append = temp.append
        for toot in toots:
            time = toot["created_at"].astimezone(timezone("Asia/Tokyo"))
            if self.day_start <= time and time < self.day_end:
                t_append(toot)
                text = "{} {}".format(toot["content"], toot["spoiler_text"])
                #もふってるのを探して数える
                if re.search(r"(ぽにて|ポニテ)(もふ|モフ)り(たい|てぇ)", text) is not None:
                    self.ponytail += 1
                if re.search(r"(ぽにて|ポニテ)(吸|す)い(たい|てぇ)", text) is not None:
                    self.ponytail += 5
                if re.search(r"毛玉(吐|は)いた", text) is not None:
                    self.kedama += 1

        self.toots = pd.DataFrame({
            "date":         [toot["created_at"].astimezone(timezone("Asia/Tokyo")) for toot in temp],
            "content":      [extract_content(toot["content"]) for toot in temp],
            "spoiler_text": [extract_content(toot["spoiler_text"]) for toot in temp],
            "visibility":   [toot["visibility"] for toot in temp]
        })

    def post(self):
        """
        投稿
        """
        age = get_age_of_the_moon(self.day_start)
        moons = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘"]
        moon = moons[round((age*8/30))%8]
        user = self.account(self.id)
        post = "{}年{}月{}日(月齢: {}{})に {} ( @{} )がぽにてをモフろうとした回数は{}回です。毛玉を吐いた回数は{}回です。".format(
            self.day_start.year,self.day_start.month, self.day_start.day,
            age, moon, user["display_name"], user["username"], self.ponytail, self.kedama
        )
        self.status_post(status=post, visibility="unlisted")

    def data_save(self):
        file_name = "{}.pkl".format(self.yesterday)
        self.toots.to_pickle(self.path/"data"/"all"/file_name)
        if len(self.toots) == 0:
            self.toots.to_pickle(self.path/"data"/"ponytail"/file_name)
            self.toots.to_pickle(self.path/"data"/"kedama"/file_name)
        else:
            pickup_list = [True if re.search(r"(ぽにて|ポニテ)((吸|す)い|(もふ|モフ)り)(たい|てぇ)", "{} {}".format(toot["content"],toot["spoiler_text"])) is not None else False for i, toot in self.toots.iterrows()]
            self.toots[pickup_list].to_pickle(self.path/"data"/"ponytail"/file_name)
            pickup_list = [True if re.search(r"毛玉(吐|は)いた", "{} {}".format(toot["content"],toot["spoiler_text"])) is not None else False for i, toot in self.toots.iterrows()]
            self.toots[pickup_list].to_pickle(self.path/"data"/"kedama"/file_name)

def main():
    kasaki = Ponytail_Counter()
    kasaki.count_ponytail()
    kasaki.post()
    kasaki.data_save()

if __name__ == "__main__":
    main()