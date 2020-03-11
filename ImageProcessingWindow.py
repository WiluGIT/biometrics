import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QLabel, QColorDialog, QApplication
from PyQt5.QtGui import QPixmap, QImage, QColor, QPalette, QPainter

class Ui_ImageProcessingWindow(object):
    clicked_pixel_x = None
    clicked_pixel_y = None
    def setupUi(self, ImageProcessingWindow):
        ImageProcessingWindow.setObjectName("ImageProcessingWindow")
        ImageProcessingWindow.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(ImageProcessingWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(0, 0, 100, 80))
        self.photo.setAlignment(QtCore.Qt.AlignCenter)
        self.photo.setText("")
        pixmap = QtGui.QPixmap("img/kontrolny3.tiff")
        base_pixmap = pixmap.scaled(100, 80)
        self.photo.setPixmap(base_pixmap)
        #self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 620, 800, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(0, 640, 113, 32))
        self.loadButton.setObjectName("loadButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(0, 680, 113, 32))
        self.saveButton.setObjectName("saveButton")
        self.pathLabel = QtWidgets.QLabel(self.centralwidget)
        self.pathLabel.setGeometry(QtCore.QRect(10, 730, 780, 16))
        self.pathLabel.setObjectName("pathLabel")
        self.sizeBox = QtWidgets.QComboBox(self.centralwidget)
        self.sizeBox.setGeometry(QtCore.QRect(145, 682, 104, 26))
        self.sizeBox.setObjectName("sizeBox")
        self.sizeBox.addItem("")
        self.sizeBox.addItem("")
        self.sizeBox.addItem("")
        self.sizeBox.addItem("")
        self.resizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.resizeLabel.setGeometry(QtCore.QRect(150, 650, 71, 16))
        self.resizeLabel.setObjectName("resizeLabel")
        self.pixelLabel = QtWidgets.QLabel(self.centralwidget)
        self.pixelLabel.setGeometry(QtCore.QRect(290, 650, 91, 16))
        self.pixelLabel.setObjectName("pixelLabel")
        self.pixelPhoto = QtWidgets.QLabel(self.centralwidget)
        self.pixelPhoto.setGeometry(QtCore.QRect(290, 670, 80, 60))
        self.pixelPhoto.setObjectName("pixelPhoto")
        self.pickerButton = QtWidgets.QPushButton(self.centralwidget)
        self.pickerButton.setGeometry(QtCore.QRect(410, 680, 113, 32))
        self.pickerButton.setObjectName("pickerButton")
        self.pixelValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.pixelValueLabel.setGeometry(QtCore.QRect(420, 650, 91, 16))
        self.pixelValueLabel.setObjectName("pixelValueLabel")
        self.valueButton = QtWidgets.QPushButton(self.centralwidget)
        self.valueButton.setGeometry(QtCore.QRect(550, 680, 113, 32))
        self.valueButton.setObjectName("valueButton")
        ImageProcessingWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ImageProcessingWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        ImageProcessingWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ImageProcessingWindow)
        self.statusbar.setObjectName("statusbar")
        ImageProcessingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ImageProcessingWindow)
        QtCore.QMetaObject.connectSlotsByName(ImageProcessingWindow)

        # init size
        self.size_combo_box()
        # click events
        self.loadButton.clicked.connect(self.open_dialog_box)
        self.sizeBox.currentIndexChanged.connect(self.size_combo_box)
        self.photo.mousePressEvent = self.get_pixel_position
        self.pickerButton.clicked.connect(self.show_color_dialog)
        self.valueButton.clicked.connect(self.save_pixel_value)
        self.saveButton.clicked.connect(self.save_dialog_box)

    def retranslateUi(self, ImageProcessingWindow):
        _translate = QtCore.QCoreApplication.translate
        ImageProcessingWindow.setWindowTitle(_translate("ImageProcessingWindow", "Image Processing"))
        self.loadButton.setText(_translate("ImageProcessingWindow", "Choose File"))
        self.saveButton.setText(_translate("ImageProcessingWindow", "Save File"))
        self.pathLabel.setText(_translate("ImageProcessingWindow", "img/kontrolny3.tiff"))
        self.sizeBox.setItemText(0, _translate("ImageProcessingWindow", "1x"))
        self.sizeBox.setItemText(1, _translate("ImageProcessingWindow", "2x"))
        self.sizeBox.setItemText(2, _translate("ImageProcessingWindow", "4x"))
        self.sizeBox.setItemText(3, _translate("ImageProcessingWindow", "8x"))
        self.resizeLabel.setText(_translate("ImageProcessingWindow", "Select size:"))
        self.pixelLabel.setText(_translate("ImageProcessingWindow", "Selected pixel:"))
        self.pixelValueLabel.setText(_translate("ImageProcessingWindow", "Pixel Value:"))
        self.valueButton.setText(_translate("ImageProcessingWindow", "Save Value"))
        self.pickerButton.setText(_translate("ImageProcessingWindow", "Choose Color"))

    def save_pixel_value(self):
        if self.clicked_pixel_y != None and self.clicked_pixel_x != None:
            rgb = self.pixelPhoto.palette().color(QPalette.Background)
            print("In Save X position: {}, Y position: {}".format(self.clicked_pixel_x, self.clicked_pixel_y))
            pixmap = self.photo.pixmap()
            img = pixmap.toImage()
            img.setPixelColor(int(self.clicked_pixel_x), int(self.clicked_pixel_y), rgb)
            pix_final = QtGui.QPixmap.fromImage(img)
            self.photo.setPixmap(pix_final)
            ImageProcessingWindow.hide()
            ImageProcessingWindow.show()

    def show_color_dialog(self):
        selected_color = QColorDialog.getColor()
        if selected_color.isValid():
            self.pixelPhoto.setStyleSheet("QLabel { background-color: %s}" % selected_color.name())

    def open_dialog_box(self):
        filter = "AllFiles (*.jpg *jpeg *.gif *.png *.bmp *.tiff *tif);;JPEG (*.jpg *jpeg);;GIF (*.gif);;PNG(*.png);;BMP (*.bmp);; TIF (*.tiff *.tif)"
        file = QFileDialog.getOpenFileName(filter=filter)
        filepath = file[0]
        pixmap = QPixmap(filepath)
        self.photo.setPixmap(pixmap)
        self.pathLabel.setText(filepath)
        self.size_combo_box()

    def save_dialog_box(self):

        filter = "JPG (*.jpg);;JPEG (*jpeg);;GIF (*.gif);;PNG(*.png);;BMP (*.bmp);; TIF (*.tif);; TIFF(*.tiff)"
        filename = QFileDialog.getSaveFileName(caption = "Save Image", directory = os.curdir, filter=filter)
        print(filename)
        pixmap = self.photo.pixmap()
        result = pixmap.save(filename[0])
        print(result)


    def size_combo_box(self):
        index = int(self.sizeBox.currentIndex())
        #pixmap = QtGui.QPixmap(self.pathLabel.text())
        pixmap = self.photo.pixmap()
        if index == 0:
            smaller_pixmap = pixmap.scaled(100, 80)
            self.photo.setGeometry(QtCore.QRect(0, 0, 100, 80))
            self.photo.setPixmap(smaller_pixmap)

        elif index == 1:
            smaller_pixmap = pixmap.scaled(200, 160)
            self.photo.setGeometry(QtCore.QRect(0, 0, 200, 160))
            self.photo.setPixmap(smaller_pixmap)
        elif index == 2:
            smaller_pixmap = pixmap.scaled(400, 320)
            self.photo.setGeometry(QtCore.QRect(0, 0, 400, 320))
            self.photo.setPixmap(smaller_pixmap)
        elif index == 3:
            smaller_pixmap = pixmap.scaled(800, 620)
            self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
            self.photo.setPixmap(smaller_pixmap)

        # if index == 0:
        #     self.photo.setGeometry(QtCore.QRect(0, 0, 100, 80))
        # elif index == 1:
        #     self.photo.setGeometry(QtCore.QRect(0, 0, 200, 160))
        #
        # elif index == 2:
        #     self.photo.setGeometry(QtCore.QRect(0, 0, 400, 320))
        #
        # elif index == 3:
        #     self.photo.setGeometry(QtCore.QRect(0, 0, 800, 640))
    def get_pixel_position(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.clicked_pixel_x = x
        self.clicked_pixel_y = y
        print("X position: {}, Y position: {}".format(self.clicked_pixel_x, self.clicked_pixel_y))
        pixmap = self.photo.pixmap()
        img = pixmap.toImage()
        c = img.pixel(x, y)
        selected_color = QColor(c)
        self.pixelPhoto.setStyleSheet("QLabel { background-color: %s}" % selected_color.name())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImageProcessingWindow = QtWidgets.QMainWindow()
    ui = Ui_ImageProcessingWindow()
    ui.setupUi(ImageProcessingWindow)
    ImageProcessingWindow.show()
    sys.exit(app.exec_())
