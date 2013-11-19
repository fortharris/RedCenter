from PyQt4 import QtGui

class AboutLabel(QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
                
        self.setStyleSheet("color: white; border-radius: 5px;")
        self.setMargin(20)
        self.setWordWrap(True)
        self.setText("About RedCenter"
                    "<p>RedCenter assists you in identifying potential malwares on drives by providing you with clues."
                    "<p>Note: It does not catch viruses.<br>"
                    "<p><img src='Icons/orange'>______Hidden"
                    "<p><img src='Icons/red'>______Executable"
                    "<p>Version: 1.1"
                    "<p>Author: Amoatey Harrison"
                    "<p>Author Email: fortharris@gmail.com"
                    "<p>Developed with Python using the PyQt interface."
                    )