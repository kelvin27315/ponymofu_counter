"""
グラフを作成
"""

from mastodon import Mastodon
from pathlib import Path
from matplotlib import ticker
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import seaborn as sns
sns.set()
import japanize_matplotlib

class Grapher(Mastodon):
    def __init__(self, delta_days, id=22674):
        self.delta_days = delta_days
        self.id = id
        self.path = Path(__file__).parent.resolve()
        self.day = dt.date.today() - dt.timedelta(days=1)

        super(Grapher, self).__init__(
            client_id = self.path/"token"/"clientcred.secret",
            access_token = self.path/"token"/"usercred.secret",
            api_base_url = "https://mstdn.poyo.me"
        )

    def get_counts(self, count_type, days):
        file_paths = [str(self.path / "data" / count_type / "{}.pkl".format(day)) for day in days]
        counts = [len(pd.read_pickle(file_path)) for file_path in file_paths]
        return(counts)

    def make_graph(self,file_name):
        days = [str(self.day - dt.timedelta(days=self.delta_days-1-i))for i in range(self.delta_days)]

        kedama_counts = self.get_counts("kedama", days)
        ponytail_counts = self.get_counts("ponytail", days)

        #日付の文字列のList。年号も入っているのでそれを落とす
        days = [day[-5:] for day in days]

        data = pd.concat([pd.DataFrame({
            "種類": "ぽにて",
            "回数": ponytail_counts,
            "日付": days
        }),pd.DataFrame({
            "種類": "毛玉",
            "回数": kedama_counts,
            "日付": days
        })])

        fig = plt.figure()
        sns.lineplot(x="日付", y="回数", hue="種類", style="種類", markers=True, dashes=False, data=data)
        #color="#ed86b3", color="#6cc5ed"
        month = dt.date.today() - relativedelta(months=1)
        plt.title("{}年{}月{}日〜{}年{}月{}日の間で、\nぽにてをモフろうとした回数、毛玉を吐いた回数".format(
            month.year,month.month,month.day, self.day.year,self.day.month, self.day.day
        ))
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
        plt.savefig(self.path / file_name)

    def post(self, file_name):
        user = self.account(self.id)
        month = dt.date.today() - relativedelta(months=1)
        post = "{}年{}月{}日〜{}年{}月{}日の間で、 {} ( @{} )がぽにてをモフろうとした回数、毛玉を吐いた回数についてのグラフです。".format(
            month.year,month.month,month.day, self.day.year,self.day.month, self.day.day, user["display_name"], user["username"]
        )
        media = [self.media_post(str(self.path / file_name))]
        self.status_post(post, media_ids = media, visibility="unlisted")