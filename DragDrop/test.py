import sys
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BSoup
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

class Action(ABC):
    @abstractmethod
    def performAction(self):
        pass

class OpenBrowser(Action):

    def performAction(self, driver):
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.maximize_window()
        return driver

class OpenURL(Action):
    def __init__(self, _url):
        self.url = _url

    def performAction(self,driver):
        try:
            return driver.get(self.url)
        except:
            print("this is not working")


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    totalItems = pyqtSignal(int)

    def run(self):
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.maximize_window()
        url = 'http://its/staff/ic/transportation.aspx'
        driver.get(url)
        driver.find_element(By.ID, 'LBextractd2').click()

        bs_obj = BSoup(driver.page_source, 'html.parser')
        table = bs_obj.find("table", {"id" : "DGmain"})
        table_body = table.find('tbody')

        value_list = []
        rows = table_body.find_all('tr')
        self.totalItems.emit(len(table_body))

        count = 1
        for row in rows[0:]:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            value_list.append([ele for ele in cols]) # Get rid of empty values

            count += 1
            self.progress.emit(count + 1)

        df = pd.DataFrame(value_list)
        df.to_csv("something.csv", encoding='utf-8', index=False)
        self.finished.emit()
        driver.close()


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self._createMenuBar()
        self._createActions()
        self._createToolBars()
        self._createStatusBar()

        self.setWindowTitle("Automate Task")
        
        self.resize(400, 200)
        self.centralWidget = QLabel("Hello, World")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

    def _createStatusBar(self):
        self.pbar = QProgressBar(self)
        self.statusBar().showMessage("this is status bar")
        self.statusBar().addPermanentWidget(self.pbar)

    def _createActions(self):
        # File actions
        self.newAction = QAction(self)
        self.newAction.setText("&New")
        self.newAction.setIcon(QIcon("./img/Play.png"))

        #self.newAction.triggered.connect(self.runLongTask)
        self.newAction.triggered.connect(self.runLongTask)

        self.openAction = QAction(QIcon("./img/download.png"), "&Open...", self)
        self.saveAction = QAction(QIcon("./img/download.png"), "&Save", self)
        self.exitAction = QAction("&Exit", self)
        # Edit actions
        self.copyAction = QAction(QIcon("./img/download.png"), "&Copy", self)
        self.pasteAction = QAction(QIcon("./img/download.png"), "&Paste", self)
        self.cutAction = QAction(QIcon("./img/download.png"), "C&ut", self)

    def runTask(self):
        ob = OpenBrowser()
        ou = OpenURL("https://www.yahoo.com/")
        arr = [ob, ou]

        driver = None
        for i in arr:
            driver = i.performAction(driver)
        driver.close()

    def _createToolBars(self):
        # File toolbar
        fileToolBar = self.addToolBar("File")
        fileToolBar.addAction(self.newAction)
        fileToolBar.addAction(self.openAction)
        fileToolBar.addAction(self.saveAction)
        # Edit toolbar
        editToolBar = QToolBar("Edit", self)
        self.addToolBar(editToolBar)
        editToolBar.addAction(self.copyAction)
        editToolBar.addAction(self.pasteAction)
        editToolBar.addAction(self.cutAction)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Using a title
        editMenu = menuBar.addMenu("&Edit")
    
    def reportProgress(self, n):
        self.pbar.setValue(n)

    def maxProgress(self, n):
        self.pbar.setMaximum(n)

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.worker.totalItems.connect(self.maxProgress)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())