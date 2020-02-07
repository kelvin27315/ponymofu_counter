"""
1週間の状況を可視化
"""

from mastodon import Mastodon
from pathlib import Path
from matplotlib import ticker
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import seaborn as sns
sns.set()
import japanize_matplotlib

class Mofumofu_visualizer(Mastodon):
    def __init__(self, id=22674):
        self.id = id
        self.path = Path(__file__).parent.resolve()
        self.day = dt.date.today() - dt.timedelta(days=1)

        super(Mofumofu_visualizer, self).__init__(
            client_id = self.path/"token"/"clientcred.secret",
            access_token = self.path/"token"/"usercred.secret",
            api_base_url = "https://mstdn.poyo.me"
        )

    def make_graph(self):
        days = [str(self.day - dt.timedelta(days=6-i))for i in range(7)]
        file_paths = [str(self.path / "data" / "kedama" / "{}.pkl".format(day)) for day in days]
        kedama = [len(pd.read_pickle(file_path)) for file_path in file_paths]
        file_paths = [str(self.path / "data" / "ponytail" / "{}.pkl".format(day)) for day in days]
        ponytail = [len(pd.read_pickle(file_path)) for file_path in file_paths]
        days = [day[-5:] for day in days]
        data = pd.concat([pd.DataFrame({
            "種類": "ぽにて",
            "回数": ponytail,
            "日付": days
        }),pd.DataFrame({
            "種類": "毛玉",
            "回数": kedama,
            "日付": days
        })])

        fig = plt.figure()
        sns.lineplot(x="日付", y="回数", hue="種類", style="種類", markers=True, dashes=False, data=data)
        #color="#ed86b3", color="#6cc5ed"
        week = self.day - dt.timedelta(days=7)
        plt.title("{}年{}月{}日〜{}年{}月{}日の間で、\nぽにてをモフろうとした回数、毛玉を吐いた回数".format(
            week.year,week.month,week.day, self.day.year,self.day.month, self.day.day
        ))
        plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
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
    mizore = Mofumofu_visualizer()
    mizore.make_graph()
    mizore.post()

if __name__ == "__main__":
    main()