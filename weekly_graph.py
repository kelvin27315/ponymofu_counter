"""
1週間の状況を可視化
"""

from mastodon import Mastodon
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

class Yoroidsuka(Mastodon):
    def __init__(self, id=22674):
        self.id = id
        self.path = Path(__file__).parent.resolve()

        super(Yoroidsuka, self).__init__(
            client_id = self.path/"token"/"clientcred.secret",
            access_token = self.path/"token"/"usercred.secret",
            api_base_url = "https://mstdn.poyo.me"
        )

    def post(self):
        pass

def main():
    mizore = Yoroidsuka()

if __name__ == "__main__":
    main()