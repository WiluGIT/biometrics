import os
import matplotlib.pyplot as plt
import numpy
from PIL import Image
import numpy as np
from PIL.ImageQt import ImageQt

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QBuffer, QIODevice
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QLabel, QColorDialog, QApplication, QMessageBox
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
        # version with quality lose
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
        self.pickerButton.setGeometry(QtCore.QRect(410, 670, 113, 32))
        self.pickerButton.setObjectName("pickerButton")
        self.pixelValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.pixelValueLabel.setGeometry(QtCore.QRect(420, 650, 91, 16))
        self.pixelValueLabel.setObjectName("pixelValueLabel")
        self.valueButton = QtWidgets.QPushButton(self.centralwidget)
        self.valueButton.setGeometry(QtCore.QRect(410, 700, 113, 32))
        self.valueButton.setObjectName("valueButton")
        self.histogramButton = QtWidgets.QPushButton(self.centralwidget)
        self.histogramButton.setGeometry(QtCore.QRect(530,640,113,32))
        self.histogramButton.setObjectName("histogramButton")
        self.brightenButton= QtWidgets.QPushButton(self.centralwidget)
        self.brightenButton.setGeometry(QtCore.QRect(530, 700, 113,32))
        self.brightenButton.setObjectName("brightenButton")
        self.darkenButton = QtWidgets.QPushButton(self.centralwidget)
        self.darkenButton.setGeometry(QtCore.QRect(530,670,113,32))
        self.darkenButton.setObjectName("darkenButton")
        self.rangeValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.rangeValueLabel.setGeometry(QtCore.QRect(650, 630, 91, 16))
        self.rangeValueLabel.setObjectName("rangeValueLabel")
        self.aRangeValue = QtWidgets.QLineEdit(self.centralwidget)
        self.aRangeValue.setGeometry(QtCore.QRect(660, 650, 30, 16))
        self.aRangeValue.setObjectName("aRangeValue")
        self.bRangeValue = QtWidgets.QLineEdit(self.centralwidget)
        self.bRangeValue.setGeometry(QtCore.QRect(710, 650, 30, 16))
        self.bRangeValue.setObjectName("bRangeValue")
        self.stretchButton = QtWidgets.QPushButton(self.centralwidget)
        self.stretchButton.setGeometry(QtCore.QRect(650, 670, 135, 32))
        self.stretchButton.setObjectName("stretchButton")
        self.equalizationButton = QtWidgets.QPushButton(self.centralwidget)
        self.equalizationButton.setGeometry(QtCore.QRect(650, 700, 135, 32))
        self.equalizationButton.setObjectName("equalizationButton")
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
        self.histogramButton.clicked.connect(self.create_histogram)
        self.brightenButton.clicked.connect(self.brighten_img)
        self.darkenButton.clicked.connect(self.darken_img)
        self.stretchButton.clicked.connect(self.stretch_histogram)
        self.equalizationButton.clicked.connect(self.equalize_histogram)
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
        self.histogramButton.setText(_translate("ImageProcessingWindow", "Plot histogram"))
        self.brightenButton.setText(_translate("ImageProcessingWindow", "Brighten Image"))
        self.darkenButton.setText(_translate("ImageProcessingWindow", "Darken Image"))
        self.rangeValueLabel.setText(_translate("ImageProcessingWindow", "Range a to b"))
        self.stretchButton.setText(_translate("ImageProcessingWindow", "Stretch histogram"))
        self.equalizationButton.setText(_translate("ImageProcessingWindow", "Equalize histogram"))

        self.aRangeValue.setText("0")
        self.bRangeValue.setText("255")
        my_regex = QtCore.QRegExp("([0-9]|[1-8][0-9]|9[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])")
        my_validator = QtGui.QRegExpValidator(my_regex, self.aRangeValue)
        self.aRangeValue.setValidator(my_validator)
        my_validator = QtGui.QRegExpValidator(my_regex, self.bRangeValue)
        self.bRangeValue.setValidator(my_validator)

    def equ_lut(self, dist):
        result = []
        k_size = 256
        for i in range(k_size):
            val = (dist[i] - dist[0] / 1 - dist[0]) * (k_size - 1)
            result.append(val)

        return result

    def equalize_histogram(self):
        try:
            # cumulative distribution
            img = Image.open(self.pathLabel.text(), "r")
            img = img.convert("RGB")
            pix_val = list(img.getdata())

            # check whether image is rgb or grayscale
            coloured = self.check_coloured(pix_val)

            if not coloured:
                gray = []
                for i in range(len(pix_val)):
                    gray.append(pix_val[i][0])
                px = self.count_pixels_histogram(gray)

                dist = []
                val = 0
                for j in range(len(px)):
                    val += px[j] / len(pix_val)
                    dist.append(val)

                gray_lut = self.equ_lut(dist)

                new_grey = []
                for j in range(len(gray)):
                    new_val = int(gray_lut[gray[j]])
                    new_grey.append(new_val)

                result_img = []
                for i in range(len(new_grey)):
                    tup = (new_grey[i], new_grey[i], new_grey[i])
                    result_img.append(tup)

                image = Image.new('RGB', img.size)
                image.putdata(result_img)

                image.save("Histogram_img/equalized.png")
                print("Saved image.")

                pix = QtGui.QPixmap("Histogram_img/equalized.png")
                self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
                scaled_pixmap = pix.scaled(800, 620)
                self.photo.setPixmap(scaled_pixmap)
                self.sizeBox.setCurrentIndex(3)
                self.sizeBox.hide()
                self.sizeBox.show()
                self.photo.hide()
                self.photo.show()

                g_px = self.count_pixels_histogram(new_grey)
                plt.bar(list(g_px.keys()), g_px.values(), color='gray')
                plt.title('GREYSCALE', size=16, y=1.1)
                plt.tight_layout()
                plt.show()
            else:
                r = []
                g = []
                b = []
                for i in range(len(pix_val)):
                    r.append(pix_val[i][0])
                    g.append(pix_val[i][1])
                    b.append(pix_val[i][2])

                rpx = self.count_pixels_histogram(r)
                gpx = self.count_pixels_histogram(g)
                bpx = self.count_pixels_histogram(b)

                dist_r = []
                dist_g = []
                dist_b = []
                val_r = 0
                val_g = 0
                val_b = 0
                for j in range(len(rpx)):
                    val_r += rpx[j] / len(pix_val)
                    val_g += gpx[j] / len(pix_val)
                    val_b += bpx[j] / len(pix_val)

                    dist_r.append(val_r)
                    dist_g.append(val_g)
                    dist_b.append(val_b)

                red_lut = self.equ_lut(dist_r)
                green_lut = self.equ_lut(dist_g)
                blue_lut = self.equ_lut(dist_b)

                new_red = []
                new_green = []
                new_blue = []
                for j in range(len(r)):
                    new_val_r = int(red_lut[r[j]])
                    new_val_g = int(green_lut[g[j]])
                    new_val_b = int(blue_lut[b[j]])

                    new_red.append(new_val_r)
                    new_green.append(new_val_g)
                    new_blue.append(new_val_b)

                result_img = []
                for i in range(len(new_red)):
                    tup = (new_red[i], new_green[i], new_blue[i])
                    result_img.append(tup)

                image = Image.new('RGB', img.size)
                image.putdata(result_img)

                image.save("Histogram_img/equalized.png")
                print("Saved image.")

                pix = QtGui.QPixmap("Histogram_img/equalized.png")
                self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
                scaled_pixmap = pix.scaled(800, 620)
                self.photo.setPixmap(scaled_pixmap)
                self.sizeBox.setCurrentIndex(3)
                self.sizeBox.hide()
                self.sizeBox.show()
                self.photo.hide()
                self.photo.show()

                r_px = self.count_pixels_histogram(new_red)
                g_px = self.count_pixels_histogram(new_green)
                b_px = self.count_pixels_histogram(new_blue)
                plt.subplot(3, 1, 1)
                plt.title('RED EQUALIZED', size=16, y=1.12)
                plt.bar(list(r_px.keys()), r_px.values(), color='r')

                plt.subplot(3, 1, 2)
                plt.title('GREEN EQUALIZED', size=16, y=1.12)
                plt.bar(list(g_px.keys()), g_px.values(), color='g')

                plt.subplot(3, 1, 3)
                plt.title('BLUE EQUALIZED', size=16, y=1.12)
                plt.bar(list(b_px.keys()), b_px.values(), color='b')

                plt.tight_layout()
                plt.show()
        except AttributeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Select image to create histogram")
            msg.setWindowTitle("Warning!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msg.exec_()


    def stretch_histogram(self):

        try:
            img = Image.open(self.pathLabel.text(), "r")
            img = img.convert("RGB")

            pix_val = list(img.getdata())

            r = []
            g = []
            b = []
            for i in range(len(pix_val)):
                r.append(pix_val[i][0])
                g.append(pix_val[i][1])
                b.append(pix_val[i][2])

            r_lut = self.calc_lut(r)
            g_lut = self.calc_lut(g)
            b_lut = self.calc_lut(b)

            result = []
            for i in range(len(r_lut)):
                tup = (r_lut[i], g_lut[i], b_lut[i])
                result.append(tup)

            image = Image.new('RGB', img.size)
            image.putdata(result)

            image.save("Histogram_img/strached.png")
            print("Saved image.")
            pix = QtGui.QPixmap("Histogram_img/strached.png")
            self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
            scaled_pixmap = pix.scaled(800, 620)
            self.photo.setPixmap(scaled_pixmap)
            self.sizeBox.setCurrentIndex(3)
            self.sizeBox.hide()
            self.sizeBox.show()
            self.photo.hide()
            self.photo.show()

            coloured = self.check_coloured(pix_val)

            if not coloured:
                gray = []
                for i in range(len(result)):
                    gray.append(result[i][0])
                px = self.count_pixels_histogram_without_zeros(gray)
                px[0] = 0
                px[255] = 0
                plt.bar(list(px.keys()), px.values(), color='gray')
                plt.title('GREYSCALE STRACHED', size=16, y=1.1)
                plt.tight_layout()
                plt.show()
            else:
                r = self.count_pixels_histogram_without_zeros(r_lut)
                r[0] = 0
                r[255] = 0

                plt.subplot(3, 1, 1)
                plt.title('RED STRACHED', size=16, y=1.12)
                plt.bar(list(r.keys()), r.values(), color='r')

                g = self.count_pixels_histogram_without_zeros(g_lut)
                g[0] = 0
                g[255] = 0
                plt.subplot(3, 1, 2)
                plt.title('GREEN STRACHED', size=16, y=1.12)
                plt.bar(list(g.keys()), g.values(), color='g')

                b = self.count_pixels_histogram_without_zeros(b_lut)
                b[0] = 0
                b[255] = 0
                plt.subplot(3, 1, 3)
                plt.title('BLUE STRACHED', size=16, y=1.12)
                plt.bar(list(b.keys()), b.values(), color='b')

                plt.tight_layout()
                plt.show()
        except AttributeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Select image to create histogram")
            msg.setWindowTitle("Warning!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msg.exec_()


    def calc_lut(self, array):
        a_range = int(self.aRangeValue.text())
        b_range = int(self.bRangeValue.text())
        result = []
        for i in range(len(array)):
            if array[i] < a_range:
                newVal = int(((a_range - a_range) / (b_range - a_range)) * 255)
            elif array[i] > b_range:
                newVal = int(((b_range - a_range) / (b_range - a_range)) * 255)
            else:
                newVal = int(((array[i] - a_range) / (b_range - a_range)) * 255)
            result.append(newVal)

        return result

    def brighten_img(self):
        try:
            img = Image.open(self.pathLabel.text(), "r")
            img = img.convert("RGB")
            c = 255 / (np.log(1 + np.max(img)))
            pix_val = list(img.getdata())

            transformed_pic = []
            for i in range(len(pix_val)):
                elems = []
                for j in range(len(pix_val[i])):
                    new_pix = int(c * np.log(1 + pix_val[i][j]))
                    elems.append(new_pix)
                tup = (elems[0], elems[1], elems[2])
                transformed_pic.append(tup)

            print("transofmed {}".format(len(transformed_pic)))
            image = Image.new('RGB', img.size)
            image.putdata(transformed_pic)

            image.save("Histogram_img/brightened.png")
            print("Saved image.")

            pix = QtGui.QPixmap("Histogram_img/brightened.png")
            self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
            scaled_pixmap = pix.scaled(800, 620)
            self.photo.setPixmap(scaled_pixmap)
            self.sizeBox.setCurrentIndex(3)
            self.sizeBox.hide()
            self.sizeBox.show()
            self.photo.hide()
            self.photo.show()
        except AttributeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Select image to create histogram")
            msg.setWindowTitle("Warning!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msg.exec_()


    def darken_img(self):
        try:
            img = Image.open(self.pathLabel.text(), "r")
            img = img.convert("RGB")
            c = 255 / (np.log(1 + np.max(img)))
            pix_val = list(img.getdata())

            transformed_pic = []
            for i in range(len(pix_val)):
                elems = []
                for j in range(len(pix_val[i])):
                    new_pix = int(c * pow(pix_val[i][j], 0.1))
                    elems.append(new_pix)
                tup = (elems[0], elems[1], elems[2])
                transformed_pic.append(tup)

            image = Image.new('RGB', img.size)
            image.putdata(transformed_pic)

            image.save("Histogram_img/darkened.png")
            print("Saved image.")

            pix = QtGui.QPixmap("Histogram_img/darkened.png")
            self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
            scaled_pixmap = pix.scaled(800, 620)
            self.photo.setPixmap(scaled_pixmap)
            self.sizeBox.setCurrentIndex(3)
            self.sizeBox.hide()
            self.sizeBox.show()
            self.photo.hide()
            self.photo.show()
        except AttributeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Select image to create histogram")
            msg.setWindowTitle("Warning!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msg.exec_()





    def create_histogram(self):
        try:
            image = Image.open(self.pathLabel.text(), "r")
            image = image.convert("RGB")
            pix_val = list(image.getdata())
            # check whether image is rgb or grayscale
            coloured = self.check_coloured(pix_val)

            if not coloured:
                gray = []
                for i in range(len(pix_val)):
                    gray.append(pix_val[i][0])
                px = self.count_pixels_histogram(gray)
                plt.bar(list(px.keys()), px.values(), color='gray')
                plt.title('GREYSCALE', size=16, y=1.1)
                plt.tight_layout()
                plt.show()

            else:
                r = []
                g = []
                b = []
                for i in range(len(pix_val)):
                    r.append(pix_val[i][0])
                    g.append(pix_val[i][1])
                    b.append(pix_val[i][2])

                r = self.count_pixels_histogram(r)
                plt.subplot(3, 1, 1)
                plt.title('RED', size=16, y=1.12)
                plt.bar(list(r.keys()), r.values(), color='r')

                g = self.count_pixels_histogram(g)
                plt.subplot(3, 1, 2)
                plt.title('GREEN', size=16, y=1.12)
                plt.bar(list(g.keys()), g.values(), color='g')

                b = self.count_pixels_histogram(b)
                plt.subplot(3, 1, 3)
                plt.title('BLUE', size=16, y=1.12)
                plt.bar(list(b.keys()), b.values(), color='b')

                plt.tight_layout()
                plt.show()

                avaraged = self.avaraged_histogram(r, g, b)
                plt.title('AVARAGED (R + G +B) / 3', size=16, y=1.12)
                plt.bar(list(avaraged.keys()), avaraged.values(), color='b')
                plt.tight_layout()
                plt.show()



                # METHOD WITH BUILT IN FUNCTION
                # region
                # r2, g2, b2 = image.split()
                # dic = {}
                # dic2 = {}
                # dic3= {}
                # for i in range(len(r2.histogram())):
                #     el = r2.histogram()[i]
                #     dic[i] = el
                # for i in range(len(g2.histogram())):
                #     el = g2.histogram()[i]
                #     dic2[i] = el
                # for i in range(len(b2.histogram())):
                #     el = b2.histogram()[i]
                #     dic3[i] = el
                # plt.subplot(3, 1, 1)
                # plt.bar(list(dic.keys()), dic.values(), color='y')
                # plt.subplot(3, 1, 2)
                # plt.bar(list(dic2.keys()), dic2.values(), color='y')
                # plt.subplot(3, 1, 3)
                # plt.bar(list(dic3.keys()), dic3.values(), color='y')
                # plt.show()
                # endregion
        except AttributeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Select image to create histogram")
            msg.setWindowTitle("Warning!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msg.exec_()

    def check_coloured(self, pix_tuple):
        counter = 0
        for i in range(len(pix_tuple)):
            if pix_tuple[i][0] == pix_tuple[i][1] == pix_tuple[i][2]:
                counter += 1

        if counter == len(pix_tuple):
            return False

        return True

    def count_pixels_histogram(self, seq):
        hist = dict([(x, 0) for x in range(256)])
        for i in seq:
            hist[i] = hist.get(i, 0) + 1
        return hist

    def count_pixels_histogram_without_zeros(self, seq):
        hist = {}
        for i in seq:
            hist[i] = hist.get(i, 0) + 1
        sort_dic = {}
        for j in sorted(hist):
            sort_dic.update({j: hist[j]})
        return sort_dic

    def avaraged_histogram(self, r, g, b):
        hist = dict([(x, 0) for x in range(256)])
        for i in range(len(r)):
            hist[i] = (r[i] + g[i] + b[i]) / 3
        return hist


    def save_pixel_value(self):
        if self.clicked_pixel_y != None and self.clicked_pixel_x != None:
            rgb = self.pixelPhoto.palette().color(QPalette.Background)
            print("In Save X position: {}, Y position: {}".format(self.clicked_pixel_x, self.clicked_pixel_y))
            pixmap = self.photo.pixmap()
            img = pixmap.toImage()
            img.setPixelColor(int(self.clicked_pixel_x), int(self.clicked_pixel_y), rgb)
            pix_final = QtGui.QPixmap.fromImage(img)
            self.photo.setPixmap(pix_final)
            self.photo.hide()
            self.photo.show()
            # ImageProcessingWindow.hide()
            # ImageProcessingWindow.show()

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
        pixmap = self.photo.pixmap()
        result = pixmap.save(filename[0])



    def size_combo_box(self):
        index = int(self.sizeBox.currentIndex())
        # version with quality lose

        # pixmap = QtGui.QPixmap(self.pathLabel.text())
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


        # version without quality lose
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
