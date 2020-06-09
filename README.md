# obs-kuvo-python

obs-websocketとPythonを使って、KUVO経由でrekordboxで流している曲の情報を表示するやつ
<img src="./assets/example.png" width="800px" alt="使用例" />

## 動作確認済み
Mac, Windows

# OBSの準備
1. OBS起動
1. 「title」「artist」「standby」のテキストソースを作る
    1. 「title」「artist」はそれぞれ曲名とアーティスト名の表示欄になる
    1. 「standby」は初期化時の準備状態を表すテキスト。お好みで「準備中」とか書いといて
1. 「title」「artist」に「scroll」という名前でスクロールのフィルターを作る
1. 上記２つを「music_info」でグループ化
1. このリポジトリ同梱のconfig.iniの\[sources_config]と\[client]を設定
1. OBSメニューから「ツール -> Websocket Server Settings」で設定

# リポジトリをクローンして動かす方法
## 環境構築
1. OBSに [obs-websocket](https://github.com/Palakis/obs-websocket/) をインストール
1. Python 3系をインストール
1. `$ pip install beautifulsoup4, selenium, obs-websocket-py`
1. [chromedriver](http://chromedriver.chromium.org/downloads) をダウンロード
1. このリポジトリをgit clone、またはreleasesからソースをダウンロード
1. このリポジトリ同梱のconfig.iniの\[selenium]を設定

## <a name="jump-how2use">使い方</a>
1. `$ cd obs-kubo-python`
1. `$ python main.py`
1. `$ 初期化する？(y or n):` -> 「y」
    1. なんか落ちたとかでDJしてる途中から起動した場合は「n」、8へ
1. KUVOをONにした状態で、rekordboxで何か曲を流す
1. https://kuvo.com/mykuvo/djmix/playlist に新しいプレイリストができるので開く
1. URLに番号が載ってるので控える
1. `$ ENTERで準備状態を解除します。曲を流してください(KUVOのオンを忘れずに):` -> 何も入力せずにENTER
1. `$ KUVOのプレイリストの番号を入力:` -> さっき控えた番号を入力

## `ENTERでリロード, hで伏せる, zで終了:` が表示されてから
- 何も入力せずにENTERでリロード
- 「h」で「???」と表示する。隠したいときなどに。ご活用ください
- 「z」で終了、OBSとの接続を切ります

# GUIアプリケーションで動かす方法
現在Mac向けのappをリリースしています。Windows用exeはそのうち…
1. 同梱のconfig.iniを同様に編集
1. obs-kuvo-pythonを起動
1. テキストボックスにKUVOのプレイリスト番号を入力し、「接続」を押す
- 「初期化」ボタンは[使い方](#jump-how2use)の3.に相当
- 「準備OK」ボタンは7.に相当
- 後は見た通り
- 何かあったら`obs-kuvo-python.app/Contents/Resources/log`の中身を私に報告してください。

# FAQ
- Q. SessionNotCreatedExceptionって出た
    - A. 多分使ってるChromeとChromeDriverのバージョンが合ってない。
- Q. Windowsでよくわからん表示が出る
    - A. `$ ENTERでリロード, hで伏せる, zで終了:` は出てるはずだからとりあえず動く。Windowsのことはようわからんへん
- Q. OBSでソースのロックを切り替えたらInvalid event SceneItemLockChangedって出た
    - A. 最近obs-websocketに更新が入って、obs-websocket-pyがまだ対応していないっぽいので触らないように
- Q. 自動更新しないの？
    - A. それで想定外の表示とかされるよりかは…という理由で手動更新。秘匿機能(h)とかは手動の方が都合がいいだろうし。
    
# 連絡先
[Twitter](https://twitter.com/msir3316)

# 姉妹品
[obs-kuvo(suzu2464氏制作)](https://github.com/suzu2469/obs-kuvo)
