import os
import sys
import platform

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from converter import *
from FileBrowser import *
from Clipboard import copy
from WidgetHighlighter import highlightWidget, unhighlightWidget
from ImageViewer import ImageViewer
from MainWindowProperties import MainWindowProperties


class MainWindow(MainWindowProperties):
    def __init__(self):
        MainWindowProperties.__init__(self, 'ui.ui', 'Image to Ascii Converter', (618, 89), (1110, 650))

        self.ascii_img = ''      # ascii image is stored as a string
        self.image_file = ''     # image file
        self.output_file = ''    # output file

        # create an Image viewer object
        self.viewer = ImageViewer(self.imageViewer)
        self.viewer.setPlaceholderText('Choose or Drag and Drop an Image in Here')

        # set button tasks
        self.chooseImgBtn.clicked.connect(lambda: self.openImageFile())
        self.removeImgBtn.clicked.connect(lambda: self.unloadImage())
        self.selectOutFileBtn.clicked.connect(lambda: self.selectOutputFile())
        self.convertBtn.clicked.connect(lambda: self.convertToAscii())
        self.copyAsciiBtn.clicked.connect(lambda: self.copyAsciiImage())
        self.openTextEditorBtn.clicked.connect(lambda: self.openImageInTextEitor())

        # slider
        self.scaleSlider.setRange(0, 100)
        self.scaleSlider.setPageStep(1)
        self.scaleSlider.valueChanged.connect(self.sliderValueUpdate)

        # line edit tasks
        self.imageFileEdit.textChanged.connect(self.loadImage)
        self.outputFileEdit.textChanged.connect(self.updateOutputPath)
        self.widthEdit.textChanged.connect(self.widthEditGuard)
        self.scaleEdit.textChanged.connect(self.scaleEditGuard)

        # disable buttons
        self.convertBtn.setEnabled(True)
        self.openTextEditorBtn.setEnabled(False)

    # load image
    def loadImage(self, path):
        if os.path.exists(path):
            self.image_file = path
            self.viewer.loadImage(self.image_file, keepAspectRatio=False)

    # update new output path
    def updateOutputPath(self, text):
        if str(text):
            self.output_file = text

            # check if the path exist or not
            if os.path.exists(self.output_file):
                self.openTextEditorBtn.setEnabled(True)
            else:
                self.openTextEditorBtn.setEnabled(False)
        else:
            self.openTextEditorBtn.setEnabled(False)

    # guard width line edit
    def widthEditGuard(self, text):
        try:
            text = int(text)
            unhighlightWidget(self.widthEdit, focus=True)
            self.convertBtn.setEnabled(True)
        except ValueError:
            highlightWidget(self.widthEdit, focus=True)
            self.convertBtn.setEnabled(False)

    # guard scale line edit
    def scaleEditGuard(self, text):
        try:
            text = float(text)
            self.scaleSlider.setValue(text*100)
            unhighlightWidget(self.scaleEdit, focus=True)
            self.convertBtn.setEnabled(True)
        except ValueError:
            highlightWidget(self.scaleEdit, focus=True)
            self.convertBtn.setEnabled(False)

    # OPEN IMAGE FILES
    def openImageFile(self):
        filename = browseFile(None, 'Select an Image', os.getcwd(), IMAGE_FILTERS)

        # if filename is not none, then procceed
        if filename:
            self.imageFileEdit.setText(filename)

    # OPEN IMAGE FILES
    def selectOutputFile(self):
        filename = createFile(None, 'Select a file to save output', os.getcwd(), ALL_FILES)

        # if filename is not none, then procceed
        if filename:
            self.output_file = filename
            self.outputFileEdit.clear()
            self.outputFileEdit.setText(filename)

    # unload image
    def unloadImage(self):
        self.image_file = ''
        self.viewer.unloadImage()
        self.imageFileEdit.clear()

    # convert image to ascii image
    def convertToAscii(self):
        # get width and scale
        width = int(self.widthEdit.text())
        scale = float(self.scaleEdit.text())

        ascii_img = convertImageToAscii(self.image_file, width, scale)
        self.ascii_img = createOutputText(ascii_img)

        self.imageOutputViewer.setText(self.ascii_img)

        self.saveOutputFile()

    # copy the ascii image
    def copyAsciiImage(self):
        copy(self.ascii_img)

    # save output file
    def saveOutputFile(self):
        if self.output_file:
            with open(self.output_file, 'w') as f:
                f.write(self.ascii_img)

    # open Image In TextEitor
    def openImageInTextEitor(self):
        system = platform.system().lower()

        if system == 'windows':
            os.system(self.output_file)
        elif system == 'linux':
            os.system(f"cat {self.output_file}")

    # update slider value
    def sliderValueUpdate(self, value):
        value = float(int(value)/100)
        self.scaleEdit.setText(str(value))


# show and ececute the window
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show_()
    app.exec_()
