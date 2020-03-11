from PyQt5 import QtCore, QtGui, QtWidgets
from ImageProcessingWindow import Ui_ImageProcessingWindow

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(60, 30, 691, 43))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.informationLabel = QtWidgets.QLabel(self.centralwidget)
        self.informationLabel.setGeometry(QtCore.QRect(200, 100, 367, 22))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.informationLabel.setFont(font)
        self.informationLabel.setObjectName("informationLabel")
        self.instructionLabel = QtWidgets.QLabel(self.centralwidget)
        self.instructionLabel.setGeometry(QtCore.QRect(250, 160, 261, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.instructionLabel.setFont(font)
        self.instructionLabel.setObjectName("instructionLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuPrograms = QtWidgets.QMenu(self.menubar)
        self.menuPrograms.setObjectName("menuPrograms")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action1_Processing_Images = QtWidgets.QAction(MainWindow)
        self.action1_Processing_Images.setObjectName("action1_Processing_Images")
        self.menuPrograms.addAction(self.action1_Processing_Images)
        self.menubar.addAction(self.menuPrograms.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # click event to manu actions
        self.action1_Processing_Images.triggered.connect(self.load_image_processing_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Biometrics by KW"))
        self.titleLabel.setText(_translate("MainWindow", "👁BIOMETRICS BY KONRAD WILCZEK👁"))
        self.informationLabel.setText(_translate("MainWindow", "Select program which you want too use from:"))
        self.instructionLabel.setText(_translate("MainWindow", "MENU -> Programs -> *Program name*"))
        self.menuPrograms.setTitle(_translate("MainWindow", "Programs"))
        self.action1_Processing_Images.setText(_translate("MainWindow", "1. Processing Images"))
        self.action1_Processing_Images.setStatusTip(_translate("MainWindow", "ZAD 1 IMAGE PROCESSING"))

    def load_image_processing_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ImageProcessingWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        # only for testing
        MainWindow.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
