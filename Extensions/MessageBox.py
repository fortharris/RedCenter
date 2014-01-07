from PyQt4 import QtGui

style = """
            QLabel {
            background: rgba(0, 0, 0, 230);
            border-radius: 0px;
            border-top: 1px solid red;
            }

            QPushButton {
                        font: Ms Reference Sans Serif;
                        color: white;
                        background: rgba(0, 0, 0, 230);
                        border-radius: 0px;
                        border: 1px solid lightgrey;
                    }

            QPushButton:hover {
                        color: white;
                        border: 1px soild #66C1FF;
                        background: rgba(0, 0, 0, 230);
                        border: 1px solid #0098FF;
                    }

            QPushButton:pressed {
                        color: black;
                        background: #0098FF;
                        }

            QPushButton:checked{
                        border-color: #000033;
                        }

            QPushButton:disabled{
                        border-color: #000033;
                        }


        """


class ReplyBox(QtGui.QLabel):

    def __init__(self, caption, parent=None):
        QtGui.QLabel.__init__(self, parent)

        self.setStyleSheet(style)

        vbox = QtGui.QVBoxLayout()

        hbox = QtGui.QHBoxLayout()

        iconLabel = QtGui.QLabel()
        iconLabel.setStyleSheet("border: none; background: none;")
        iconLabel.setScaledContents(True)
        iconLabel.setMaximumWidth(35)
        iconLabel.setMinimumWidth(35)
        iconLabel.setMaximumHeight(35)
        iconLabel.setPixmap(QtGui.QPixmap("Icons\\alert"))
        hbox.addWidget(iconLabel)

        self.messageLabel = QtGui.QLabel(caption)
        self.messageLabel.setStyleSheet(
            "color: white; background: none; border: none;")
        hbox.addWidget(self.messageLabel)

        vbox.addLayout(hbox)

        vbox.addStretch(1)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)

        self.retryButton = QtGui.QPushButton("Retry")
        self.retryButton.clicked.connect(parent.hide)
        hbox.addWidget(self.retryButton)

        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelButton.clicked.connect(parent.hide)
        hbox.addWidget(self.cancelButton)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class MessageBox(QtGui.QLabel):

    def __init__(self, caption, parent=None):
        QtGui.QLabel.__init__(self, parent)

        self.setStyleSheet(style)

        vbox = QtGui.QVBoxLayout()

        hbox = QtGui.QHBoxLayout()

        iconLabel = QtGui.QLabel()
        iconLabel.setStyleSheet("border: none; background: none;")
        iconLabel.setScaledContents(True)
        iconLabel.setMaximumWidth(35)
        iconLabel.setMinimumWidth(35)
        iconLabel.setMaximumHeight(35)
        iconLabel.setPixmap(QtGui.QPixmap("Icons\\alert"))
        hbox.addWidget(iconLabel)

        self.messageLabel = QtGui.QLabel(caption)
        self.messageLabel.setStyleSheet(
            "color: white; background: none; border: none;")
        hbox.addWidget(self.messageLabel)

        vbox.addLayout(hbox)

        vbox.addStretch(1)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)

        self.acceptButton = QtGui.QPushButton("Yes")
        self.acceptButton.clicked.connect(parent.hide)
        hbox.addWidget(self.acceptButton)

        self.rejectButton = QtGui.QPushButton("No")
        self.rejectButton.clicked.connect(parent.hide)
        hbox.addWidget(self.rejectButton)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
