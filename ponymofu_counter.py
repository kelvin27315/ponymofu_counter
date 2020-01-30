"""
1日の発言を収集して，ぽにてをモフった数を数える
"""

from mastodon import Mastodon
from pytz import timezone
from pathlib import Path
import datetime as dt
import pandas as pd
import re

class Ponytail_Counter(Mastodon):
    def __init__(self, id=22674):
        self.path = Path(__file__).parent.resolve()
        self.id = id
        self.ponytail = 0
        self.kedama = 0

        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        #1日の始まりの時刻(JST)
        self.day_start = timezone("Asia/Tokyo").localize(dt.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0, 0))
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
        #時間内のtootのみcontentを追加する
        for toot in toots:
            time = toot["created_at"].astimezone(timezone("Asia/Tokyo"))
            if self.day_start <= time and time < self.day_end:
                #CWの呟きの場合,隠されている方も追加する
                text = toot["content"]
                text = "{} {}".format(toot["content"], toot["spoiler_text"]) if toot["sensitive"] == True else toot["content"]
                #もふってるのを探して数える
                if re.search(r"(ぽにて|ポニテ)(もふ|モフ)り(たい|てぇ)", text) is not None:
                    self.ponytail += 1
                if re.search(r"毛玉(吐|は)いた", text) is not None:
                    self.kedama += 1

    def post(self):
        """
        投稿
        """
        user = self.account(self.id)
        post = "{}年{}月{}日に {} ( @{} )がぽにてをモフろうとした回数は{}回です。毛玉を吐いた回数は{}回です。".format(
            self.day_start.year,self.day_start.month, self.day_start.day, user["display_name"], user["username"], self.ponytail, self.kedama
        )
        self.status_post(status=post, visibility="unlisted")

def main():
    kasaki = Ponytail_Counter()
    kasaki.count_ponytail()
    kasaki.post()

if __name__ == "__main__":
    main()