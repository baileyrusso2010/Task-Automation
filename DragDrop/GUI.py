from re import S
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BSoup
import pandas as pd

class Action():

    def __init__(self):
        self.driver = None
        self.arr = []
        self.url = "http://its/staff/ic/transportation.aspx"

    def OpenBrowser(self):
        s=Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)
        self.driver.maximize_window()

    def OpenURl(self):
        try:
            self.driver.get(self.url)
        except:
            print("this is not working")

    def CloseBrowser(self):
        self.driver.close()

    def ReadData(self):
        self.driver.find_element(By.ID, 'LBextractd2').click()

        bs_obj = BSoup(self.driver.page_source, 'html.parser')
        table = bs_obj.find("table", {"id" : "DGmain"})
        table_body = table.find('tbody')

        value_list = []
        rows = table_body.find_all('tr')

        count = 1
        for row in rows[0:]:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            value_list.append([ele for ele in cols]) # Get rid of empty values

            count += 1

        df = pd.DataFrame(value_list)
        df.to_csv("something.csv", encoding='utf-8', index=False)

if __name__ == "__main__":
    ac = Action()
    ac.OpenBrowser()
    ac.OpenURl()
    ac.ReadData()
    ac.CloseBrowser()