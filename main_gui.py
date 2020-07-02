from gui_core import obs_kuvo_gui
from utl import error_logger
from tkinter import messagebox

try:
    app = obs_kuvo_gui.OBS_KUVO_GUI()
    app.run()
except Exception as e:
    error_logger.print_error("main")
    obs_kuvo_gui.showError()
    exit(1)
