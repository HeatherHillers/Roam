from PyQt4.QtGui import QToolBar, QSizePolicy
from PyQt4.QtCore import Qt, QEvent


class MenuToolbar(QToolBar):
    def __init__(self, parent=None):
        super(MenuToolbar, self).__init__(parent)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        style = self.toolButtonStyle()
        if style == Qt.ToolButtonIconOnly:
            self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        else:
            self.setToolButtonStyle(Qt.ToolButtonIconOnly)

        super(MenuToolbar, self).mouseDoubleClickEvent(*args, **kwargs)


class ProjectToolbar(QToolBar):
    def __init__(self, parent=None):
        super(ProjectToolbar, self).__init__(parent)
        self.setStyleSheet("""QWidget {background-color: rgba(0, 0, 0, 0);}
                           QToolBar { spacing: 3px; background-color: rgba(240, 242, 255, 240);}
                           QToolButton:checked {
                                    color: rgb(91,147,194);
                                    background-color: rgba(240, 242, 255, 255);
                                    } """)
        self.setFloatable(True)
        self.setAllowedAreas(Qt.NoToolBarArea)
        self.parent().installEventFilter(self)

    def showEvent(self, *args, **kwargs):
        self.updatesize()

    def updatesize(self):
        self.move(10, 10)
        self.resize(self.sizeHint().width(), self.sizeHint().height())

    def eventFilter(self, object, event):
        print self.parent()
        if event.type() == QEvent.Resize:
            self.updatesize()

        return False

