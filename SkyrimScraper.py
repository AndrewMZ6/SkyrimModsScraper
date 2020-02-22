# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Myui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import bs4
import requests
import sys



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(80, 460, 91, 41))
        self.StartButton.setObjectName("HotButton")
        self.StartButton.clicked.connect(self.HotMods)

        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setGeometry(300, 15, 300, 15)
        self.progress.setMaximum(100)

        self.PopularButton = QtWidgets.QPushButton(self.centralwidget)
        self.PopularButton.setGeometry(QtCore.QRect(200, 460, 91, 41))
        self.PopularButton.setObjectName("PopularButton")
        self.PopularButton.clicked.connect(self.PopularMods)

        self.NewButton = QtWidgets.QPushButton(self.centralwidget)
        self.NewButton.setGeometry(QtCore.QRect(300, 460, 91, 41))
        self.NewButton.setObjectName("NewButton")
        self.NewButton.clicked.connect(self.NewMods)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(60, 50, 691, 361))
        self.textBrowser.setObjectName("textBrowser")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 20, 91, 20))
        self.label.setObjectName("label")

        self.CloseButton = QtWidgets.QPushButton(self.centralwidget)
        self.CloseButton.setGeometry(QtCore.QRect(640, 480, 91, 61))
        self.CloseButton.setObjectName("CloseButton")
        self.CloseButton.clicked.connect(sys.exit)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def HotMods(self):
        self.textBrowser.setText('')
        url = 'https://www.nexusmods.com/skyrimspecialedition'
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        blockTiles = soup.find('ul', class_='tiles') # Применяю метод find а не findAll, потому что findAll НЕ итерируемый с помощью findAll()
											#  и к тому же нам нужен блок 'ul', т.е. ОДИН блок
        pContent = blockTiles.findAll('p')
        h3Content = blockTiles.findAll('h3')
        k = 0
        self.textBrowser.append('--------------- HOT MODS ----------------'+ '\n')
        for i in range(len(pContent)):
            k += 1
            self.textBrowser.append(str(k) + ' ' + h3Content[i].get_text()+ '  -----  '+ pContent[i].get_text()+ '\n')
            self.progress.setValue((k/len(pContent)*100))
		
    def PopularMods(self):
        self.textBrowser.setText('')
        url = 'https://www.nexusmods.com/skyrimspecialedition?tab=popular+%2830+days%29'

        response = requests.get(url)

        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        divModList = soup.find('div', id='mod-list')

        h3Tags = divModList.findAll('h3')
        pTags = divModList.findAll('p')

        observer = []
        k = 0
        self.textBrowser.append('--------------- POPULAR MODS ----------------'+ '\n')
        for i in range(len(h3Tags)):
            
            if h3Tags[i] in observer:
                k += 1
                self.progress.setValue(int(k/len(h3Tags)*100))
                continue
            else:
                k += 1
                observer.append(h3Tags[i])
                self.textBrowser.append('h3 = '+ h3Tags[i].get_text().strip())
                self.textBrowser.append('p = '+ pTags[i].get_text().strip() + '\n\n')
                self.progress.setValue(int(k/len(h3Tags)*100))


    def NewMods(self):    
        self.textBrowser.setText('')
        url = 'https://www.nexusmods.com/skyrimspecialedition'
        response = requests.get(url)

        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        divModList = soup.find('div', id='mod-list')
        
        h3Tags = divModList.findAll('h3')
        pTags = divModList.findAll('p')
        k = 0
        observer = []
        self.textBrowser.append('--------------- NEW MODS ----------------'+ '\n')
        for i in range(len(h3Tags)):

            if h3Tags[i] in observer:
                k += 1
                self.progress.setValue(int(k/len(h3Tags)*100))
                continue
            else:
                k += 1
                observer.append(h3Tags[i])
                self.textBrowser.append('h3 = '+ h3Tags[i].get_text().strip())
                self.textBrowser.append('p = '+ pTags[i].get_text().strip() + '\n\n')
                self.progress.setValue(int(k/len(h3Tags)*100))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.StartButton.setText(_translate("MainWindow", "HotMods"))
        self.label.setText(_translate("MainWindow", "Вывод текста"))
        self.CloseButton.setText(_translate("MainWindow", "Закрыть"))
        self.PopularButton.setText(_translate("MainWindow", "PopularMods"))
        self.NewButton.setText(_translate("MainWindow", "NewMods"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
