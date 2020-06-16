from obswebsocket import obsws, requests
import core.kuvoinfogetter as getkuvo
from core import configreader
import unicodedata, os

class OBScontroller():

    def __init__(self):
        config = configreader.read_config()

        host = config["client"]["host"]
        port = int(config["client"]["port"])
        password = config["client"]["password"]

        cx_title = int(config["sources_config"]["width_title"])
        cx_artist = int(config["sources_config"]["width_artist"])
        self.title_limit_length = int(config["sources_config"]["title_limit_length"])
        self.artist_limit_length = int(config["sources_config"]["artist_limit_length"])
        scroll_speed = float(config["sources_config"]["scroll_speed"])

        self.scroll_t_true = {'cx': cx_title, 'limit_cx': True, 'limit_cy': False, 'speed_x': scroll_speed}
        self.scroll_t_false = {'cx': cx_title, 'limit_cx': False, 'limit_cy': False, 'speed_x': 0.0}

        self.scroll_a_true = {'cx': cx_artist, 'limit_cx': True, 'limit_cy': False, 'speed_x': scroll_speed}
        self.scroll_a_false = {'cx': cx_artist, 'limit_cx': False, 'limit_cy': False, 'speed_x': 0.0}

        # OBSに接続
        self.ws = obsws(host, port, password)
        self.ws.connect()

    def setMusicInfo(self,title, artist):
        if title is not None and artist is not None:
            if title == "":
                title = " "
            if artist == "":
                artist = " "
            # 一定文字数以上ならスクロールさせる
            if self.get_east_asian_width_count(title) > self.title_limit_length:
                title = title + "　　"  # 見やすいようにスクロール用のスペースを開ける
                title_scroll = self.scroll_t_true
            else:
                title_scroll = self.scroll_t_false
            if self.get_east_asian_width_count(artist) > self.artist_limit_length:
                artist = artist + "　　"  # 見やすいようにスクロール用のスペースを開ける
                artist_scroll = self.scroll_a_true
            else:
                artist_scroll = self.scroll_a_false

            # 各種セット
            self.setText("title", title)
            self.ws.call(requests.SetSourceFilterSettings("title", "scroll", title_scroll))
            self.setText("artist", artist)
            self.ws.call(requests.SetSourceFilterSettings("artist", "scroll", artist_scroll))

    def setText(self, sourcename, text):
        # OS判別してGDI+かFreetype2か変わる
        if os.name == "nt":  # Windows
            self.ws.call(requests.SetTextGDIPlusProperties(sourcename, text=text))
        elif os.name == "posix":  # Mac, Linux
            self.ws.call(requests.SetTextFreetype2Properties(sourcename, text=text))

    # 表示非表示切り替え
    def setVisible(self, item, visible):
        self.ws.call(requests.SetSceneItemProperties(item, visible=visible))

    # 全角と半角を区別して文字数をカウント
    def get_east_asian_width_count(self, text):
        count = 0
        for c in text:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 1
            else:
                count += 0.5
        return count

    def main(self):
        while True:
            init_command = input("初期化する？(y or n):")
            if init_command == "y":
                # 初期化
                self.setText("title", "TITLE")
                self.setText("artist", "ARTIST")
                self.ws.call(requests.SetSourceFilterSettings("title", "scroll", self.scroll_t_false))
                self.ws.call(requests.SetSourceFilterSettings("artist", "scroll", self.scroll_a_false))

                self.setVisible("music_info", False)
                self.setVisible("standby", True)

                while True:
                    command = input("ENTERで準備状態を解除します。曲を流してください(KUVOのオンを忘れずに):")
                    if command == "":
                        self.setVisible("standby", False)
                        self.setVisible("music_info", True)
                        break
                break
            if init_command == "n":
                break

        playlist_num = input("KUVOのプレイリストの番号を入力:")
        kuvo = getkuvo.KuvoGetter(playlist_num)
        title, artist = kuvo.get_music_info()

        # 曲情報をセット
        self.setMusicInfo(title, artist)

        # 終了命令来るまでリロードでループさせる
        while True:
            command = input("ENTERでリロード, hで伏せる, 「#」を頭につけて任意のコメント, zで終了:")
            if command == "":
                kuvo.refresh()
                title, artist = kuvo.get_music_info()

                self.setMusicInfo(title, artist)

            elif command == "h":
                self.setMusicInfo("???", "???")

            elif command[0] == "#":
                comment = command[1:]
                self.setMusicInfo(comment, " ")

            elif command == "z":
                kuvo.close()
                break

        self.ws.disconnect()