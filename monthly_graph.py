"""
1ヶ月の状況を可視化
"""

from dateutil.relativedelta import relativedelta
import datetime as dt
from grapher import Grapher

def main():
    delta_days = (dt.date.today() - (dt.date.today() - relativedelta(months=1))).days
    mizore = Grapher(delta_days)
    mizore.make_graph_of_counts_per_daily("monthly_graph.png")
    mizore.make_glaph_of_counts_per_hourly("monthly_graph_per_hourly.png")
    mizore.post(("monthly_graph.png","monthly_graph_per_hourly.png"))

if __name__ == "__main__":
    main()