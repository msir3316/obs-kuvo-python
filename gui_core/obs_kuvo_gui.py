import tkinter as tk
from tkinter import messagebox
import re
from core import obs_controller
import obswebsocket.exceptions
from utl import my_exception, error_logger

app_version = "v1.1.0dev"

class OBS_KUVO_GUI():
    def __init__(self):

        self.root = tk.Tk()
        # self.myapp = MainFrame(master=self.root)
        self.root.title("obs-kuvo-python")
        # self.myapp.master.geometry("450x240")

        self.obs = None
        self.connectOBS()

        """
        OBSにアクセスする部分
        """
        obscnctFrame = tk.Frame(self.root)
        obscnctFrame.pack(fill="x")

        app_version_label = tk.Label(obscnctFrame, text=app_version)
        app_version_label.pack(side="left")
        # obs_button = tk.Button(obscnctFrame, text="OBSに接続")
        # obs_button.pack(side="left")

        """
        番号を入力してアクセスする部分
        """
        acccessFrame = tk.Frame(self.root, bd=2)
        acccessFrame.pack(fill="x")

        # ラベル
        input_label = tk.Label(acccessFrame, text="KUVOのプレイリスト番号を入力")
        # input_label.grid(row=0, column=0, sticky=tk.W)
        input_label.pack(side="left")

        # 入力欄
        self.kuvonum_input = tk.Entry(acccessFrame, width=10)
        self.kuvonum_input.pack(side="left", expand=True, fill="x")

        # ボタン
        button = tk.Button(acccessFrame, text="接続", command=self.kuvo_playlistnum_input)
        button.pack(side="left")

        """
        接続してから操作する部分
        """
        ctrlFrame = tk.Frame(self.root)
        ctrlFrame.pack(fill="x")

        standby_button = tk.Button(ctrlFrame, text="初期化", command=self.init_layout)
        standby_button.pack(side="left")

        ok_button = tk.Button(ctrlFrame, text="準備OK", command=self.standby_ok)
        ok_button.pack(side="left")

        reload_button = tk.Button(ctrlFrame, text="リロード", command=self.reload)
        reload_button.pack(side="left")

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
            self.obs.close()
            self.root.destroy()

    def get_clipboard_enable(self):
        return self.clpbd_bln.get()

    def connectOBS(self):
        try:
            self.obs = obs_controller.OBScontroller()
        except obswebsocket.exceptions.ConnectionFailure:
            self.noteOBSconnection()
            exit()

    def kuvo_playlistnum_input(self):
        input_value = self.kuvonum_input.get()
        if input_value == "":
            return

        if re.match("^\d*$", input_value):
            playlistnum = int(input_value)
            self.access(playlistnum)
        else:
            messagebox.showerror("エラー", "数字のみで入力してください。")

    def access(self, playlistnum):
        self.obs.access_kuvo(playlistnum)
        self.music_info()

    def standby_ok(self):
        self.obs.standby_ok()

    def init_layout(self):
        if messagebox.askokcancel("初期化", "初期化しますか？"):
            self.obs.init_layout()

    def music_info(self):
        try:
            self.obs.show_music_info(self)
        except my_exception.KuvoPageNotFoundException:
            self.playlistNotFound()
        except my_exception.TrackInfoNotFoundException:
            self.trackNotFound()
        except Exception:
            error_logger.print_error("kuvo")
            self.showError()

    def reload(self):
        self.obs.reload()
        self.music_info()


    def hide(self):
        self.obs.hide_music_info()


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

    def showError(self):
        messagebox.showerror("エラー","予期しないエラーが発生しました。詳細はログを確認してください。")