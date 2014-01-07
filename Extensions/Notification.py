from PyQt4 import QtCore, QtGui


class Notification(QtGui.QLabel):

    noted = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.setContentsMargins(10, 0, 5, 0)
        self.setLayout(mainLayout)

        self.setMinimumHeight(20)

        self.setStyleSheet("""background: #1A1A1A;
                                color: white;
                                border: none;
                                border-radius: 0px;
                                """)

        iconLabel = QtGui.QLabel()
        iconLabel.setStyleSheet("border: none;")
        iconLabel.setScaledContents(True)
        iconLabel.setMaximumWidth(25)
        iconLabel.setMinimumWidth(25)
        iconLabel.setMaximumHeight(25)
        iconLabel.setPixmap(QtGui.QPixmap("Icons\\widget_noaccess_32px"))
        mainLayout.addWidget(iconLabel)

        self.infoLabel = QtGui.QLabel()
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setStyleSheet("""background: none;
                                        color: white;
                                        border: none;
                                        border-radius: 0px;""")

        mainLayout.addWidget(self.infoLabel)

    def mousePressEvent(self, event):
        self.hide()

    def showMessage(self, mess):
        self.infoLabel.setText(mess)
        self.show()
