from gui_core import obs_kuvo_gui
from utl import error_logger
from tkinter import messagebox


def showError():
    messagebox.showerror("エラー", "予期しないエラーが発生しました。詳細はログを確認してください。")

try:
    app = obs_kuvo_gui.OBS_KUVO_GUI()
    app.run()
except Exception as e:
    error_logger.print_error("main")
    showError()
    exit(1)
