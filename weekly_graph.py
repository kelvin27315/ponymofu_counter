"""
1週間の状況を可視化
"""
from grapher import Grapher

def main():
    delta_days = 7
    mizore = Grapher(delta_days)
    mizore.make_graph("weekly_graph.png")
    mizore.post()

if __name__ == "__main__":
    main()