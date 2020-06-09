import tkinter as tk
from tkinter import messagebox
import re


class OBS_KUVO_GUI():
    def __init__(self):

        self.root = tk.Tk()
        self.myapp = MainFrame(master=self.root)
        self.myapp.master.title("obs-kuvo-python")
        self.myapp.master.geometry("450x240")

    def run(self):
        self.myapp.mainloop()


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # ラベルの作成
        input_label = tk.Label(text="KUVOのプレイリスト番号を入力")
        input_label.grid(row=0, column=0, padx=5, pady=5)

        self.kuvonum_input = tk.Entry(width=10)
        self.kuvonum_input.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

        # ボタンの作成
        button = tk.Button(text="実行ボタン", command=self.kuvo_playlistnum_input)
        button.grid(row=0, column=2, padx=5, pady=5)

    # ボタンがクリックされたら実行
    def kuvo_playlistnum_input(self):
        input_value = self.kuvonum_input.get()
        if input_value == "":
            return

        if re.match("^\d*$", input_value):
            messagebox.showinfo("入力確認", input_value + "が入力されました。")
        else:
            messagebox.showinfo("エラー", "数字のみで入力してください。")

class ObsCtrlFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.pack()

    def create_wedgets(self):
        pass
