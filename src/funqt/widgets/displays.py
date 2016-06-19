from funqt import QtCore, QtGui, LayoutMixin, HBoxLayout, VBoxLayout, qcreate


class Spacer(QtGui.QSpacerItem):
    def __init__(self, mode="horizontal"):
        args = [None, None, None, None]
        if mode == "horizontal":

            args[0] = 20
            args[1] = 10
            args[2] = QtGui.QSizePolicy.Expanding
            args[3] = QtGui.QSizePolicy.Minimum
        elif mode == "vertical":
            args[0] = 20
            args[1] = 10
            args[2] = QtGui.QSizePolicy.Minimum
            args[3] = QtGui.QSizePolicy.Expanding

        super(Spacer, self).__init__(*args)


class SeparatorLine(QtGui.QFrame):
    def __init__(self, mode="horizontal"):
        super(SeparatorLine, self).__init__()
        if mode == 'horizontal':
            self.setFrameShape(QtGui.QFrame.HLine)
        elif mode == 'vertical':
            self.setFrameShape(QtGui.QFrame.VLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


class Splitter(QtGui.QSplitter, LayoutMixin):
    def __init__(self, mode="horizontal"):
        if mode == "horizontal":
            orient = QtCore.Qt.Horizontal
        elif mode == "vertical":
            orient = QtCore.Qt.Vertical
        else:
            orient = QtCore.Qt.Horizontal

        super(Splitter,self).__init__(orient)

        self.setStyleSheet('''QSplitter::handle:horizontal{border: 1px outset darkgrey;};QSplitter::handle:vertical{border: 1px outset darkgrey;}''')


class TabLayout(QtGui.QTabWidget, LayoutMixin):
    def addWidget(self, widget):
        self.addTab(widget, widget.title)


class TabWidget(QtGui.QWidget):
    def __init__(self, title=""):
        super(TabWidget, self).__init__()
        self.title = title


class FrameLayout(QtGui.QWidget, LayoutMixin):
    """ referenced from https://github.com/By0ute/pyqt-collapsable-widget
    """
    def __init__(self, parent=None, title=None):
        super(FrameLayout, self).__init__(parent)

        self._titleText = title
        self._isCollapsed = True
        self._titleFrame = None
        self._content = None

        self._initUI()
        self._connectSignals()

    def _initUI(self):
        self._main_v_layout = VBoxLayout(self)
        with self._main_v_layout:
            self._titleFrame = qcreate(self.TitleFrame,title=self._titleText,collapsed=self._isCollapsed)
            self._content = qcreate(QtGui.QWidget,layoutType=VBoxLayout)
            self._content.setVisible(not self._isCollapsed)

    def _connectSignals(self):
        self._titleFrame.clicked.connect(self.toggleCollapsed)

    def addWidget(self, widget):
        self._content.layout.addWidget(widget)

    def toggleCollapsed(self):
        self._content.setVisible(self._isCollapsed)
        self._isCollapsed = not self._isCollapsed
        self._titleFrame.arrow.setArrow(int(self._isCollapsed))

    class TitleFrame(QtGui.QFrame):
        clicked = QtCore.Signal()

        def __init__(self, parent=None, title="", collapsed=False):
            super(FrameLayout.TitleFrame,self).__init__(parent)
            self._titleText = title
            self._collapsed = collapsed

            self._initUI()

        def _initUI(self):
            self.setMinimumHeight(24)
            self.move(QtCore.QPoint(24, 0))
            self.setStyleSheet("border:1px solid rgb(41, 41, 41); ")

            self.layout = HBoxLayout(self)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)
            with self.layout:
                self.arrow = qcreate(FrameLayout.Arrow,collapsed=self._collapsed)
                self.arrow.setStyleSheet("border:0px")

                self.title = qcreate(QtGui.QLabel,self._titleText)
                self.title.setMinimumHeight(24)
                self.title.move(QtCore.QPoint(24, 0))
                self.title.setStyleSheet("border:0px")

        def mousePressEvent(self, event):
            self.clicked.emit()
            return super(FrameLayout.TitleFrame, self).mousePressEvent(event)

    class Arrow(QtGui.QFrame):
        def __init__(self, parent=None, collapsed=False):
            super(FrameLayout.Arrow, self).__init__(parent)
            self._collapsed = collapsed
            self._arrow = None
            self._initUI()

        def _initUI(self):
            self.setMaximumSize(24, 24)

            # horizontal == 0
            self._arrow_horizontal = (QtCore.QPointF(7.0, 8.0), QtCore.QPointF(17.0, 8.0), QtCore.QPointF(12.0, 13.0))
            # vertical == 1
            self._arrow_vertical = (QtCore.QPointF(8.0, 7.0), QtCore.QPointF(13.0, 12.0), QtCore.QPointF(8.0, 17.0))
            # arrow
            self._arrow = None
            self.setArrow(int(self._collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_vertical
            else:
                self._arrow = self._arrow_horizontal

        def paintEvent(self, event):
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setBrush(QtGui.QColor(192, 192, 192))
            painter.setPen(QtGui.QColor(64, 64, 64))
            painter.drawPolygon(self._arrow)
            painter.end()
