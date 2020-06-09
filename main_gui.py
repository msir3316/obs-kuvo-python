from gui_core import obs_kuvo_gui
import datetime, traceback, os

def print_error():
    try:
        now_time = datetime.datetime.now()
        dtstr = now_time.strftime('log/%Y-%m-%d_%H-%M-%S.%f'.format())
        with open(dtstr + ".log", 'a') as f:
            traceback.print_exc(file=f)
    except FileNotFoundError:
        mkdir_log()
        print_error()

def mkdir_log():
    import subprocess
    if os.name == "nt":  # Windows
        subprocess.run(["mkdir", "log"], shell=True)
    elif os.name == "posix": #Mac, Linux
        subprocess.run(["mkdir","log"])

try:
    app = obs_kuvo_gui.OBS_KUVO_GUI()

    raise Exception
except Exception as e:
    print_error()
    exit(1)
