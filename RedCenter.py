import sys
from PyQt4 import QtCore, QtGui

from Extensions.FileManager import FileManager
from Extensions.VaultManager import VaultManager
from Extensions.SingleInstance import SingleInstance
from Extensions.FrameLabel import FrameLabel
from Extensions.DriveManager import DriveManager
from Extensions.Notification import Notification
from Extensions.Lock import Lock
from Extensions.Delete import Delete
from Extensions.Unlock import Unlock
from Extensions.AboutLabel import AboutLabel
from Extensions.ProgressWidget import ProgressWidget
import Extensions.MessageBox as MessageBox


class RedCenter(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent, QtCore.Qt.Window |
                                  QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint |
                                  QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.setWindowIcon(QtGui.QIcon("Icons\\Icon.png"))
        self.setFixedSize(492, 515)
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())
                  / 2, (screen.height() - size.height()) / 2)
        self.setWindowTitle('RedCenter - Standard Edition')

        mainBackgroundLabel = QtGui.QLabel(self)
        mainBackgroundLabel.setStyleSheet(
            "background: rgba(0, 0, 0, 220); border: 1px solid grey; border-radius: 0px;")
        mainBackgroundLabel.setScaledContents(True)
        mainBackgroundLabel.setGeometry(0, 0, 492, 515)

        frame = FrameLabel(self)

        self.createTrayIcon()

        self.mainWidget = QtGui.QWidget(self)
        self.mainWidget.setGeometry(5, 25, 492, 555)

        # load configuration from file
        tempList = []
        file = open("settings.ini", "r")
        for i in file.readlines():
            if i.strip() == '':
                pass
            else:
                tempList.append(tuple(i.strip().split('=')))
        file.close()
        self.SETTINGS = dict(tempList)

        # *************************** Main Interface *************************

        separator = QtGui.QFrame(self.mainWidget)
        separator.setFrameShape(separator.HLine)
        separator.setFrameShadow(separator.Raised)
        separator.setGeometry(0, 0, 488, 1)

        self.homeDirPathLabel = QtGui.QLabel(self.mainWidget)
        self.homeDirPathLabel.setStyleSheet("color: white;")
        self.homeDirPathLabel.setGeometry(5, 2, 470, 15)

        self.homeDirCountLabel = QtGui.QLabel(self.mainWidget)
        self.homeDirCountLabel.setStyleSheet("color: white;")
        self.homeDirCountLabel.setGeometry(0, 470, 90, 15)

        self.homeDirNameLabel = QtGui.QLabel(self.mainWidget)
        self.homeDirNameLabel.setStyleSheet("color: white;")
        self.homeDirNameLabel.setGeometry(110, 470, 370, 15)

        self.driveIconLabel = QtGui.QLabel(self.mainWidget)
        self.driveIconLabel.setGeometry(403, 150, 80, 80)
        self.driveIconLabel.setScaledContents(True)

        self.prevButton = QtGui.QPushButton(self.mainWidget)
        self.prevButton.setGeometry(405, 48, 38, 25)
        self.prevButton.setIcon(QtGui.QIcon("Icons\\Previous"))
        self.prevButton.setToolTip("Previous")
        self.prevButton.setDisabled(True)
        self.prevButton.clicked.connect(self.prevItem)

        self.nextButton = QtGui.QPushButton(self.mainWidget)
        self.nextButton.setGeometry(444, 48, 36, 25)
        self.nextButton.setIcon(QtGui.QIcon("Icons\\Next"))
        self.nextButton.setToolTip("Next")
        self.nextButton.setDisabled(True)
        self.nextButton.clicked.connect(self.nextItem)

        self.lockButton = QtGui.QPushButton("Lock", self.mainWidget)
        self.lockButton.setGeometry(405, 255, 75, 25)
        self.lockButton.setDisabled(True)
        self.lockButton.clicked.connect(self.lockItem_init)

        self.unhideButton = QtGui.QPushButton("Unhide", self.mainWidget)
        self.unhideButton.setGeometry(405, 285, 75, 25)
        self.unhideButton.setDisabled(True)
        self.unhideButton.clicked.connect(self.unhideItems)

        separator = QtGui.QFrame(self.mainWidget)
        separator.setFrameShape(separator.VLine)
        separator.setFrameShadow(separator.Raised)
        separator.setGeometry(100, 470, 1, 15)

        self.browseButton = QtGui.QPushButton("Browse", self.mainWidget)
        self.browseButton.setGeometry(405, 20, 75, 25)
        self.browseButton.clicked.connect(self.selectPath)

        self.backShortcut = QtGui.QShortcut(self.prevButton)
        self.backShortcut.setKey(QtGui.QKeySequence("Backspace"))
        self.backShortcut.activated.connect(self.prevItem)

        self.backShortcut_2 = QtGui.QShortcut(self.prevButton)
        self.backShortcut_2.setKey(QtGui.QKeySequence("Alt+Left"))
        self.backShortcut_2.activated.connect(self.prevItem)

        self.nextShortcut = QtGui.QShortcut(self.nextButton)
        self.nextShortcut.setKey(QtGui.QKeySequence("Alt+Right"))
        self.nextShortcut.activated.connect(self.nextItem)

        self.homeButton = QtGui.QPushButton("Home", self.mainWidget)
        self.homeButton.setGeometry(405, 76, 75, 25)
        self.homeButton.clicked.connect(self.goHome)

        self.vaultButton = QtGui.QPushButton("Vault", self.mainWidget)
        self.vaultButton.setGeometry(405, 350, 75, 25)
        self.vaultButton.setCheckable(True)
        self.vaultButton.clicked.connect(self.changeView)

        self.aboutButton = QtGui.QPushButton("About", self.mainWidget)
        self.aboutButton.setGeometry(405, 410, 75, 25)
        self.aboutButton.setCheckable(True)
        self.aboutButton.toggled.connect(self.about)

        self.closeButton = QtGui.QPushButton("Close", self.mainWidget)
        self.closeButton.setGeometry(405, 440, 75, 25)
        self.closeButton.clicked.connect(self.close)

    #************************* Vault Interface Elements ***********************

        self.vaultNameLabel = QtGui.QLabel("Vault", self.mainWidget)
        self.vaultNameLabel.setGeometry(5, 2, 533, 15)
        self.vaultNameLabel.setStyleSheet("color: white;")
        self.vaultNameLabel.hide()

        self.vaultItemCountLabel = QtGui.QLabel(self.mainWidget)
        self.vaultItemCountLabel.setGeometry(0, 470, 90, 15)
        self.vaultItemCountLabel.setStyleSheet("color: white;")
        self.vaultItemCountLabel.hide()

        self.selectAllButton = QtGui.QPushButton("Select All", self.mainWidget)
        self.selectAllButton.setGeometry(405, 20, 75, 25)
        self.selectAllButton.clicked.connect(self.selectAll)
        self.selectAllButton.hide()

        self.clearSelectionButton = QtGui.QPushButton(
            "Deselect All", self.mainWidget)
        self.clearSelectionButton.setGeometry(405, 50, 75, 25)
        self.clearSelectionButton.clicked.connect(self.clearSelection)
        self.clearSelectionButton.hide()

        self.vaultIconLabel = QtGui.QLabel(self.mainWidget)
        self.vaultIconLabel.setGeometry(403, 150, 80, 80)
        self.vaultIconLabel.setScaledContents(True)
        self.vaultIconLabel.setPixmap(
            QtGui.QPixmap("Icons\\driveIcons\\security"))
        self.vaultIconLabel.hide()

        self.deleteButton = QtGui.QPushButton("Delete", self.mainWidget)
        self.deleteButton.setGeometry(405, 255, 75, 25)
        self.deleteButton.clicked.connect(self.delete)
        self.deleteButton.setDisabled(True)
        self.deleteButton.hide()

        self.unlockButton = QtGui.QPushButton("Unlock", self.mainWidget)
        self.unlockButton.setGeometry(405, 285, 75, 25)
        self.unlockButton.clicked.connect(self.unlockItem_init)
        self.unlockButton.setDisabled(True)
        self.unlockButton.hide()

        self.sizeLabel = QtGui.QLabel(self.mainWidget)
        self.sizeLabel.setGeometry(110, 470, 430, 15)
        self.sizeLabel.setStyleSheet("color: white;")
        self.sizeLabel.hide()

        self.pagesStack = QtGui.QStackedWidget(self.mainWidget)
        self.pagesStack.setGeometry(0, 20, 400, 445)

        self.notification = Notification(self.mainWidget)
        self.notification.setGeometry(0, 410, 400, 50)
        self.notification.hide()

        self.busyIndicatorWidget = ProgressWidget(self.mainWidget)
        self.busyIndicatorWidget.move(0, 20)
        self.busyIndicatorWidget.hide()

        #---------------------------------------------------------------------

        self.fileManager = FileManager(self, self.busyIndicatorWidget)
        self.pagesStack.addWidget(self.fileManager)

        self.vaultListWidget = VaultManager(self.vaultItemCountLabel,
                                           self.sizeLabel, self.busyIndicatorWidget, self)
        self.pagesStack.addWidget(self.vaultListWidget)

        self.itemLock = Lock(self.busyIndicatorWidget,
                            self.fileManager, self)
        self.itemUnlock = Unlock(self.busyIndicatorWidget,
                                self.vaultListWidget,
                                                    self.fileManager, self)
        self.itemDelete = Delete(self.busyIndicatorWidget,
                                self.vaultListWidget, self)
        #--------------------------------------------------------------------
        self.aboutLabel = AboutLabel()
        self.pagesStack.addWidget(self.aboutLabel)
        #---------------------------------------------------------------------
        self.messageStack = QtGui.QStackedWidget(self.mainWidget)
        self.messageStack.setGeometry(0, 20, 400, 80)

        lockMessage = MessageBox.MessageBox(
            "Send the selected files to vault?",
            self.messageStack)
        lockMessage.acceptButton.clicked.connect(self.itemLock.lock)
        self.messageStack.addWidget(lockMessage)

        unlockMessage = MessageBox.MessageBox(
            "Restore the selected files to a specified location?",
            self.messageStack)
        unlockMessage.acceptButton.clicked.connect(self.itemUnlock.unlock)
        self.messageStack.addWidget(unlockMessage)

        deleteMessage = MessageBox.MessageBox(
            "Permanently remove the selected files from the vault?",
            self.messageStack)
        deleteMessage.acceptButton.clicked.connect(self.itemDelete.delete)
        self.messageStack.addWidget(deleteMessage)

        lockReplyMessage = MessageBox.ReplyBox("Failed to complete lock!",
                                              self.messageStack)
        lockReplyMessage.retryButton.clicked.connect(self.itemLock.retryLock)
        self.messageStack.addWidget(lockReplyMessage)

        unlockReplyMessage = MessageBox.ReplyBox(
            "Failed to complete unlock! \nFile will not be unlocked if it already exists.",
            self.messageStack)
        unlockReplyMessage.retryButton.clicked.connect(
            self.itemUnlock.retryUnlock)
        self.messageStack.addWidget(unlockReplyMessage)

        deleteReplyMessage = MessageBox.ReplyBox("Failed to complete delete!",
                                                self.messageStack)
        deleteReplyMessage.retryButton.clicked.connect(
            self.itemDelete.retryDelete)
        self.messageStack.addWidget(deleteReplyMessage)

        self.messageStack.hide()

    def showMessage(self, mess):
        self.notification.showMessage(mess)

    def hideMessage(self):
        self.notification.hide()

    def saveSettings(self):
        file = open("settings.ini", "w")
        for key, value in self.SETTINGS.items():
            file.write('\n' + key + '=' + value)
        file.close()

    def createTrayIcon(self):
        self.restoreAction = QtGui.QAction(QtGui.QIcon("Icons\\restore.png"),
                                          "Show", self, triggered=self.showNormal)

        self.hideAction = QtGui.QAction("Hide", self, triggered=self.hide)

        self.closeAction = QtGui.QAction(QtGui.QIcon("Icons\\close.png"),
                                        "Exit", self, triggered=self.shutdown)

        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addAction(self.hideAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.closeAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon("Icons\\Icon.png"))
        self.trayIcon.setToolTip("RedCenter - Standard Edition")
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)

        self.trayIcon.show()

    def closeEvent(self, event):
        self.hide()
        if self.SETTINGS['NotificationClicked'] == "False":
            self.trayIcon.showMessage("RedCenter - Standard Edition",
                                     "Program is still running in the background. Disable this notification by clicking on this balloon.", 1)
        else:
            pass
        event.ignore()

    def reload_homeDir(self):
        self.fileManager.reload_homeDir()

    def selectPath(self):
        self.fileManager.setParentDirectory()

    def prevItem(self):
        self.fileManager.prevDir()

    def nextItem(self):
        self.fileManager.nextDir()

    def goHome(self):
        self.fileManager.goHome()

    def unhideItems(self):
        self.fileManager.unhideItems()

    def delete(self):
        self.itemDelete.loadDeleteList()
        self.messageStack.setCurrentIndex(2)
        self.messageStack.show()

    def loadDirectory(self, directory):
        self.fileManager.loadDirectory(directory)

    def selectAll(self):
        self.vaultListWidget.selectAll()

    def clearSelection(self):
        self.vaultListWidget.clearSelection()

    def lockItem_init(self):
        self.itemLock.loadLockList()
        self.messageStack.setCurrentIndex(0)
        self.messageStack.show()

    def unlockItem_init(self):
        self.itemUnlock.loadUnlockList()
        self.messageStack.setCurrentIndex(1)
        self.messageStack.show()

    def messageClicked(self):
        self.SETTINGS['NotificationClicked'] = 'True'
        self.saveSettings()

    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger,
                     QtGui.QSystemTrayIcon.DoubleClick):
            self.setHidden(False)
        else:
            pass

    def about(self, show):
        if show:
            self.currentWidget = self.pagesStack.currentWidget()
            self.vaultButton.setDisabled(True)
            self.pagesStack.setCurrentWidget(self.aboutLabel)
        else:
            self.pagesStack.setCurrentWidget(self.currentWidget)
            self.vaultButton.setDisabled(False)

    def sound(self, soundType):
        if soundType == "open":
            sound = QtGui.QSound("Sounds\\Open.wav")
        elif soundType == "deleted":
            sound = QtGui.QSound("Sounds\\Trash Empty.wav")
        sound.play()

    def shutdown(self):
        self.saveSettings()
        sys.exit(0)

    def showBusy(self, view):
        self.busyIndicatorWidget.show()
        if view == "directory":
            self.browseButton.setDisabled(True)
            self.prevButton.setDisabled(True)
            self.nextButton.setDisabled(True)
            self.homeButton.setDisabled(True)
            self.lockButton.setDisabled(True)
            self.unhideButton.setDisabled(True)
            self.vaultButton.setDisabled(True)
            self.aboutButton.setDisabled(True)
        elif view == "vault":
            self.selectAllButton.setDisabled(True)
            self.clearSelectionButton.setDisabled(True)
            self.deleteButton.setDisabled(True)
            self.unlockButton.setDisabled(True)
            self.vaultButton.setDisabled(True)
            self.aboutButton.setDisabled(True)

    def showReady(self, view):
        self.busyIndicatorWidget.hide()
        self.busyIndicatorWidget.currentItemLabel.clear()
        self.busyIndicatorWidget.updateProgress(0)
        if view == "directory":
            self.setHidden(False)
            self.browseButton.setDisabled(False)
            self.homeButton.setDisabled(False)
            self.lockButton.setDisabled(False)
            self.unhideButton.setDisabled(False)
            self.vaultButton.setDisabled(False)
            self.aboutButton.setDisabled(False)
        elif view == "vault":
            self.setHidden(False)
            self.selectAllButton.setDisabled(False)
            self.clearSelectionButton.setDisabled(False)
            self.deleteButton.setDisabled(False)
            self.unlockButton.setDisabled(False)
            self.vaultButton.setDisabled(False)
            self.aboutButton.setDisabled(False)

    def changeView(self):
        if self.vaultButton.isChecked() == True:
            # hide directory widgets
            self.homeDirPathLabel.hide()
            self.homeDirCountLabel.hide()
            self.homeDirNameLabel.hide()
            self.browseButton.hide()
            self.prevButton.hide()
            self.nextButton.hide()
            self.homeButton.hide()
            self.driveIconLabel.hide()
            self.lockButton.hide()
            self.unhideButton.hide()

            # show vault widgets
            self.vaultNameLabel.setHidden(False)
            self.pagesStack.setCurrentWidget(self.vaultListWidget)
            self.vaultItemCountLabel.setHidden(False)
            self.selectAllButton.setHidden(False)
            self.clearSelectionButton.setHidden(False)
            self.vaultIconLabel.setHidden(False)
            self.deleteButton.setHidden(False)
            self.unlockButton.setHidden(False)
            self.sizeLabel.setHidden(False)
            self.vaultButton.setText("Back")
            self.vaultListWidget.loadVault()
        else:
            # hide vault widgets
            self.vaultNameLabel.hide()
            self.vaultItemCountLabel.hide()
            self.selectAllButton.hide()
            self.clearSelectionButton.hide()
            self.vaultIconLabel.hide()
            self.deleteButton.hide()
            self.unlockButton.hide()
            self.sizeLabel.hide()

            # show directory widgets
            self.homeDirPathLabel.setHidden(False)
            self.pagesStack.setCurrentWidget(self.fileManager)
            self.homeDirCountLabel.setHidden(False)
            self.homeDirNameLabel.setHidden(False)
            self.browseButton.setHidden(False)
            self.prevButton.setHidden(False)
            self.nextButton.setHidden(False)
            self.homeButton.setHidden(False)
            self.driveIconLabel.setHidden(False)
            self.lockButton.setHidden(False)
            self.unhideButton.setHidden(False)
            self.vaultButton.setText("Vault")

