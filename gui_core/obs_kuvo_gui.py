import tkinter as tk
from tkinter import messagebox
import re, pyperclip
from core import obs_controller, kuvoinfogetter
import obswebsocket.exceptions
from utl import my_exception, error_logger

app_version = "v1.1.0dev"

class OBS_KUVO_GUI():
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("obs-kuvo-python")

        self.obs = None
        self.kuvo = None

        """
        接続する部分
        """
        cnctFrame = tk.Frame(self.root)
        cnctFrame.pack(fill="x")

        app_version_label = tk.Label(cnctFrame, text=app_version)
        app_version_label.pack(side="left")

        obs_button = tk.Button(cnctFrame, text="OBSに接続", command=self.connectOBS)
        obs_button.pack(side="left")

        """
        番号を入力してアクセスする部分
        """
        acccessFrame = tk.Frame(self.root, bd=2)
        acccessFrame.pack(fill="x")

        # ラベル
        input_label = tk.Label(acccessFrame, text="KUVOのプレイリスト番号を入力")
        input_label.pack(side="left")

        # 入力欄
        self.kuvonum_input = tk.Entry(acccessFrame, width=10)
        self.kuvonum_input.pack(side="left", expand=True, fill="x")

        # ボタン
        button = tk.Button(acccessFrame, text="接続", command=self.kuvo_playlistnum_input)
        button.pack(side="left")

        reload_button = tk.Button(acccessFrame, text="リロード", command=self.reload)
        reload_button.pack(side="left")

        """
        情報を表示する部分
        """
        infoFrame = tk.Frame(self.root)
        infoFrame.pack(fill="x")

        title_label = tk.Label(infoFrame,text="Title")
        title_label.grid(row=0, column=0)
        self.title_info = tk.Entry(infoFrame)
        self.title_info.grid(row=0, column=1, sticky=(tk.W, tk.E))

        artist_label = tk.Label(infoFrame, text="Artist")
        artist_label.grid(row=1, column=0)
        self.artist_info = tk.Entry(infoFrame)
        self.artist_info.grid(row=1, column=1, sticky=(tk.W, tk.E))

        """
        接続してから操作する部分
        """
        ctrlFrame = tk.Frame(self.root)
        ctrlFrame.pack(fill="x")

        obs_label = tk.Label(ctrlFrame, text="OBSの操作")
        obs_label.pack(side="left")

        standby_button = tk.Button(ctrlFrame, text="初期化", command=self.init_layout)
        standby_button.pack(side="left")

        ok_button = tk.Button(ctrlFrame, text="準備OK", command=self.standby_ok)
        ok_button.pack(side="left")

        hide_button = tk.Button(ctrlFrame, text="隠す", command=self.hide)
        hide_button.pack(side="left")

        """
        追加機能部分
        """
        additionalFrame = tk.Frame(self.root)
        additionalFrame.pack(fill="x")

        #チェックボックス用の状態はこちらで指定
        self.clpbd_bln = tk.BooleanVar()
        self.clpbd_bln.set(False)
        clipboard_check = tk.Checkbutton(additionalFrame, text="取得時にクリップボードにコピー", variable=self.clpbd_bln)
        clipboard_check.pack(side="left")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("終了", "終了しますか？"):
            if self.obs:
                self.obs.close()
            if self.kuvo:
                self.kuvo.close()
            self.root.destroy()

    def get_clipboard_enable(self):
        return self.clpbd_bln.get()

    def kuvo_playlistnum_input(self):
        input_value = self.kuvonum_input.get()
        if input_value == "":
            return

        if re.match("^\d*$", input_value):
            playlistnum = int(input_value)
            self.access(playlistnum)
        else:
            messagebox.showerror("エラー", "数字のみで入力してください。")

    """
    OBSと接続
    """
    def connectOBS(self):
        try:
            self.obs = obs_controller.OBScontroller()
            self.noteOBSconnectionSuccessful()
        except obswebsocket.exceptions.ConnectionFailure:
            self.noteOBSconnection()


    """
    selenium起動、ページにアクセス
    """
    def access(self, playlistnum):
        if self.kuvo is None:
            self.kuvo = kuvoinfogetter.KuvoGetter()
        self.kuvo.access(playlistnum)
        self.music_info()

    """
    ページ内の情報を取得、OBSとクリップボードにそれを送る
    """
    def music_info(self):
        try:
            title, artist = self.kuvo.get_music_info()
            self.show_music_info(title,artist)
            if self.obs:
                self.obs.setMusicInfo(title, artist)
            if self.get_clipboard_enable():
                self.copy_to_clipboard(title, artist)

        except my_exception.KuvoPageNotFoundException:
            self.playlistNotFound()
        except my_exception.TrackInfoNotFoundException:
            self.trackNotFound()

    """
    テキストボックスに取得した情報の表示
    """
    def show_music_info(self, title, artist):
        self.title_info.delete(0, tk.END)
        self.title_info.insert(0, title)
        self.artist_info.delete(0, tk.END)
        self.artist_info.insert(0, artist)

    """
    リロード
    """
    def reload(self):
        if self.kuvo:
            self.kuvo.refresh()
            self.music_info()


    """
    OBSへの命令
    """
    def hide(self):
        if self.obs:
            self.obs.hide_music_info()

    def standby_ok(self):
        if self.obs:
            self.obs.standby_ok()

    def init_layout(self):
        if self.obs:
            if messagebox.askokcancel("初期化", "初期化しますか？"):
                self.obs.init_layout()

    """
    クリップボードにコピー
    """
    def copy_to_clipboard(self, title, artist):
        """
        クリップボードに情報をコピー。OBS以外の用途
        少なくとも曲名がないなんてことはないはずなのでtitleは未処理
        """
        if artist == "":
            pyperclip.copy("♪ {}".format(title))
        else:
            pyperclip.copy("♪ {} - {}".format(title, artist))


    """
    諸々のメッセージボックス
    """
    def noteOBSconnectionSuccessful(self):
        messagebox.showinfo("OBSに接続","OBSと接続しました。")

    """
    エラー周りのメッセージボックス
    """
    def noteOBSconnection(self):
        messagebox.showerror("エラー", "OBSとの接続に失敗しました。以下を確認してください。\n"
                                   "\n・先にOBSを起動し、websocketサーバを有効にしているか"
                                   "\n・websocketサーバとconfig.iniのパスワード等の記述が正しいか")

    def playlistNotFound(self):
        messagebox.showerror("エラー","指定したKUVOのプレイリストは存在しません。")

    def trackNotFound(self):
        messagebox.showerror("エラー","トラック情報を取得することができませんでした。")