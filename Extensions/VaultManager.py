import os
from PyQt4 import QtCore, QtGui

from Extensions.Global import sizeformat

class SearchWidget(QtGui.QLabel):
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)
        
        self._parent = parent
        
        self.setStyleSheet("""background: rgba(0, 0, 0, 50); border-radius: 0px;""")
        self.setFixedSize(300, 28)
        self.setPixmap(QtGui.QPixmap("Icons\\line"))
        self.setScaledContents(True)
        
        self.searchTimer = QtCore.QTimer()
        self.searchTimer.setSingleShot(True)
        self.searchTimer.setInterval(200)
        self.searchTimer.timeout.connect(self.gotoText)
        
        self.textFindLine = QtGui.QLineEdit(self)
        self.textFindLine.setStyleSheet("background: white; border-radius: 0px;")
        self.textFindLine.setGeometry(3, 2, 270, 23)
        self.textFindLine.grabKeyboard()
        self.textFindLine.setTextMargins(2, 1, 22, 1)
        self.textFindLine.textChanged.connect(self.show)
        self.textFindLine.textChanged.connect(self.searchTimer.start)
        
        self.clearTextFindLineButton = QtGui.QPushButton(self.textFindLine)
        self.clearTextFindLineButton.setGeometry(250, 2, 15, 15)
        self.clearTextFindLineButton.setFlat(True)
        self.clearTextFindLineButton.setIcon(QtGui.QIcon("Icons\\clearLeft"))
        self.clearTextFindLineButton.setStyleSheet("background: white; border: none;")
        self.clearTextFindLineButton.clicked.connect(self.textFindLine.clear)
        
        self.finderCloseButton = QtGui.QToolButton(self)
        self.finderCloseButton.setStyleSheet("background: none;")
        self.finderCloseButton.setGeometry(278, 6, 15, 15)
        self.finderCloseButton.setAutoRaise(True)
        self.finderCloseButton.setIconSize(QtCore.QSize(25, 25))
        self.finderCloseButton.setIcon(QtGui.QIcon("Icons\\Cross"))
        self.finderCloseButton.clicked.connect(self.hide)
        
    def gotoText(self):
        text = self.textFindLine.text()
        self._parent.gotoText(text)

class VaultManager(QtGui.QListWidget):
    def __init__(self, vaultItemCountLabel, sizeLabel, busyIndicatorWidget, parent):
        QtGui.QListWidget.__init__(self, parent)
        
        self.redCenter = parent
        
        self.setLayoutMode(1)
        self.setBatchSize(1)
        self.setUniformItemSizes(True)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setAlternatingRowColors(True)
        self.setIconSize(QtCore.QSize(30, 30))
        self.itemSelectionChanged.connect(self.selectionMade)
        
        searchWidget = SearchWidget(self)
        searchWidget.move(80, 0)
        searchWidget.hide()
        
        self.vaultItemCountLabel = vaultItemCountLabel
        self.sizeLabel = sizeLabel
        self.busyIndicatorWidget = busyIndicatorWidget
        
        self.vaultZeroContentLabel = QtGui.QLabel("Empty", self)
        self.vaultZeroContentLabel.setGeometry(150, 20, 100, 50)
        self.vaultZeroContentLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vaultZeroContentLabel.setStyleSheet("background: none; font: 20px; color: lightgrey;")
        self.vaultZeroContentLabel.hide()
        
        self.vaultCleanUp()
        
    def gotoText(self, text):
        for i in self.vaultKeyList:
            if self.logDict[i].split('|')[0].startswith(text):
                index = self.vaultKeyList.index(i)
                self.setCurrentRow(index)
                break

    def loadVault(self):
        try:
            logList = []
            self.vaultKeyList = []
            file = open("Vault\\LOG","r")
            for i in file.readlines():
                if i.strip() == '':
                    pass
                else:
                    logList.append(tuple(i.strip().split('||')))
            file.close()
            self.logDict = dict(logList)

            self.vaultContentsSize = 0

            self.clear()
            size = QtCore.QSize()
            size.setHeight(40)
            for key, property in self.logDict.items():
                self.vaultKeyList.append(key)
                ## extract attributes
                attrib = self.logDict[key].split('|')

                # get locking time
                time_split = key.split('=')[0].split('-')
                date = QtCore.QDate(int(time_split[0]), int(time_split[1]), 
                                            int(time_split[3])).toString()
                
                item = QtGui.QListWidgetItem(attrib[0])
                item.setToolTip('Original Location: ' + attrib[2] + '\nModified: ' + date)
                item.setSizeHint(size)
                # assign icon
                if attrib[1] == "exec":
                    item.setIcon(QtGui.QIcon("Icons\\executable"))
                else:
                    item.setIcon(QtGui.QIcon("Icons\\unknown"))
                self.addItem(item)
                
                self.vaultContentsSize += int(attrib[3])
            self.vaultItemCountLabel.setText("Items: " + str(len(self.logDict)))
            # display size of total files
            self.sizeLabel.setText(sizeformat(self.vaultContentsSize))
            self.showVaultEmptyLabel()
        except:
            self.redCenter.showMessage("Problem loading items in the vault.")
        self.redCenter.hideMessage()
        
    def showVaultEmptyLabel(self):
        if self.count() > 0:
            self.vaultZeroContentLabel.hide()
        else:
            self.vaultZeroContentLabel.show()
            
    def selectionMade(self):
        self.selected = self.selectedItems()
        if len(self.selected) > 0:
            self.redCenter.unlockButton.setEnabled(True)
            self.redCenter.deleteButton.setEnabled(True)
        else:
            self.redCenter.unlockButton.setEnabled(False)
            self.redCenter.deleteButton.setEnabled(False)
            
    def vaultCleanUp(self):
        logList = []
        file = open("Vault\\LOG","r")
        for i in file.readlines():
            if i.strip() == '':
                pass
            else:
                logList.append(tuple(i.strip().split('||')))
        file.close()
        logDict = dict(logList)
        
        filesList = os.listdir("Vault\\Files")
        bookedFilesList = []
        for i, v in logDict.items():
            bookedFilesList.append(i)
        for i in filesList:
            if i not in bookedFilesList:
                path = os.path.join("Vault\\Files", i)
                try:
                    os.remove(path)
                except:
                    pass