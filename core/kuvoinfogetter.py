from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from core import configreader
from utl import my_exception

class KuvoGetter():

    def __init__(self):
        config = configreader.read_config()

        options = Options()
        if os.name == "nt":
            # Windows
            options.binary_location = config["selenium"]["main_chrome_path"]
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options, executable_path=config["selenium"]["chromedriver_path"])

    def access(self, playlist_num):
        target = "https://kuvo.com/playlist/" + str(playlist_num)
        self.driver.get(target)

    def refresh(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()

    def get_music_info(self):
        if self.driver.find_elements_by_xpath("//section[@data-page='notfound']"):
            raise my_exception.KuvoPageNotFoundException()

        #スペースは「.」と扱われるので注意 ("row on" -> "row.on")
        row_on = self.driver.find_elements_by_class_name("row.on")

        if row_on:
            title = row_on[0].find_element_by_class_name("title")
            artist = row_on[0].find_element_by_class_name("artist")
            return title.text, artist.text
        else:
            # 「row on」がないときがたまにある。多分リストの最後に居座ってる
            row_off = self.driver.find_elements_by_class_name("row.off")
            print(row_off)
            if row_off:
                title = row_off[-1].find_element_by_class_name("title")
                artist = row_off[-1].find_element_by_class_name("artist")
                return title.text, artist.text
            else:
                raise my_exception.TrackInfoNotFoundException("トラック情報を取得できませんでした")



