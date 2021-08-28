from PyQt5.QtWidgets import *

# image filters
IMAGE_FILTERS = "JPG (*.jpg);;PNG (*.png);;JPEG (*.jpeg);;BPM (*.bmp);;CUR (*.cur);;GIF(*.gif);;Icons (*.ico);;PBM (" \
                "*.pbm);;PGM (*.pgm);;PPM (*.ppm);;SVG (*.svg);;SVGZ (*.svgz);;TGA (*.tga);;TIF (*.tif);;TIFF (" \
                "*.tiff);;WBMP (*.wbmp);;WEBP (*.webp);;XBM (*.xbm);;XPM (*.xpm) "
# all files
ALL_FILES = "All files (*.*)"


# browse for folders only
def browseFolder(window, title='', default_path='C://', filter=None, sidebar_urls=[]):
    # create a dialog object
    dialog = QFileDialog(window, title, default_path, filter=filter)
    # set file mode; in this case directory only
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    # convert all urls to a QUrl object
    # and then set sidebar urls
    dialog.setSidebarUrls([QUrl.fromLocalFile(url) for url in sidebar_urls])

    # after successful execution, return the data
    if dialog.exec_() == QDialog.Accepted:
        return dialog.selectedFiles()[0]


# browse for files only
def browseFile(window, title='', default_path='C://', filter=None):
    # create a dialog object
    return QFileDialog.getOpenFileName(window, title, default_path, filter=filter)[0]


# browse multiple files
def browseMultipleFile(window, title='', default_path='C://', filter=None, sidebar_urls=[]):
    # create a dialog object
    dialog = QFileDialog(window, title, default_path, filter=filter)
    dialog.setLabelText(QFileDialog.Accept, 'Choose')
    # dialog.setOption(QFileDialog.DontUseNativeDialog, True)
    # set file mode; in this case directory only
    dialog.setFileMode(QFileDialog.AnyFile)
    # convert all urls to a QUrl object
    # and then set sidebar urls
    dialog.setSidebarUrls([QUrl.fromLocalFile(url) for url in sidebar_urls])

    # after successful execution, return the data
    if dialog.exec_() == QDialog.Accepted:
        return dialog.selectedFiles()


# create file
def createFile(window, title='', default_path='C://', filter=None):
    # create a dialog object
    dialog = QFileDialog(window, title, default_path, filter=filter)
    dialog.setLabelText(QFileDialog.Accept, 'Select')
    return dialog.getSaveFileName(window, title, default_path, filter=filter)[0]
