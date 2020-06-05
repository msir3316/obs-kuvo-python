from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import traceback, os
from core import configreader

class KuvoGetter():

    def __init__(self, playlist_num):
        config = configreader.read_config("config.ini")
        try:
            target = "https://kuvo.com/playlist/" + str(playlist_num)
            options = Options()
            if os.name == "nt": # Windows
                options.binary_location = config["selenium"]["main_chrome_path"]
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options, executable_path=config["selenium"]["chromedriver_path"])
            self.driver.get(target)
        except Exception as e:
            print(e.with_traceback)

    def refresh(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()

    def get_music_info(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            if soup is None:
                return None

            track = soup.find_all(class_="row on")

            if track:
                title = track[0].find(class_="title")
                artist = track[0].find(class_="artist")
                return title.get_text(), artist.get_text()
            else:
                # row onがないときがたまにある。多分リストの最後に居座ってる
                tracklist = soup.find_all(class_="row off")
                if tracklist:
                    title = tracklist[-1].find(class_="title")
                    artist = tracklist[-1].find(class_="artist")
                    return title.get_text(), artist.get_text()
                return None, None

        except Exception as e:
            traceback.print_exc()
            return "!!Error Occurred!!", "!!エラーが発生しました!!"




