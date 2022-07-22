from abc import abstractmethod
import sys
from PyQt5 import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from abc import ABC, abstractmethod
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
        self.url = "http://its/staff/ic/sportsschedule2.aspx"

    def OpenBrowser(self):
        s=Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s)
        print("hello world")
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

class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget,self).__init__()

        self.myListWidget1 = QListWidget()
        self.myListWidget2 = QListWidget()

        #self.myListWidget2.setViewMode(QListWidget.IconMode)
        self.myListWidget1.setAcceptDrops(False)
        self.myListWidget1.setDragEnabled(True)

        self.myListWidget2.setAcceptDrops(True)
        self.myListWidget2.setDragEnabled(True)

        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.addWidget(self.myListWidget1)
        self.hboxlayout.addWidget(self.myListWidget2)

        act = Action()

        one = QListWidgetItem(QIcon("./img/Web.png"), "Open Browser")
        two = QListWidgetItem(QIcon("./img/WebClick.png"), "Open URL")
        
        data = act.OpenBrowser

        one.setData(Qt.UserRole, data)
        two.setData(QtCore.Qt.UserRole, "Russo")

        self.myListWidget1.insertItem(1,one)
        self.myListWidget1.insertItem(2,two)
        one.data(Qt.UserRole)
        
        self.setLayout(self.hboxlayout)
        self.runActions()

    def runActions(self):
        self.myListWidget1.item(0).data(QtCore.Qt.UserRole)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    m=MainWidget()
    m.show()
    sys.exit(app.exec_())