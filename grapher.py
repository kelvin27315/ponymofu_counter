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
import re
sns.set()
import japanize_matplotlib

def get_age_of_the_moon(day):
        c = {1:0, 2:2, 3:0, 4:2, 5:2, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10}
        age = (((day.year - 11) % 19) * 11 + c[day.month] + day.day) % 30
        #moons = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘"]
        #matplotlibで絵文字の出し方わからん
        #moon = moons[round((age*8/30))%8]
        return(age)

class Grapher(Mastodon):
    def __init__(self, delta_days, id=22674):
        self.delta_days = delta_days
        self.id = id
        self.path = Path(__file__).parent.resolve()
        self.day = dt.date.today() - dt.timedelta(days=1)
        self.from_day = dt.date.today() - dt.timedelta(days=self.delta_days)

        super(Grapher, self).__init__(
            client_id = self.path/"token"/"clientcred.secret",
            access_token = self.path/"token"/"usercred.secret",
            api_base_url = "https://mstdn.poyo.me"
        )

    def get_file_paths(self, count_type, days):
        file_paths = [str(self.path / "data" / count_type / "{}.pkl".format(str(day))) for day in days]
        return(file_paths)

    def get_daily_counts(self, count_type, days):
        file_paths = self.get_file_paths(count_type, days)
        if count_type == "ponytail":
            counts = [0] * len(file_paths)
            for i, file_path in enumerate(file_paths):
                df = pd.read_pickle(file_path)["content"]
                for toot in df:
                    counts[i] += 1 if re.search(r"(ぽにて|ポニテ)(もふ|モフ)り(たい|てぇ)", toot) is not None else 5
        else:
            counts = [len(pd.read_pickle(file_path)) for file_path in file_paths]
        return(counts)

    def get_hourly_counts(self, count_type, days):
        file_paths = self.get_file_paths(count_type, days)
        weekdays = []
        counts = []
        for file_path in file_paths:
            df = pd.read_pickle(file_path)
            if len(df) != 0:
                counts.extend([date[1]["date"].hour + date[1]["date"].minute/60 for date in df.iterrows()])
                weekdays.extend([date[1]["date"].weekday() for date in df.iterrows()])
        return(counts, weekdays)

    def make_graph_of_counts_per_daily(self,file_name):
        days = [self.day - dt.timedelta(days=self.delta_days-1-i) for i in range(self.delta_days)]

        kedama_counts = self.get_daily_counts("kedama", days)
        ponytail_counts = self.get_daily_counts("ponytail", days)

        #日付の文字列のList。年号も入っているのでそれを落とす
        days = [str(day)[-5:]+" 月齢"+str(get_age_of_the_moon(day)) for day in days]

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
        plt.title("{}年{}月{}日〜{}年{}月{}日の間で、\nぽにてをモフろうとした回数、毛玉を吐いた回数".format(
            self.from_day.year, self.from_day.month, self.from_day.day, self.day.year,self.day.month, self.day.day
        ))
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
        plt.savefig(self.path / "figure" / file_name)

    def make_glaph_of_counts_per_hourly(self,file_name):
        days = [self.day - dt.timedelta(days=self.delta_days-1-i) for i in range(self.delta_days)]
        kedama_counts, kedama_weekdays = self.get_hourly_counts("kedama", days)
        ponytail_counts, ponytail_weekdays = self.get_hourly_counts("ponytail", days)

        data = pd.concat([pd.DataFrame({
            "種類": "ぽにて",
            "時間": ponytail_counts,
            "曜日": ponytail_weekdays
        }),pd.DataFrame({
            "種類": "毛玉",
            "時間": kedama_counts,
            "曜日": kedama_weekdays
        })])

        weekday_dic = {0:"月",1:"火",2:"水",3:"木",4:"金",5:"土",6:"日"}

        fig = plt.figure()
        ax = fig.add_subplot(111)
        sns.violinplot(x="曜日", y="時間", hue="種類", data=data, inner="stick", split=True)
        plt.legend(loc="upper right", bbox_to_anchor=(1,-0.1), ncol=2)
        plt.ylim(0,24)
        plt.title("{}年{}月{}日〜{}年{}月{}日の間で、\nぽにてをモフろうとした事と毛玉を吐いた事の曜日と時間ごとの頻度".format(
            self.from_day.year, self.from_day.month, self.from_day.day, self.day.year,self.day.month, self.day.day
        ))
        ax.set_xticklabels([weekday_dic[w] for w in plt.xticks()[0]])
        plt.tight_layout()
        plt.savefig(self.path / "figure" / file_name)

    def post(self, file_names):
        user = self.account(self.id)
        post = "{}年{}月{}日〜{}年{}月{}日の間で、 {} ( @{} )がぽにてをモフろうとした事、毛玉を吐いた事についてのグラフです。".format(
            self.from_day.year, self.from_day.month, self.from_day.day, self.day.year, self.day.month, self.day.day, user["display_name"], user["username"]
        )
        media = [self.media_post(str(self.path / "figure" / file_name)) for file_name in file_names]
        self.status_post(post, media_ids = media, visibility="unlisted")