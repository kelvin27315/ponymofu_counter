from mastodon import Mastodon
from pathlib import Path
import os

"""
アプリケーションの登録とアカウントへの認証を行う
"""

def check_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def main():
    url = "https://mstdn.poyo.me"
    path = Path(__file__).parent.resolve()
    paths = [str(path/"token"), str(path/"data"), str(path/"data"/"all"), str(path/"data"/"ponytail"), str(path/"data"/"kedama")]
    for path in paths:
        check_dir(path)

    Mastodon.create_app(
        client_name = "ponymofu_counter",
        scopes = ["read", "write"],
        website = "https://github.com/kelvin27315/ponymofu_counter",
        to_file = path / "clientcred.secret",
        api_base_url = url
    )

    mastodon = Mastodon(client_id = (path/"clientcred.secret"), api_base_url = url)

    mail = "*****@example.com"
    password = "*****"
    mastodon.log_in(
        mail, password,
        scopes = ['read', 'write'],
        to_file = path / "usercred.secret"
    )

if __name__ == "__main__":
    main()