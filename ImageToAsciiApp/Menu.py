import os
import sys

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from AnimationProperties import WindowAnimator

class CustomMenu(QWidget):
    def __init__(self, parent=None, trackWidget=None, runtimeEventManager=None):
        QWidget.__init__(self)

        self.parent = parent            # parent widget
        self.trackWidget = trackWidget  # the widget which enables this menu
        self.evtManager = runtimeEventManager   # runtime event manager function
        self.size = [120, 150]

        # load the UI
        self.ui = uic.loadUi('menuUI.ui', self)
        # set the parent
        self.setParent(parent)

        # animator object
        self.animator = WindowAnimator(self)

        # call event manager function
        self.list.itemClicked.connect(self.callRuntimeEventManager)

        # hide it by default
        self.hide()

    # show or hide
    def showOrHide(self, status):
        if status is True:
            self.show_()
        else:
            self.hide_()

    # set size
    def setSize(self, width=100, height=150):
        self.size = [width, height]

    # show the menu
    def show_(self):
        # get tracker widget size
        size = [self.trackWidget.size().width(), self.trackWidget.size().height()]
        # get tracker widget position
        pos = [self.trackWidget.pos().x()+5, self.trackWidget.pos().y()+size[1]+1]

        # size animation
        size_anim = self.animator.animate(self, (self.size[0], 0), self.size, 'size', duration=400, return_=True)
        # position animation
        pos_anim = self.animator.animate(self, (pos[0], pos[1]-40), pos, 'pos', duration=400, return_=True)

        # start parallel animation
        self.animator.startParallelAnimation(size_anim, pos_anim)

        # make the menu visible
        self.show()

        # call event manager
        self.callRuntimeEventManager('show', hide=False)

    # hide the menu
    def hide_(self):
        # get tracker widget position
        pos = [self.pos().x(), self.pos().y()]

        # size animation
        size_anim = self.animator.animate(self, self.size, (self.size[0], 0), 'size', duration=400, return_=True)
        # position animation
        pos_anim = self.animator.animate(self, pos, (pos[0], pos[1]-40), 'pos', duration=400, return_=True)

        # animation finishing task
        size_anim.finished.connect(lambda: self.hide())

        # start parallel animation
        self.animator.startParallelAnimation(size_anim, pos_anim)

        # call event manager
        self.callRuntimeEventManager('hide', hide=False)

    # add item
    def addItem(self, item, clearAll=True):
        if clearAll:
            self.list.clear()
            
        self.list.addItem(item)

    # add items
    def addItems(self, items, clearAll=True):
        if clearAll:
            self.list.clear()
            
        self.list.addItems(items)

    # set event manager function
    def setRuntimeEventManager(self, func):
        if callable(func):
            self.evtManager = func

    # call event manager function
    def callRuntimeEventManager(self, data, hide=True):
        if callable(self.evtManager):
            self.evtManager.__call__(data)

        # hide menu
        if hide:
            self.hide_()
