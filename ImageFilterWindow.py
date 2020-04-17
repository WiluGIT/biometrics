import os
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy
from PIL import Image
import numpy as np
from PIL.ImageQt import ImageQt
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QBuffer, QIODevice
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QLabel, QColorDialog, QApplication, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QImage, QColor, QPalette, QPainter


createdMask = []
mask = ""
class Ui_MaskDialog(object):
    def setupUi(self, MaskDialog):
        MaskDialog.setObjectName("MaskDialog")
        MaskDialog.resize(308, 198)
        self.buttonBox = QtWidgets.QDialogButtonBox(MaskDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 160, 151, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtWidgets.QComboBox(MaskDialog)
        self.comboBox.setGeometry(QtCore.QRect(210, 20, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.textEdit = QtWidgets.QTextEdit(MaskDialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 151, 131))
        self.textEdit.setObjectName("textEdit")
        self.confirmMaskButton = QtWidgets.QPushButton(MaskDialog)
        self.confirmMaskButton.setGeometry(QtCore.QRect(210, 60, 75, 23))
        self.confirmMaskButton.setObjectName("confirmMaskButton")
        self.retranslateUi(MaskDialog)
        self.buttonBox.accepted.connect(MaskDialog.accept)
        self.buttonBox.rejected.connect(MaskDialog.reject)
        self.confirmMaskButton.clicked.connect(self.confirm_mask)
        self.comboBox.currentIndexChanged.connect(self.mask_size_change)
        QtCore.QMetaObject.connectSlotsByName(MaskDialog)

        # init combobox
        self.mask_size_change()
    def retranslateUi(self, MaskDialog):
        _translate = QtCore.QCoreApplication.translate
        MaskDialog.setWindowTitle(_translate("MaskDialog", "Mask"))
        self.comboBox.setItemText(0, _translate("MaskDialog", "3x3"))
        self.comboBox.setItemText(1, _translate("MaskDialog", "5x5"))
        self.comboBox.setItemText(2, _translate("MaskDialog", "7x7"))
        self.confirmMaskButton.setText(_translate("MaskDialog", "Confirm mask"))

    def confirm_mask(self):
        global mask
        mask = ""
        mask = self.textEdit.toPlainText()
        maskArray = mask.split(",")

        mask1d =[]
        for i in range(len(maskArray)):
            mask1d.append(int(maskArray[i].strip('\n')))
        maskLen = len(mask1d)
        global createdMask
        createdMask = []
        element = []
        counter = 0

        if maskLen == 9:
            for i in range(3):
                for j in range(3):
                    element.append(mask1d[counter])
                    counter += 1
                createdMask.append(element)
                element = []
        elif maskLen == 25:
            for i in range(5):
                for j in range(5):
                    element.append(mask1d[counter])
                    counter += 1
                createdMask.append(element)
                element = []
        elif maskLen == 49:
            for i in range(7):
                for j in range(7):
                    element.append(mask1d[counter])
                    counter += 1
                createdMask.append(element)
                element = []

    def mask_size_change(self):
        mask_index = int(self.comboBox.currentIndex())
        size = 0
        if mask_index == 0:
            size = 3
        elif mask_index == 1:
            size = 5
        elif mask_index == 2:
            size = 7

        matrix_text = ""
        for i in range(size):
            for j in range(size):
                if i == size-1 and j == size-1:
                    matrix_text += "1"
                else:
                    matrix_text += "1,"
            matrix_text += "\n"
        self.textEdit.setText(matrix_text)


class Ui_ImageProcessingWindow(object):
    clicked_pixel_x = None
    clicked_pixel_y = None
    def setupUi(self, ImageProcessingWindow):
        ImageProcessingWindow.setObjectName("ImageProcessingWindow")
        ImageProcessingWindow.resize(1100, 800)
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
        self.lineVertical = QtWidgets.QFrame(self.centralwidget)
        self.lineVertical.setGeometry(QtCore.QRect(800, 0, 20, 800))
        self.lineVertical.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineVertical.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineVertical.setObjectName("lineVertical")
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
        self.greyscaleBox = QtWidgets.QComboBox(self.centralwidget)
        self.greyscaleBox.setGeometry(QtCore.QRect(810, 35, 104, 26))
        self.greyscaleBox.setObjectName("greyscaleBox")
        self.greyscaleBox.addItem("")
        self.greyscaleBox.addItem("")
        self.greyscaleBox.addItem("")
        self.greyscaleBox.addItem("")
        self.greyscaleBox.addItem("")
        self.tresholdLabel = QtWidgets.QLabel(self.centralwidget)
        self.tresholdLabel.setGeometry(QtCore.QRect(820, 10, 150, 16))
        self.tresholdLabel.setObjectName("tresholdLabel")
        self.filterLabel = QtWidgets.QLabel(self.centralwidget)
        self.filterLabel.setGeometry(QtCore.QRect(820, 260, 150, 16))
        self.filterLabel.setObjectName("filterLabel")
        self.maskLabel = QtWidgets.QLabel(self.centralwidget)
        self.maskLabel.setGeometry(QtCore.QRect(900, 280, 150, 16))
        self.maskLabel.setObjectName("maskLabel")
        self.tresholdValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.tresholdValueLabel.setGeometry(QtCore.QRect(820, 70, 150, 16))
        self.tresholdValueLabel.setObjectName("tresholdLabel")
        self.windowValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.windowValueLabel.setGeometry(QtCore.QRect(820, 170, 78, 16))
        self.windowValueLabel.setObjectName("windowValueLabel")
        self.kValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.kValueLabel.setGeometry(QtCore.QRect(950, 170, 78, 16))
        self.kValueLabel.setObjectName("kValueLabel")
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
        self.niblackButton = QtWidgets.QPushButton(self.centralwidget)
        self.niblackButton.setGeometry(QtCore.QRect(810,210,135,32))
        self.niblackButton.setObjectName("niblackButton")
        self.rangeValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.rangeValueLabel.setGeometry(QtCore.QRect(650, 630, 91, 16))
        self.rangeValueLabel.setObjectName("rangeValueLabel")
        self.maskValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.maskValueLabel.setGeometry(QtCore.QRect(950, 310, 80, 100))
        self.maskValueLabel.setObjectName("maskValueLabel")
        self.aRangeValue = QtWidgets.QLineEdit(self.centralwidget)
        self.aRangeValue.setGeometry(QtCore.QRect(660, 650, 30, 16))
        self.aRangeValue.setObjectName("aRangeValue")
        self.bRangeValue = QtWidgets.QLineEdit(self.centralwidget)
        self.bRangeValue.setGeometry(QtCore.QRect(710, 650, 30, 16))
        self.bRangeValue.setObjectName("bRangeValue")
        self.tresholdValueText = QtWidgets.QLineEdit(self.centralwidget)
        self.tresholdValueText.setGeometry(QtCore.QRect(820, 100, 30, 16))
        self.tresholdValueText.setObjectName("aRangeValue")
        self.windowValueText = QtWidgets.QLineEdit(self.centralwidget)
        self.windowValueText.setGeometry(QtCore.QRect(820, 190, 30, 16))
        self.windowValueText.setObjectName("windowValueText")
        self.kValueText = QtWidgets.QLineEdit(self.centralwidget)
        self.kValueText.setGeometry(QtCore.QRect(950, 190, 30, 16))
        self.kValueText.setObjectName("kValueText")
        self.basicTresholdButton = QtWidgets.QPushButton(self.centralwidget)
        self.basicTresholdButton.setGeometry(QtCore.QRect(870, 94, 135, 32))
        self.basicTresholdButton.setObjectName("basicTresholdButton")
        self.otsuTresholdButton = QtWidgets.QPushButton(self.centralwidget)
        self.otsuTresholdButton.setGeometry(QtCore.QRect(810, 130, 135, 32))
        self.otsuTresholdButton.setObjectName("otsuTresholdButton")
        self.greyscaleButton = QtWidgets.QPushButton(self.centralwidget)
        self.greyscaleButton.setGeometry(QtCore.QRect(930, 32, 135, 32))
        self.greyscaleButton.setObjectName("greyscaleButton")
        self.stretchButton = QtWidgets.QPushButton(self.centralwidget)
        self.stretchButton.setGeometry(QtCore.QRect(650, 670, 135, 32))
        self.stretchButton.setObjectName("stretchButton")
        self.equalizationButton = QtWidgets.QPushButton(self.centralwidget)
        self.equalizationButton.setGeometry(QtCore.QRect(650, 700, 135, 32))
        self.equalizationButton.setObjectName("equalizationButton")
        self.maskButton = QtWidgets.QPushButton(self.centralwidget)
        self.maskButton.setGeometry(QtCore.QRect(820, 308, 110, 32))
        self.maskButton.setObjectName("maskButton")
        self.convolutionButton = QtWidgets.QPushButton(self.centralwidget)
        self.convolutionButton.setGeometry(QtCore.QRect(820, 350, 110, 32))
        self.convolutionButton.setObjectName("convolutionButton")


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
        self.basicTresholdButton.clicked.connect(self.value_threshold)
        self.otsuTresholdButton.clicked.connect(self.otsu_threshold)
        self.niblackButton.clicked.connect(self.niblack_threshold)
        self.greyscaleButton.clicked.connect(self.turn_greyscale)
        self.maskButton.clicked.connect(self.create_mask)
        self.convolutionButton.clicked.connect(self.convolution_filter)
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
        self.greyscaleBox.setItemText(0, _translate("ImageProcessingWindow", "Mean"))
        self.greyscaleBox.setItemText(1, _translate("ImageProcessingWindow", "Lum"))
        self.greyscaleBox.setItemText(2, _translate("ImageProcessingWindow", "Red"))
        self.greyscaleBox.setItemText(3, _translate("ImageProcessingWindow", "Green"))
        self.greyscaleBox.setItemText(4, _translate("ImageProcessingWindow", "Blue"))
        self.tresholdValueLabel.setText(_translate("ImageProcessingWindow", "Threshold value:"))
        self.windowValueLabel.setText(_translate("ImageProcessingWindow", "Window size:"))
        self.kValueLabel.setText(_translate("ImageProcessingWindow", "k paremeter:"))
        self.tresholdLabel.setText(_translate("ImageProcessingWindow", "Threshold section:"))
        self.filterLabel.setText(_translate("ImageProcessingWindow", "Filters section:"))
        self.maskValueLabel.setText(_translate("ImageProcessingWindow", "No mask picked"))
        self.maskLabel.setText(_translate("ImageProcessingWindow", "Pick mask:"))
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
        self.basicTresholdButton.setText(_translate("ImageProcessingWindow", "Value threshold"))
        self.otsuTresholdButton.setText(_translate("ImageProcessingWindow", "Otsu threshold"))
        self.niblackButton.setText(_translate("ImageProcessingWindow", "Niblack threshold"))
        self.greyscaleButton.setText(_translate("ImageProcessingWindow", "Turn greyscale"))
        self.maskButton.setText(_translate("ImageProcessingWindow", "Create mask"))
        self.convolutionButton.setText(_translate("ImageProcessingWindow", "Convolution filter"))


        self.aRangeValue.setText("0")
        self.bRangeValue.setText("255")
        self.tresholdValueText.setText("150")
        self.kValueText.setText("-0.5")
        self.windowValueText.setText("3")
        my_regex = QtCore.QRegExp("([0-9]|[1-8][0-9]|9[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])")
        my_validator = QtGui.QRegExpValidator(my_regex, self.aRangeValue)
        self.aRangeValue.setValidator(my_validator)
        my_validator = QtGui.QRegExpValidator(my_regex, self.bRangeValue)
        self.bRangeValue.setValidator(my_validator)
        my_validator = QtGui.QRegExpValidator(my_regex, self.tresholdValueText)
        self.tresholdValueText.setValidator(my_validator)


    def convolution_filter(self):
        img = Image.open(self.pathLabel.text(), "r")
        img = img.convert("RGB")
        np_img = np.asarray(img)

        pix_val = list(img.getdata())
        coloured = self.check_coloured(pix_val)


        maskLen = len(createdMask[0])

        window_val = 0
        if maskLen == 3:
            window_val = 3
        elif maskLen == 5:
            window_val = 5
        elif maskLen == 7:
            window_val = 7

        pad_w = int(window_val / 2)
        mask_weight = 0
        for k in range(window_val):
            for l in range(window_val):
                mask_weight += createdMask[k][l]
        if mask_weight == 0:
            mask_weight = 1

        result_array = np.zeros(shape=(len(np_img),len(np_img[0]), 3))

        if coloured:
            k_counter = 0
            l_counter = 0
            for i in range(pad_w, len(np_img) - pad_w):
                for j in range(pad_w, len(np_img[0]) - pad_w):
                    sum_r = 0
                    sum_g = 0
                    sum_b = 0
                    for k in range(window_val):
                        for l in range(window_val):
                            sum_r += np_img[k + k_counter][l + l_counter][0] * createdMask[k][l]
                            sum_g += np_img[k + k_counter][l + l_counter][1] * createdMask[k][l]
                            sum_b += np_img[k + k_counter][l + l_counter][2] * createdMask[k][l]

                    pix_r = sum_r / mask_weight
                    pix_g = sum_g / mask_weight
                    pix_b = sum_b / mask_weight

                    if pix_r > 255:
                        pix_r = 255
                    elif pix_r < 0:
                        pix_r = 0
                    if pix_g > 255:
                        pix_g = 255
                    elif pix_g < 0:
                        pix_g = 0
                    if pix_b > 255:
                        pix_b = 255
                    elif pix_b < 0:
                        pix_b = 0

                    result_array[i, j, 0] = pix_r
                    result_array[i, j, 1] = pix_g
                    result_array[i, j, 2] = pix_b

                    l_counter += 1
                k_counter += 1
                l_counter = 0
            img_filter = Image.fromarray(result_array.astype('uint8'), 'RGB')
            img_filter.save("Filters_img/Conv_filter.png")
            print("Saved image.")
        else:
            k_counter = 0
            l_counter = 0
            for i in range(pad_w, len(np_img) - pad_w):
                for j in range(pad_w, len(np_img[0]) - pad_w):
                    sum_g = 0
                    for k in range(window_val):
                        for l in range(window_val):
                            sum_g += np_img[k + k_counter][l + l_counter][0] * createdMask[k][l]

                    pix_g = sum_g / mask_weight

                    if pix_g > 255:
                        pix_g = 255
                    elif pix_g < 0:
                        pix_g = 0

                    result_array[i, j, 0] = pix_g
                    result_array[i, j, 1] = pix_g
                    result_array[i, j, 2] = pix_g

                    l_counter += 1
                k_counter += 1
                l_counter = 0

            img_filter = Image.fromarray(result_array.astype('uint8'), 'RGB')
            img_filter.save("Filters_img/Conv_greyscale_filter.png")
            print("Saved image.")







    def create_mask(self):
        self.showDialog()


    def showDialog(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_MaskDialog()
        self.ui.setupUi(self.window)
        #self.window.show()
        returnCode = self.window.exec_()
        if returnCode == 1:
            self.maskValueLabel.setText(mask)

    def niblack_threshold(self):
        window_val = int(self.windowValueText.text())
        k_val = float(self.kValueText.text())

        self.turn_greyscale()
        img = Image.open("Threshold_img/greyscale.jpg", "r")
        image_matrix = numpy.array(img)

        pad_w = int(window_val / 2)

        x = np.pad(image_matrix, pad_width=pad_w, mode="constant", constant_values=0)
        counter_mask = window_val * window_val
        k_counter = 0
        l_counter = 0

        for i in range(pad_w, len(x) - pad_w):
            for j in range(pad_w, len(x[0]) - pad_w):
                avarage = 0
                std_div = 0
                sum = 0
                for k in range(window_val):
                    for l in range(window_val):
                        sum += x[k + k_counter][l + l_counter]


                avarage = sum / counter_mask
                sum = 0
                for k in range(window_val):
                    for l in range(window_val):
                        sum += pow(x[k + k_counter][l + l_counter] - avarage, 2)

                std_div = math.sqrt(sum / counter_mask)
                threshold = avarage + (k_val * std_div)

                if x[i][j] < threshold:
                    x[i][j] = 0
                elif x[i][j] >= threshold:
                    x[i][j] = 255
                l_counter += 1
            k_counter += 1
            l_counter = 0

        threshold_array_sl = x[pad_w:x.shape[0]-pad_w, pad_w:x.shape[1]-pad_w]
        img_tr = Image.fromarray(threshold_array_sl, 'L')
        img_tr.save("Threshold_img/niblack_threshold.png")
        print("Saved image.")

        # save in folder
        pix = QtGui.QPixmap("Threshold_img/niblack_threshold.png")
        self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
        scaled_pixmap = pix.scaled(800, 620)
        self.photo.setPixmap(scaled_pixmap)
        self.sizeBox.setCurrentIndex(3)
        self.sizeBox.hide()
        self.sizeBox.show()
        self.photo.hide()
        self.photo.show()
        # plot
        plt.subplot(2, 1, 1)
        plt.title('Before niblack threshold', size=16, y=1.12)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)

        plt.subplot(2, 1, 2)
        plt.title('After niblack threshold', size=16, y=1.12)
        plt.imshow(img_tr, cmap='gray', vmin=0, vmax=255)

        plt.tight_layout()
        plt.show()


    def niblack_v2(self):
        #pioterowa
        window_val = int(self.windowValueText.text())
        k_val = float(self.kValueText.text())

        self.turn_greyscale()
        img = Image.open("Threshold_img/greyscale.jpg", "r")
        image_matrix = numpy.array(img)
        pad_w = int(window_val / 2)
        counter_mask = window_val * window_val

        threshold_array = np.zeros((image_matrix.shape[0], image_matrix.shape[1]))

        for i in range(image_matrix.shape[0]):
            for j in range(image_matrix.shape[1]):
                avarage = 0
                std_div = 0
                sum = 0
                try:
                    for k in range(-1 * pad_w, pad_w + 1):
                        for l in range(-1 * pad_w, pad_w + 1):
                            sum += image_matrix[i + k, j + l]
                except:
                    sum += 0

                avarage = sum / counter_mask
                var = 0
                try:
                    for k in range(window_val):
                        for l in range(window_val):
                            var += pow(image_matrix[i+k, j+l] - avarage, 2)
                except:
                    sum += pow(0-avarage, 2)

                variance = var / counter_mask
                std_div = np.sqrt(variance)
                threshold = avarage + (k_val * std_div)

                if image_matrix[i][j] < threshold:
                    image_matrix[i][j] = 0
                elif image_matrix[i][j] >= threshold:
                    image_matrix[i][j] = 255

        img_tr = Image.fromarray(image_matrix, 'L')
        img_tr.save("Threshold_img/niblack_threshold.png")
        print("Saved image.")

        # save in folder
        pix = QtGui.QPixmap("Threshold_img/niblack_threshold.png")
        self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
        scaled_pixmap = pix.scaled(800, 620)
        self.photo.setPixmap(scaled_pixmap)
        self.sizeBox.setCurrentIndex(3)
        self.sizeBox.hide()
        self.sizeBox.show()
        self.photo.hide()
        self.photo.show()
        # plot
        plt.subplot(2, 1, 1)
        plt.title('Before niblack threshold', size=16, y=1.12)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)

        plt.subplot(2, 1, 2)
        plt.title('After niblack threshold', size=16, y=1.12)
        plt.imshow(img_tr, cmap='gray', vmin=0, vmax=255)

        plt.tight_layout()
        plt.show()



    def otsu_threshold(self):
        self.turn_greyscale()
        img = Image.open("Threshold_img/greyscale.jpg", "r")
        pix_val = list(img.getdata())

        hist = self.count_pixels_histogram(pix_val)

        sum = 0
        for j in range(len(hist)):
            sum += j * hist[j]

        sum_b = 0
        w_b = 0
        w_f = 0
        max = 0
        threshold = 0
        pix_count = len(pix_val)

        for k in range(len(hist)):
            w_b += hist[k]
            if w_b == 0:
                continue

            w_f = pix_count - w_b
            if w_f == 0:
                break

            sum_b += float(k * hist[k])

            m_b = sum_b / w_b
            m_f = (sum - sum_b) / w_f

            variance_diff = float(w_b) * float(w_f) * (m_b - m_f) * (m_b - m_f)

            if variance_diff > max:
                max = variance_diff
                threshold = k

        print(threshold)
        for i in range(len(pix_val)):
            if pix_val[i] < threshold:
                pix_val[i] = 0
            elif pix_val[i] >= threshold:
                pix_val[i] = 255

        result_img = []
        for i in range(len(pix_val)):
            result_img.append(pix_val[i])

        threshold_img = Image.new('L', img.size)
        threshold_img.putdata(result_img)

        threshold_img.save("Threshold_img/otsu_threshold.png")
        print("Saved image.")

        #save in folder
        pix = QtGui.QPixmap("Threshold_img/otsu_threshold.png")
        self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
        scaled_pixmap = pix.scaled(800, 620)
        self.photo.setPixmap(scaled_pixmap)
        self.sizeBox.setCurrentIndex(3)
        self.sizeBox.hide()
        self.sizeBox.show()
        self.photo.hide()
        self.photo.show()
        #plot
        plt.subplot(2, 1, 1)
        plt.title('Before otsu threshold', size=16, y=1.12)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)

        plt.subplot(2, 1, 2)
        plt.title('After otsu threshold', size=16, y=1.12)
        plt.imshow(threshold_img, cmap='gray', vmin=0, vmax=255)

        plt.tight_layout()
        plt.show()

    def value_threshold(self):
        self.turn_greyscale()
        img = Image.open("Threshold_img/greyscale.jpg", "r")

        pix_val = list(img.getdata())
        threshold = int(self.tresholdValueText.text())

        for i in range(len(pix_val)):
            if pix_val[i] < threshold:
                pix_val[i] = 0
            elif pix_val[i] >= threshold:
                pix_val[i] = 255

        result_img = []
        for i in range(len(pix_val)):
            result_img.append(pix_val[i])

        threshold_img = Image.new('L', img.size)
        threshold_img.putdata(result_img)

        threshold_img.save("Threshold_img/value_threshold.png")
        print("Saved image.")

        #save in folder
        pix = QtGui.QPixmap("Threshold_img/value_threshold.png")
        self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
        scaled_pixmap = pix.scaled(800, 620)
        self.photo.setPixmap(scaled_pixmap)
        self.sizeBox.setCurrentIndex(3)
        self.sizeBox.hide()
        self.sizeBox.show()
        self.photo.hide()
        self.photo.show()
        #plot
        plt.subplot(2, 1, 1)
        plt.title('Before threshold', size=16, y=1.12)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)

        plt.subplot(2, 1, 2)
        plt.title('After threshold', size=16, y=1.12)
        plt.imshow(threshold_img, cmap='gray', vmin=0, vmax=255)

        plt.tight_layout()
        plt.show()

    def turn_greyscale(self):
        index = int(self.greyscaleBox.currentIndex())

        img = Image.open(self.pathLabel.text(), "r")
        img = img.convert("RGB")

        pix_val = list(img.getdata())

        result_greyscale = []
        if index == 0:
            for i in range(len(pix_val)):
                val = int((pix_val[i][0] + pix_val[i][1] + pix_val[i][2]) / 3)
                result_greyscale.append(val)
        elif index == 1:
            for i in range(len(pix_val)):
                val = int((0.2126 * pix_val[i][0]) + (0.7152 * pix_val[i][1]) + (0.0722 * pix_val[i][2]))
                result_greyscale.append(val)
        elif index == 2:
            for i in range(len(pix_val)):
                val = int(pix_val[i][0])
                result_greyscale.append(val)
        elif index == 3:
            for i in range(len(pix_val)):
                val = int(pix_val[i][1])
                result_greyscale.append(val)
        elif index == 4:
            for i in range(len(pix_val)):
                val = int(pix_val[i][2])
                result_greyscale.append(val)

        greyscale_img = Image.new('L', img.size)
        greyscale_img.putdata(result_greyscale)

        greyscale_img.save("Threshold_img/greyscale.jpg")
        pix = QtGui.QPixmap("Threshold_img/greyscale.jpg")
        self.photo.setGeometry(QtCore.QRect(0, 0, 800, 620))
        scaled_pixmap = pix.scaled(800, 620)
        self.photo.setPixmap(scaled_pixmap)
        self.sizeBox.setCurrentIndex(3)
        self.sizeBox.hide()
        self.sizeBox.show()
        self.photo.hide()
        self.photo.show()

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
