import pyautogui as pg

from PyQt5.QtCore import *

class WindowAnimator:
    def __init__(self, window, min_size=None, default_size=None, cur_opc=0.0, min_opc=0, max_opc=1.0, opc_rate=0.1, opc_time=30, **kwargs):
        # main window
        self.window = window

        # screen size
        self.screen_size = list(pg.size())

        # window opacity properties
        self.opc = cur_opc
        self.max_opc = max_opc
        self.min_opc = min_opc
        self.opc_rate = opc_rate
        self.opc_time = opc_time
        self.opc_mode = '+'
        # -------------------------

        # RRUNTIME EVENT MANAGER FUNCTION
        self.runtime_evt_manager = None

        # should it raise the dialog while a mouse press event?
        self.raiseOnMousePress = False

        # window size properties
        self.min_size = min_size
        self.default_size = default_size
        # -----------------------

        if self.min_size:
            # window positions
            self.window_center_pos = (int((self.screen_size[0]-self.min_size[0])/2),
                                        int((self.screen_size[1]-self.min_size[1])/2))

        if self.default_size:
            self.center_pos = (int((self.screen_size[0]-self.default_size[0])/2),
                                int((self.screen_size[1]-self.default_size[1])/2))
            self.max_size = [self.default_size[0]+200, self.default_size[1]+200]
        # -----------------------

        # timers ---------------------
        # close
        self.ctimer = QTimer()
        self.ctimer.timeout.connect(lambda: self.callRuntimeEventManager(cmd='fade-out', value=None))

        self.opctimer = QTimer()
        self.opctimer.timeout.connect(self.changeopct_)
        # --------------------------------

        # set window opacity
        self.window.setWindowOpacity(self.opc)

    # set window opening task
    def setRuntimeEventManager(self, task):
        if callable(task):
            self.runtime_evt_manager = task

    # set window Closing task
    def callRuntimeEventManager(self, cmd, value):
        data = {'cmd': cmd, 'value': value}
        if callable(self.runtime_evt_manager):
            self.runtime_evt_manager.__call__(data)

    # animate widgets
    def animate(self, widget, startvalue, endvalue, propertyname='pos', duration=500,
                curve=QEasingCurve.InOutQuart, return_=True):

        if propertyname == 'pos':
            function = QPoint
        else:
            function = QSize

        startvalue = function(startvalue[0], startvalue[1])
        endvalue = function(endvalue[0], endvalue[1])

        self.window.animation = QPropertyAnimation(widget, propertyname.encode())
        self.window.animation.setDuration(duration)
        self.window.animation.setStartValue(startvalue)
        self.window.animation.setEndValue(endvalue)
        self.window.animation.setEasingCurve(curve)

        if return_:
            return self.window.animation

        self.window.animation.start()

    # animation in a parallel animation group
    def startParallelAnimation(self, *animations):
        # animation group
        self.window.parallel_animation = QParallelAnimationGroup()

        for animation in animations:
            self.window.parallel_animation.addAnimation(animation)

        self.window.parallel_animation.start()

        # call event manager
        self.callRuntimeEventManager(cmd='parallel-anim-start', value=None)

    # change opc
    def changeopct_(self):
        stop = False

        if self.opc_mode == '+':
            if self.opc <= self.max_opc:
                self.opc += self.opc_rate
            else:
                self.opc = self.max_opc
                stop = True

        if self.opc_mode == '-':
            if self.opc >= self.min_opc:
                self.opc -= self.opc_rate
            else:
                self.opc = self.min_opc
                stop = True

        self.window.setWindowOpacity(self.opc)

        if stop:
            self.opctimer.stop()

    # set opacity mode
    def setopctmode_(self, mode):
        self.opc_mode = mode

        if mode == '+':
            self.opc = self.min_opc
        else:
            self.opc = self.max_opc

    # window opening animation
    def showFadeInAnimation(self, animate_size_pos=True):
        self.setopctmode_('+')
        self.opctimer.start(self.opc_time)

        # if other animations are allowed to execute, then
        # show size and position animation at startup
        if animate_size_pos:

            window_center_pos = (int((self.screen_size[0]-self.max_size[0])/2),
                int((self.screen_size[1]-self.max_size[1])/2))

            # previous page animation
            pos_anim = self.animate(self.window, window_center_pos, self.center_pos, 'pos', duration=500)
            # current page animation
            size_anim = self.animate(self.window, self.max_size, self.default_size, 'size', duration=500)

            self.startParallelAnimation(pos_anim, size_anim)

        # call event manager
        self.callRuntimeEventManager(cmd='fade-in', value=None)

    # window closing animation
    def showFadeOutAnimation(self, animate_size_pos=True):
        self.ctimer.start(300)
        self.setopctmode_('-')
        self.opctimer.start(self.opc_time)

        # if other animations are allowed to execute, then
        # show size and position animation at window closing
        if animate_size_pos:
            # previous page animation
            pos_anim = self.animate(self.window, self.center_pos, self.window_center_pos, 'pos', duration=500)
            # current page animation
            size_anim = self.animate(self.window, self.default_size, self.min_size, 'size', duration=500)

            self.startParallelAnimation(pos_anim, size_anim)
