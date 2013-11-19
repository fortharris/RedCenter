from PyQt4 import QtCore, QtGui

class ProgressWidget(QtGui.QLabel):
    
    stopThread = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
                
        self.setFixedSize(400, 555)
        self.setStyleSheet("background: rgba(0, 0, 0, 50)")
        
        whiteSpace = QtGui.QLabel(self)
        whiteSpace.setGeometry(0, 0, 400, 60)
        whiteSpace.setStyleSheet("background: rgb(255, 255, 255)")
        
        self.currentItemLabel = QtGui.QLabel(whiteSpace)
        self.currentItemLabel.setGeometry(10, 18, 380, 20)
        
        self.progressBar = QtGui.QProgressBar(whiteSpace)
        self.progressBar.setGeometry(10, 40, 380, 15)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        
        self.currentItem = ''

        cancelButtonStyle = """ 
            QPushButton {
                        width: 75;
                        height: 25;
                        color: white;
                        background: #343434;
                        border-radius: 0px;
                        border: 1px solid lightgrey;
                    }

            QPushButton:hover {
                        color: white;
                        border: 1px soild #66C1FF;
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
                                
                        """
        self.stopThreadButton = QtGui.QPushButton("Cancel", self)
        self.stopThreadButton.setGeometry(165, 70, 80, 30)
        self.stopThreadButton.setStyleSheet(cancelButtonStyle)
        self.stopThreadButton.clicked.connect(self.stopThread.emit)
        self.stopThreadButton.clicked.connect(self.indicateStop)
        
    def showCurrentJobText(self, text):
        self.currentItemLabel.setText(text)

    def indicateStop(self):
        self.currentItemLabel.setText("Canceling...")
        
    def updateProgress(self, value):
        self.progressBar.setValue(value)
