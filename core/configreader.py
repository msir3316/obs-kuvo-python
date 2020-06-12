import configparser, os, errno, sys


def read_config():
    if os.name == "posix":  # Linux, Mac
        #Mac app用
        exctbl = sys.executable
        if "app/Contents" in exctbl:
            LiPath = exctbl.split('/')
            sPath = '/'.join(LiPath[:-4])
            config_path = sPath + "/config.ini"
        else:
            config_path = "config.ini"
    else:
        config_path = "config.ini"
    config_ini = configparser.ConfigParser()

    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)

    config_ini.read(config_path, encoding='utf-8')

    return config_ini
