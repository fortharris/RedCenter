import os
import win32api
import win32con
from PyQt4 import QtCore, QtGui

from Extensions.Global import sizeformat
from Extensions.Global import updateLogFile


class DeleteThread(QtCore.QThread):

    currentJobChanged = QtCore.pyqtSignal(str)
    deleteSizeChanged = QtCore.pyqtSignal(int)

    def run(self):
        self.failedDeleteList = []
        self.successDeleteList = []
        self.deleteSize = 0
        for i in self.deleteKeyList:
            if self.stopThread == False:
                attrib = self.logDict[i].split('|')
                self.currentJobChanged.emit("Deleting: " + attrib[0])

                fpath = os.path.join("Vault\\Files\\", i)

                fileSize = int(attrib[3])
                try:
                    win32api.SetFileAttributes(
                        fpath, win32con.FILE_ATTRIBUTE_NORMAL)
                    os.remove(fpath)

                    self.deleteSize += fileSize

                    # append index in list for easy removal
                    self.successDeleteList.append(self.vaultKeyList.index(i))

                    del self.logDict[i]
                    self.vaultKeyList.remove(i)

                    value = len(self.successDeleteList) * 100 / len(
                        self.deleteKeyList)
                    self.deleteSizeChanged.emit(value)
                except:
                    self.failedDeleteList.append(i)
            else:
                break
        updateLogFile(self.logDict)

    def beginDelete(self, deleteKeyList, logDict, vaultKeyList):
        self.vaultKeyList = vaultKeyList
        self.logDict = logDict
        self.deleteKeyList = deleteKeyList
        self.stopThread = False

        self.start()

    def stopJob(self):
        self.stopThread = True


class Delete(QtGui.QWidget):

    def __init__(self, busyIndicatorWidget, vaultListWidget, parent):
        QtGui.QWidget.__init__(self, parent)

        self.busyIndicatorWidget = busyIndicatorWidget
        self.vaultManager = vaultListWidget
        self.redCenter = parent

        self.deleteThread = DeleteThread()
        self.deleteThread.deleteSizeChanged.connect(self.updateDeleteProgress)
        self.deleteThread.finished.connect(self.deleteFinished)
        self.deleteThread.currentJobChanged.connect(self.printCurrentJob)

        self.busyIndicatorWidget.stopThread.connect(self.deleteThread.stopJob)

    def printCurrentJob(self, job):
        self.busyIndicatorWidget.showCurrentJobText(job)

    def loadDeleteList(self):
        self.deleteKeyList = []
        for i in self.vaultManager.selected:
            index = self.vaultManager.row(i)
            self.deleteKeyList.append(self.vaultManager.vaultKeyList[index])

    def delete(self):
        self.redCenter.showBusy("vault")
        self.deleteThread.beginDelete(self.deleteKeyList,
                                     self.vaultManager.logDict,
                                     self.vaultManager.vaultKeyList)

    def retryDelete(self):
        self.deleteKeyList = []
        self.deleteKeyList.extend(self.deleteThread.failedDeleteList)
        self.delete()

    def deleteErrorMess(self):
        self.redCenter.messageStack.setCurrentIndex(5)
        self.redCenter.messageStack.show()

    def deleteFinished(self):
        self.redCenter.showReady("vault")
        # display size of remaining files
        new_size = self.vaultManager.vaultContentsSize - \
            self.deleteThread.deleteSize
        self.redCenter.sizeLabel.setText(sizeformat(new_size))
        self.vaultManager.vaultContentsSize = new_size
        self.updateVaultListWidget_deleteList()
        if len(self.deleteThread.failedDeleteList) > 0:
            self.deleteErrorMess()
        else:
            self.redCenter.sound("deleted")

    def updateVaultListWidget_deleteList(self):
        for i in self.deleteThread.successDeleteList:
            self.vaultManager.takeItem(i)
        self.vaultManager.showVaultEmptyLabel()
        self.vaultManager.vaultItemCountLabel.setText(
            "Items: " + str(self.vaultManager.count()))

    def updateDeleteProgress(self, value):
        self.busyIndicatorWidget.updateProgress(value)
