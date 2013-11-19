import os
import win32api, win32con, win32file
from PyQt4 import QtCore, QtGui

from Extensions.Global import sizeformat

lightFont = QtGui.QFont()
lightFont.setWeight(0)

class FileItemWidget(QtGui.QWidget):
    def __init__(self, filePath, isDir, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.filePath = filePath
        self.isDir = isDir
        
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.setMargin(1)
        self.setLayout(mainLayout)

        iconLabel = QtGui.QLabel()
        iconLabel.setScaledContents(True)
        iconLabel.setMaximumWidth(30)
        iconLabel.setMinimumWidth(30)
        iconLabel.setMaximumHeight(30)
        mainLayout.addWidget(iconLabel)

        vbox = QtGui.QVBoxLayout()
        
        self.fileName = os.path.basename(self.filePath)
        
        nameLabel = QtGui.QLabel()
        nameLabel.setAlignment(QtCore.Qt.AlignVCenter)
        nameLabel.setWordWrap(True)
        nameLabel.setText(self.fileName)
        nameLabel.setMinimumWidth(250)
        nameLabel.setMaximumWidth(250)
        vbox.addWidget(nameLabel)
        mainLayout.addLayout(vbox)
        
        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(0)
        mainLayout.addLayout(vbox)

        hbox_1 = QtGui.QHBoxLayout()
        vbox.addLayout(hbox_1)
        
        sizeLabel = QtGui.QLabel()
        sizeLabel.setFont(lightFont)
        sizeLabel.setAlignment(QtCore.Qt.AlignRight)
        hbox_1.addWidget(sizeLabel)

        sizeValueLabel = QtGui.QLabel()
        sizeValueLabel.setMaximumWidth(50)
        sizeValueLabel.setMinimumWidth(50)
        sizeValueLabel.setAlignment(QtCore.Qt.AlignRight)
        hbox_1.addWidget(sizeValueLabel)

        
        vbox.addStretch(1)

        hbox_2 = QtGui.QHBoxLayout()
        hbox_2.addStretch(1)
        vbox.addLayout(hbox_2)
        
        execIconLabel = QtGui.QLabel()
        hbox_2.addWidget(execIconLabel)
        
        hiddenIconLabel = QtGui.QLabel()
        hbox_2.addWidget(hiddenIconLabel)
        
        # check if item is a file or folder
        fileInfo = QtCore.QFileInfo(self.filePath)
        # assign icon
        if self.isDir:
            iconLabel.setPixmap(QtGui.QPixmap("Icons\\folder"))
        else:
            self.isExe = fileInfo.isExecutable()
            if self.isExe:
                icon = QtGui.QFileIconProvider()
                fileIcon = icon.icon(fileInfo)
                icon = QtGui.QIcon(fileIcon)
                pixmap = icon.pixmap(40, 40)
                iconLabel.setPixmap(pixmap)

                execIconLabel.setPixmap(QtGui.QPixmap("Icons\\red"))
            else:
                iconLabel.setPixmap(QtGui.QPixmap("Icons\\unknown"))
        try:
            self.isHidden = fileInfo.isHidden()
            if self.isHidden:
                hiddenIconLabel.setPixmap(QtGui.QPixmap("Icons\\orange"))
            else:
                hiddenIconLabel.hide()
        except:
            pass
        try:
            if self.isDir:
                try:
                    contents_count = len(os.listdir(self.filePath))
                    sizeValueLabel.setText("<font color='grey'>" + str(contents_count)  + "</font color>")
                except:
                    sizeValueLabel.setText("<font color='grey'>Blocked</font color>")
            else:
                sizeLabel.setText("""<font color="grey">Size:</font color>""")
                # get size
                itemSize = os.path.getsize(self.filePath)
                sizeValueLabel.setText(sizeformat(itemSize))
        except:
            sizeValueLabel.setText("<i>Error</i>")

class FileManager(QtGui.QListWidget):
    def __init__(self, redCenter, busyIndicatorWidget, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        
        self.setLayoutMode(1)
        self.setBatchSize(1)
        self.setUniformItemSizes(True)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setIconSize(QtCore.QSize(20, 20))
        self.itemActivated.connect(self.openDir)
        self.itemSelectionChanged.connect(self.selectionMade)
        
        self.redCenter = redCenter
        self.busyIndicatorWidget = busyIndicatorWidget
        
        self.rootPath = os.path.normpath(QtCore.QDir().rootPath())
        # for folder operations
        self.path_history_list = []
        self.path_history_position = 0
        self.path_history_list.append('')
        
        self.fileSystemWatcher = QtCore.QFileSystemWatcher()
        self.fileSystemWatcher.directoryChanged.connect(self.reload_homeDir)
        
        self.dirZeroContentLabel = QtGui.QLabel("Empty", self)
        self.dirZeroContentLabel.setGeometry(150, 20, 100, 50)
        self.dirZeroContentLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dirZeroContentLabel.setStyleSheet("background: none; font: 20px; color: lightgrey;")
        self.dirZeroContentLabel.hide()
        
    def blockWatcher(self):
        self.fileSystemWatcher.blockSignals(True)
        
    def unBlockWatcher(self):
        self.fileSystemWatcher.blockSignals(False)
                
    def nonExistentPath(self):
        self.redCenter.showMessage("Path no longer exists!\n\nAccess Denied")
            
    def openDir(self):
        widgetItem = self.getItemWidget()
        if widgetItem.isDir:
            path = self.getItemPath()
            self.loadDirectory(path)
        else:
            pass
            
    def prevDir(self):
        path = self.path_history_list[self.path_history_position - 1]
        if os.path.exists(path):
            self.loadDirectory(path)
        else:
            self.nonExistentPath()

    def nextDir(self):
        path = self.path_history_list[self.path_history_position + 1]
        if os.path.exists(path):
            self.loadDirectory(path)
        else:
            self.nonExistentPath()
        
    def goHome(self):
        if os.path.exists(self.path_history_list[0]):
            self.loadDirectory(self.path_history_list[0])
        else:
            self.nonExistentPath()
            self.loadDirectory(self.rootPath)
            
    def unhideItems(self):
        pathList = []
        for i in self.selected:
            index = self.row(i)
            path = self.getItemPath(index)
            pathList.append(path)
        for path in pathList:
            try:
                win32api.SetFileAttributes(path, win32con.FILE_ATTRIBUTE_NORMAL)
            except:
                pass
        self.reload_homeDir()
            
    def setParentDirectory(self):    
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                "Choose Folder", self.getLastOpenedDir(), options)
        if directory:
            d = os.path.normpath(directory)
            self.loadDirectory(d)
            self.saveLastOpenedDir(d)
            
    def reload_homeDir(self):
        if os.path.exists(self.home):
            self.loadDirectory(self.home)
        else:
            self.loadDirectory(self.rootPath)  
            
    def storage_media_handler(self, path):
        self.showNormal()
        if os.path.exists(path):
            self.loadDirectory(path)
            self.redCenter.show()
        else:
            self.reload_homeDir()
        
    def getLastOpenedDir(self):
        if os.path.exists(self.redCenter.SETTINGS["LastOpenedPath"]) == True:
            pass
        else:
            self.redCenter.SETTINGS["LastOpenedPath"] = QtCore.QDir().homePath()
        return self.redCenter.SETTINGS["LastOpenedPath"]
       
    def saveLastOpenedDir(self, path):
        if self.redCenter.SETTINGS["LastOpenedPath"] == path:
            pass
        else:
            self.redCenter.SETTINGS["LastOpenedPath"] = path
            
    def selectionMade(self):
        self.selected = self.selectedItems()
        if len(self.selected) > 0:
            self.redCenter.lockButton.setEnabled(True)
            self.redCenter.unhideButton.setEnabled(True)
        else:
            self.redCenter.lockButton.setEnabled(False)
            self.redCenter.unhideButton.setEnabled(False)
            
    def getItemWidget(self, index=None):
        if index == None:
            index = self.currentRow()
        item = self.item(index)
        widgetItem = self.itemWidget(item)
        
        return widgetItem
            
    def getItemPath(self, index=None):
        if index == None:
            index = self.currentRow()
        item = self.item(index)
        widgetItem = self.itemWidget(item)
        path = widgetItem.filePath
        
        return path
        
    def getItemName(self, index=None):
        if index == None:
            index = self.currentRow()
        item = self.item(index)
        widgetItem = self.itemWidget(item)
        path = widgetItem.fileName
        
        return path
            
    def sortFolderList(self, foldersList):
        hidden = []
        normal = []
        for i in foldersList:
            if i.isHidden:
                hidden.append(i)
            else:
                normal.append(i)
        total = []
        total.extend(hidden)
        total.extend(normal)
        
        return total
        
    def sortFileList(self, filesList):
        hidden = []
        normal = []
        executable = []
        for i in filesList:
            if i.isExe:
                executable.append(i)
                continue
            if i.isHidden:
                hidden.append(i)
            else:
                normal.append(i)
        total = []
        total.extend(executable)
        total.extend(hidden)
        total.extend(normal)
        
        return total
            
    def loadDirectory(self, dirPath):
        try:
            contents = os.listdir(dirPath)
            if len(contents) > 0:
                self.dirZeroContentLabel.hide()
            else:
                self.dirZeroContentLabel.show()
        except Exception as err:
            basename = os.path.basename(dirPath)
            if basename != '':
                self.redCenter.showMessage("Mounting failed: " + basename + '\n\n' + str(err.args[1]))
            else:
                self.redCenter.showMessage("Mounting failed: " + dirPath + '\n\n' + str(err))
            return
        
        # FIXME: Cant seem to be able to remove the drice c:\ path from watch list
        self.fileSystemWatcher.removePaths(self.fileSystemWatcher.directories())
        self.fileSystemWatcher.addPath(dirPath)
        
        self.home = dirPath

        foldersList = []
        filesList = []

        # load lists
        for i in contents:
            fpath = os.path.join(dirPath, i)
            fileInfo = QtCore.QFileInfo(fpath)
            isDir = fileInfo.isDir()
            if isDir:
                fileItemWidget = FileItemWidget(fpath, True)
                foldersList.append(fileItemWidget)
            else:
                fileItemWidget = FileItemWidget(fpath, False)
                filesList.append(fileItemWidget)
                
        sortedFolderList = self.sortFolderList(foldersList)
        sortedFileList = self.sortFileList(filesList)
        total = []
        total.extend(sortedFolderList)
        total.extend(sortedFileList)
        
        size = QtCore.QSize()
        size.setHeight(40)
        
        self.clear()
        for fileItemWidget in total:
            item = QtGui.QListWidgetItem()
            item.setSizeHint(size)
            self.addItem(item)
            self.setItemWidget(item, fileItemWidget)
            
        self.redCenter.homeDirPathLabel.setText(self.home)
        self.redCenter.homeDirPathLabel.setToolTip(self.home)
        
        # show number of items incide current directory
        self.redCenter.homeDirCountLabel.setText("Items: " + str(len(self)))
        # show name of current directory
        self.redCenter.homeDirNameLabel.setText(os.path.split(self.home)[1])

        # get drive type
        try:
            driveName = os.path.splitdrive(self.home)[0] + '\\'
            driveType = win32file.GetDriveType(driveName)
            if driveType == 0:
                # Unknown
                icon = "Icons\\driveIcons\\unknown"
            elif driveType == 1:
                # No Root Directory
                icon = "Icons\\driveIcons\\noRoot"
            elif driveType == 2:
                # Removable Disk
                icon = "Icons\\driveIcons\\removable"
            elif driveType == 3:
                # Local Disk
                icon = "Icons\\driveIcons\\localDrive"
            elif driveType == 4:
                # Network Drive
                icon = "Icons\\driveIcons\\networkDrive"
            elif driveType == 5:
                # Compact Disc
                icon = "Icons\\driveIcons\\compactDisk"
            elif driveType == 6:
                # RAM Disk
                icon = "Icons\\driveIcons\\ramDisk"
        except:
            icon = "Icons\\driveIcons\\unknown"
        self.redCenter.driveIconLabel.setPixmap(QtGui.QPixmap(icon))
        
        # prepare path_history_list for navigation
        find = 0
        for i in self.path_history_list:
            if self.home == i:
                # meaning user visited a previously visited path
                find = 1
                break
        if find == 1:
            pass
        else:
            split_path = os.path.split(self.home)
            if split_path[0] == self.path_history_list[-1]:
                # meaning user just visited subdirectory
                self.path_history_list.append(self.home)
            else:
                # meaning there has been a diversion in the path
                for i in self.path_history_list:
                    if split_path[0] == i:
                        path_index = self.path_history_list.index(i)
                        find = 1
                        for w in range(len(self.path_history_list) - path_index - 1):
                            del self.path_history_list[path_index + 1]
                        self.path_history_list.append(self.home)
                        break
                if find == 1:
                    pass
                else:
                    # user has opened a completely different path
                    # meaning root is different
                    self.path_history_list = []
                    self.path_history_list.append(self.home)
        self.path_history_position = self.path_history_list.index(self.home)
        if self.path_history_position == 0:
            self.redCenter.prevButton.setDisabled(True)
        else:
            self.redCenter.prevButton.setDisabled(False)
        if (len(self.path_history_list) - 1) == self.path_history_position:
            self.redCenter.nextButton.setDisabled(True)
        else:
            self.redCenter.nextButton.setDisabled(False)
        self.redCenter.hideMessage()
