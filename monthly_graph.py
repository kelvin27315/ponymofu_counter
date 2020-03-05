"""
1ヶ月の状況を可視化
"""

from dateutil.relativedelta import relativedelta
import datetime as dt
from grapher import Grapher

def main():
    delta_days = (dt.date.today() - (dt.date.today() - relativedelta(months=1))).days
    mizore = Grapher(delta_days)
    mizore.make_graph("monthly_graph.png")
    mizore.post()

if __name__ == "__main__":
    main()