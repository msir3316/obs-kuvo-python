# obs-kuvo-python

obs-websocketとPythonを使って、KUVO経由でrekordboxで流している曲の情報を表示するやつ

# 環境構築
1. OBSに [obs-websocket](https://github.com/Palakis/obs-websocket/) をインストール
1. Python 3系をインストール
1. `$ pip install beautifulsoup4, selenium, obs-websocket-py`
1. [chromedriver](http://chromedriver.chromium.org/downloads) をダウンロード
1. このリポジトリをgit clone
1. このリポジトリ同梱のconfig.iniの\[selenium]を設定

# OBSの準備
1. OBS起動
1. 「title」「artist」「standby」のテキストソースを作る
    1. 「title」「artist」はそれぞれ曲名とアーティスト名の表示欄になる
    1. 「standby」は初期化時の準備状態を表すテキスト。お好みで「準備中」とか書いといて
1. 「title」「artist」に「scroll」という名前でスクロールのフィルターを作る
1. このリポジトリ同梱のconfig.iniの\[sources_config]と\[client]を設定
1. OBSメニューから「ツール -> Websocket Server Settings」で設定

# 使い方
1. `$ cd obs-kubo-python`
1. `$ cd python main.py`
1. `$ 初期化する？(y or n):` -> 「y」
    1. なんか落ちたとかでDJしてる途中から起動した場合は「n」
1. KUVOをONにした状態で、rekordboxで何か曲を流す
1. https://kuvo.com/mykuvo/djmix/playlist に新しいプレイリストができるので開く
1. URLに番号が載ってるので控える
1. `$ ENTERで準備状態を解除します。曲を流してください(KUVOのオンを忘れずに):` -> 何も入力せずにENTER
1. `$ KUVOのプレイリストの番号を入力:` -> さっき控えた番号を入力

# `ENTERでリロード, hで伏せる, zで終了:` が表示されてから
- 何も入力せずにENTERでリロード
- 「h」で「???」と表示する。隠したいときなどに。ご活用ください
- 「z」で終了、OBSとの接続を切ります

# FAQ
- Q. SessionNotCreatedExceptionって出た
    - A. 多分使ってるChromeとChromeDriverのバージョンが合ってない。
- Q. Windowsでよくわからん表示が出る
    - A. `$ KUVOのプレイリストの番号を入力:` は出てるはずだからとりあえず機能する。わしWindowsのことはようわからんへん
