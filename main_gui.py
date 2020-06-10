from gui_core import obs_kuvo_gui
import datetime, traceback, os

def print_error():
    now_time = datetime.datetime.now()
    dtstr = now_time.strftime('log/%Y-%m-%d_%H-%M-%S.%f'.format())
    log_path = dtstr + ".log"
    if not os.path.exists(log_path):
        mkdir_log()
    with open(dtstr + ".log", 'a') as f:
        traceback.print_exc(file=f)

def mkdir_log():
    import subprocess
    if os.name == "nt":  # Windows
        subprocess.run(["mkdir", "log"], shell=True)
    elif os.name == "posix": #Mac, Linux
        subprocess.run(["mkdir", "log"])

try:
    app = obs_kuvo_gui.OBS_KUVO_GUI()
    app.run()
except Exception as e:
    print_error()
