import tkinter as tk
from tkinter import messagebox
import re
from core import obs_controller

class OBS_KUVO_GUI():
    def __init__(self):

        self.root = tk.Tk()
        # self.myapp = MainFrame(master=self.root)
        self.root.title("obs-kuvo-python")
        # self.myapp.master.geometry("450x240")

        self.obs = obs_controller.OBScontroller()

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

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("終了", "終了しますか？"):
            self.obs.close()
            self.root.destroy()

    # ボタンがクリックされたら実行
    def kuvo_playlistnum_input(self):
        input_value = self.kuvonum_input.get()
        if input_value == "":
            return

        if re.match("^\d*$", input_value):
            playlistnum = int(input_value)
            self.access(playlistnum)
            # messagebox.showinfo("入力確認", input_value + "が入力されました。")
        else:
            messagebox.showinfo("エラー", "数字のみで入力してください。")

    def access(self, playlistnum):
        self.obs.access_kuvo(playlistnum)
        self.obs.show_music_info()

    def standby_ok(self):
        self.obs.standby_ok()

    def init_layout(self):
        if messagebox.askokcancel("初期化", "初期化しますか？"):
            self.obs.init_layout()

    def reload(self):
        self.obs.show_music_info()

    def hide(self):
        self.obs.hide_music_info()

