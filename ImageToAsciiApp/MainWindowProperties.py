import os
import pyautogui as pg

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Menu import CustomMenu
from AnimationProperties import WindowAnimator


# MAIN WINDOW PROPERTIES CLASS
# ui_path, window title, window_minimum_size, window_default_size
class MainWindowProperties(QMainWindow):
    def __init__(self, ui_path, title, msize, nsize):
        QMainWindow.__init__(self)

        # ui path
        self.ui_path = ui_path
        self.resizeAnimTime = 500     # window resizing animation duration
        self.sizegriptimerTime = 200  # size gripper animation duration
        self.windowMaximized = False  # window maximize status
        self.minimizing = False       # is the window minimizing right now?
        self.close_window = False     # should the event manager close the window?

        # normal size
        self.normal_size = nsize
        # screen size
        self.screen_size = list(pg.size())

        # default sized window's center position on screen
        self.normal_center_pos = (int((self.screen_size[0] - self.normal_size[0]) / 2),
                                  int((self.screen_size[1] - self.normal_size[1]) / 2))

        # load the ui
        self.ui = uic.loadUi(self.ui_path, self)
        # set mouse move event
        self.titleBar.mouseMoveEvent = self.moveWindow

        # set window flags
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        # set a translucent background to the window
        self.setAttribute(Qt.WA_TranslucentBackground)

        # window resizing
        self.sizegrip = QSizeGrip(self.sizegripper)
        self.sizegrip.setVisible(True)

        # previous window pos
        self.prev_pos = self.normal_center_pos
        # previou window size
        self.prev_size = self.getCurSize(self)

        # TIMERS
        # window maximizing timer
        self.maximizeTimer = QTimer()
        self.maximizeTimer.timeout.connect(self.maximizeWindow)

        # window minimizing timer
        self.minimizeTimer = QTimer()
        self.minimizeTimer.timeout.connect(self.minimizeWindow)

        # window restoring timer
        self.normalizeTimer = QTimer()
        self.normalizeTimer.timeout.connect(self.normalizeWindow)

        # size gripper (window resizing widget) hide/visible animation timer
        self.sizegripTimer = QTimer()
        self.sizegripTimer.timeout.connect(lambda: self.sizegrip.setVisible(True))
        # ------------------------------

        # animator object
        self.animator = WindowAnimator(self, msize, nsize)
        self.animator.setRuntimeEventManager(self.animationRuntimeEventManager)

        # menu widget
        self.menu = CustomMenu(self, self.themeBtnFrame, self.menuRuntimeEventManager)
        self.menu.setSize(200, 100)
        # self.loadMenu()

        # button tasks
        self.minimizeBtn.clicked.connect(self.showMinimized_)
        self.maximizeBtn.clicked.connect(self.maximizeAndRestore)
        self.closeBtn.clicked.connect(self.close_)
        self.themeBtn.clicked.connect(lambda: self.menu.showOrHide(self.themeBtn.isChecked()))

        # set window title
        self.setWindowTitle(title)  # MOVE WINDOW EVENT

        # start timers
        self.sizegripTimer.start(self.sizegriptimerTime)

    # move window on mouse press
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    # window move event
    def moveWindow(self, event):
        try:
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        except:
            pass

    # catch the happening event and do some stuff during the event
    def event(self, e):
        # check if it's a window state changing event
        if e.type() == e.WindowStateChange:

            # show animation while restoring window; 'Qt.WindowNoState' refers to restore window event
            if e.oldState() == Qt.WindowMinimized and self.windowState() == Qt.WindowNoState:
                self.show()
                self.showRestored_()

            # show some animation while window minimize event
            elif e.oldState() == Qt.WindowNoState and self.windowState() == Qt.WindowMinimized:
                if not self.minimizing:
                    self.showNormal()
                    self.showMinimized_()

        # no matter what happens, return the event
        return super(MainWindowProperties, self).event(e)

    # runtime event manager
    # in here this function may not doing anything, but in case of using it outside this class (inheriting/non-inheriting)
    # use have to override this function to use it
    def runtimeEventManager(self, event):
        pass

    # evt manager for menu
    def menuRuntimeEventManager(self, data):
        # if data is not empty
        if data:
            if type(data) == str:
                if data == 'show':
                    self.loadMenu()
            else:
                self.themeBtn.setChecked(False)

                fname = f"themes/{data.text().replace(' ', '-')}.css"

                with open(fname, 'r') as f:
                    stylesheet = f.read()

                self.setStyleSheet(stylesheet)

    # load menu
    def loadMenu(self):
        data = [file.replace('-', ' ').replace('.css', '') for file in os.listdir('themes/') if file.endswith('.css')]
        self.menu.addItems(data, clearAll=True)

    # get current pos
    def getCurPos(self, widget):
        return (int(widget.pos().x()), int(widget.pos().y()))

    # get current size
    def getCurSize(self, widget):
        return (int(widget.size().width()), int(widget.size().height()))

    # runtime event manager function
    def animationRuntimeEventManager(self, data):
        if data:
            cmd = data['cmd']
            value = data['value']

            if cmd == 'fade-in':
                pass

            elif cmd == 'fade-out' and self.close_window is True:
                self.close()

            elif cmd == 'parallel-anim-start':
                pass

    # sizegripper guard function
    def sizegripperGuard(self):
        if self.windowMaximized:
            self.sizegripper.setEnabled(False)
            self.sizegripper.hide()
        else:
            self.sizegripper.setEnabled(True)
            self.sizegripper.show()

    # show normal
    def showNormal_(self):
        start_pos = self.getCurPos(self)
        end_pos = self.normal_center_pos

        start_size = self.getCurSize(self)
        end_size = self.normal_size

        pos_anim = self.animator.animate(self, start_pos, end_pos, 'pos', self.resizeAnimTime)
        size_anim = self.animator.animate(self, start_size, end_size, 'size', self.resizeAnimTime)

        self.animator.startParallelAnimation(pos_anim, size_anim)
        self.normalizeTimer.start(self.resizeAnimTime)

        self.windowMaximized = False
        self.runtimeEventManager('normal')

    # show restored
    def showRestored_(self):
        startpos = self.getCurPos(self)
        endpos = (self.prev_pos[0], self.prev_pos[1])

        pos_anim = self.animator.animate(self, startpos, endpos, 'pos', self.resizeAnimTime)
        self.animator.startParallelAnimation(pos_anim)

        self.close_window = False
        self.window_minimized = False
        self.setWindowState(Qt.WindowNoState)
        self.animator.showFadeInAnimation(animate_size_pos=False)
        self.runtimeEventManager('restore')

    # maximization and restoring window
    def maximizeAndRestore(self):
        if self.windowMaximized:
            self.showNormal_()
        else:
            self.showMaximized_()

        self.sizegripperGuard()

    # show maximized
    def showMaximized_(self):
        self.prev_pos = self.getCurPos(self)
        self.prev_size = self.getCurSize(self)

        start_pos = self.getCurPos(self)
        end_pos = (0, 0)

        start_size = self.getCurSize(self)
        end_size = self.screen_size

        pos_anim = self.animator.animate(self, start_pos, end_pos, 'pos', self.resizeAnimTime)
        size_anim = self.animator.animate(self, start_size, end_size, 'size', self.resizeAnimTime)

        self.animator.startParallelAnimation(pos_anim, size_anim)
        self.maximizeTimer.start(self.resizeAnimTime)

        self.windowMaximized = True
        self.runtimeEventManager('maximize')

    # show minimized
    def showMinimized_(self):
        self.minimizing = True

        startpos = list(self.getCurPos(self))
        endpos = (startpos[0], int(self.screen_size[1]))

        pos_anim = self.animator.animate(self, startpos, endpos, 'pos', self.resizeAnimTime)
        self.animator.startParallelAnimation(pos_anim)

        self.prev_pos = startpos.copy()

        self.close_window = False

        self.minimizeTimer.start(200)
        self.animator.showFadeOutAnimation(animate_size_pos=False)
        self.runtimeEventManager('minimize')

    # show the window
    def show_(self):
        self.show()
        self.animator.showFadeInAnimation(False)
        self.runtimeEventManager('show')

    # maximize window
    def maximizeWindow(self):
        self.showMaximized()
        self.maximizeTimer.stop()
        self.setWindowState(Qt.WindowMaximized)

    # minimize window
    def minimizeWindow(self):
        self.showMinimized()
        self.minimizeTimer.stop()
        self.setWindowState(Qt.WindowMinimized)
        self.minimizing = False

    # normalize window
    def normalizeWindow(self):
        self.showNormal()
        self.normalizeTimer.stop()
        self.setWindowState(Qt.WindowNoState)

    # close the window
    def close_(self):
        self.close_window = True
        self.animator.showFadeOutAnimation(False)
        self.runtimeEventManager('close')