application = SingleInstance()
# check is another instance of same program running
if application.alreadyRunning():
    sys.exit(0)

app = QtGui.QApplication(sys.argv)
style = """
            QPushButton {
                        width: 75;
                        height: 25;
                        color: white;
                        background: #DD0000;
                        border-radius: 0px;
                        border: 1px solid lightgrey;
                    }

            QPushButton:hover {
                        color: white;
                        border: 1px solid #0098FF;
                    }

            QPushButton:pressed {
                        color: black;
                        background: #0098FF;
                        }

            QPushButton:checked{
                        border-color: black;
                        }

            QPushButton:disabled{
                        border-color: black;
                        }

            QListView {
                        color: black;
                        show-decoration-selected: 1; /* make the selection span the entire width of the view */
                       }

            QListView:item {
                        border-bottom: 1px solid #EDEDED;
                        }

            QListView::item:selected:!active {
                        color: black;
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(114, 156, 190, 100), stop: 1 rgba(114, 156, 190, 150));
                        }

            QListView::item:selected:active {
                        color: black;
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(114, 156, 190, 100), stop: 1 rgba(114, 156, 190, 150));
                        }

            QToolTip {
                         color: white;
                         border: none;
                         border-radius: 0px;
                         background: rgb(15, 15, 15);
                         opacity: 200;
                    }

            QProgressBar {
                 text-align: center;
             }

            QScrollBar:vertical{
                padding: 1px;
                border-left-width: 1px;
                border-style:solid;
                border-left-color: transparent;
                background: #ffffff;
                width: 16px;
            }

            QScrollBar:horizontal{
                padding: 1px;
                border-top-width: 1px;
                border-style:solid;
                border-top-color: transparent;
                background: #ffffff;
                height: 16px;
            }

            QScrollBar::handle:vertical{
                padding: 2px;
                min-height: 30px;
                border: 1px solid white;
                border-radius: 0px;
                border-width: 1px;
                background: #B2B8BE;
            }

            QScrollBar::handle:horizontal{
                padding: 2px;
                min-width: 50px;
                background: #B2B8BE;
                border-radius: 0px;
                border-width: 5px;
                border: 1px solid #8A9199;
            }

            QScrollBar::handle:hover{
                background: #6F767D;
            }

            QScrollBar::handle:pressed{
                background: #141414;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical,
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal,
            QScrollBar::add-page:horizontal,

            QScrollBar::sub-page:horizontal{
                background: none;
                border: none;
            }
                    """

app.setStyleSheet(style)

main = RedCenter()
main.loadDirectory(main.fileManager.rootPath)
main.show()

driveDetect = DriveManager()
driveDetect.newDrive.connect(main.fileManager.storage_media_handler)
driveDetect.start()

sys.exit(app.exec_())
