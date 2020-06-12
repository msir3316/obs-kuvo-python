import datetime, traceback, os

def print_error(process):
    now_time = datetime.datetime.now()
    dtstr = now_time.strftime('log/{}_%Y-%m-%d_%H-%M-%S.%f'.format(process))
    log_path = dtstr + ".log"
    if not os.path.exists("log"):
        mkdir_log()
    with open(log_path, 'a') as f:
        traceback.print_exc(file=f)


def mkdir_log():
    import subprocess
    if os.name == "nt":
        # Windows
        subprocess.run(["mkdir", "log"], shell=True)
    elif os.name == "posix":
        # Mac, Linux
        subprocess.run(["mkdir", "log"])