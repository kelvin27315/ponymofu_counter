"""
1週間の状況を可視化
"""
from grapher import Grapher

def main():
    delta_days = 7
    mizore = Grapher(delta_days)
    mizore.make_graph_of_counts_per_daily("weekly_graph.png")
    mizore.make_glaph_of_counts_per_hourly("weekly_graph_per_hourly.png")
    mizore.post(("weekly_graph.png","weekly_graph_per_hourly.png"))

if __name__ == "__main__":
    main()