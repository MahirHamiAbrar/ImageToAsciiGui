import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *


# image viewer class
class ImageViewer:
    def __init__(self, widget=None, path=None, load=False, placeholder_text=''):

        # the label where image will be shown
        self.widget = widget

        # image path
        if path:
            self.imgPath = str(path)

        # load the image when initializing the UI if permitted
        if load:
            self.loadImage()

        # set placeholder text
        self.text = str(placeholder_text) if placeholder_text else 'Selected images appear here.'

    # set the placeholder text
    def setPlaceholderText(self, text):
        self.text = str(text)

    # set the image widget
    def setImageWidget(self, widget):
        self.widget = widget
        self.widget.setAcceptDrops(True)

    # set image path
    def setImageFile(self, file):
        if path:
            self.imgPath = str(file)

    # load image to the widget
    def loadImage(self, path=None, keepAspectRatio=True):
        if path:
            self.imgPath = str(path)

        # create a pixmap to load and view image
        pixmap = QPixmap(self.imgPath)

        # scale the image
        if not keepAspectRatio:
            pixmap = pixmap.scaled(self.widget.size().width(), self.widget.size().height())
        else:
            pixmap = pixmap.scaled(self.widget.size().width(), self.widget.size().height(), Qt.KeepAspectRatio)

        # show the image in the image widget
        self.widget.setPixmap(pixmap)
        self.widget.show()

    # unload the image
    def unloadImage(self):
        self.widget.clear()
        self.widget.setText(self.text)
