from PyQt4 import QtCore, QtGui


class FrameLabel(QtGui.QLabel):

    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)

        self.setGeometry(0, 0, 496, 25)

        nameLabel = QtGui.QLabel("RedCenter - Standard Edition", self)
        nameLabel.setStyleSheet("color: white;")
        nameLabel.setGeometry(5, 0, 300, 25)

        self._parent = parent

        minimizeButton = QtGui.QPushButton(self)
        minimizeButton.setToolTip("Minimize")
        minimizeButton.setGeometry(431, 0, 30, 17)
        minimizeButton.setIcon(QtGui.QIcon("Icons\\minimize"))
        minimizeButton.clicked.connect(self._parent.showMinimized)

        minimizeButton.setStyleSheet(""" QPushButton {
                        width: 75;
                        height: 25;
                        background: #2c80ff;
                        border-radius: 0px;
                        border: none;
                    }

            QPushButton:hover {
                        color: white;
                        border: 1px solid #2c80ff;
                    }

            QPushButton:pressed {
                        background: #2c80ff;
                        border: none;
                        padding-top: 2px;
                        }
            """)

        closeButton = QtGui.QPushButton(self)
        closeButton.setToolTip("Close")
        closeButton.setGeometry(461, 0, 30, 17)
        closeButton.setIcon(QtGui.QIcon("Icons\\tray"))
        closeButton.clicked.connect(self._parent.close)

        closeButton.setStyleSheet(""" QPushButton {
                        width: 75;
                        height: 25;
                        background: #ea3c3c;
                        border-radius: 0px;
                        border: none;
                    }

            QPushButton:hover {
                        border: 1px solid #ea3c3c;
                    }

            QPushButton:pressed {
                        background: #ea3c3c;
                        border: none;
                        padding-top: 2px;
                        }
            """)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - \
                                                self._parent.frameGeometry(
                                                ).topLeft()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self._parent.move(event.globalPos() - self.dragPosition)
            event.accept()
        else:
            event.ignore()
