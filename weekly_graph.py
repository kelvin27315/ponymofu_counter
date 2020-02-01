"""
1週間の状況を可視化
"""

from mastodon import Mastodon
from pathlib import Path
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import japanize_matplotlib

class Yoroizuka(Mastodon):
    def __init__(self, id=22674):
        self.id = id
        self.path = Path(__file__).parent.resolve()
        self.day = dt.date.today() - dt.timedelta(days=1)

        super(Yoroizuka, self).__init__(
            client_id = self.path/"token"/"clientcred.secret",
            access_token = self.path/"token"/"usercred.secret",
            api_base_url = "https://mstdn.poyo.me"
        )

    def make_graph(self):
        x1 = range(7)
        x2 = [i + 0.4 for i in range(7)]
        file_paths = [str(self.path / "data" / "kedama" / "{}.pkl".format(self.day - dt.timedelta(days=6-i))) for i in range(7)]
        kedama = [len(pd.read_pickle(file_path)) for file_path in file_paths]
        file_paths = [str(self.path / "data" / "ponytail" / "{}.pkl".format(self.day - dt.timedelta(days=6-i))) for i in range(7)]
        ponytail = [len(pd.read_pickle(file_path)) for file_path in file_paths]

        plt.figure(figsize=(8,5))
        plt.bar(x1,kedama, 0.4,label="毛玉",color="#ed86b3")
        plt.bar(x2,ponytail, 0.4,label="ぽにて",color="#6cc5ed")
        week = self.day - dt.timedelta(days=7)
        plt.title("{}年{}月{}日〜{}年{}月{}日の間で、ぽにてをモフろうとした回数、毛玉を吐いた回数".format(
            week.year,week.month,week.day, self.day.year,self.day.month, self.day.day
        ))
        plt.xlabel("日付")
        plt.ylabel("回数")
        days = [str(self.day - dt.timedelta(days=6-i))[-5:] for i in range(7)]
        plt.xticks([i+0.2 for i in range(7)], days)
        plt.legend()
        plt.savefig(self.path / "weekly_graph.png")

    def post(self):
        user = self.account(self.id)
        week = self.day - dt.timedelta(days=7)
        post = "{}年{}月{}日〜{}年{}月{}日の間で、 {} ( @{} )がぽにてをモフろうとした回数、毛玉を吐いた回数についてのグラフです。".format(
            week.year,week.month,week.day, self.day.year,self.day.month, self.day.day, user["display_name"], user["username"]
        )
        media = [self.media_post(str(self.path / "weekly_graph.png"))]
        self.status_post(post, media_ids = media, visibility="unlisted")

def main():
    mizore = Yoroizuka()
    mizore.make_graph()
    mizore.post()

if __name__ == "__main__":
    main()