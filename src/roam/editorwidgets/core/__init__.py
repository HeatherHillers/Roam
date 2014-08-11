from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QObject, pyqtSignal
from collections import OrderedDict


widgets = OrderedDict()

class EditorWidgetException(Exception):
    pass

def registerwidgets(*widgetclasses):
    for widgetclass in widgetclasses:
        widgets[widgetclass.widgettype] = widgetclass

def registerallwidgets():
    from roam.editorwidgets.imagewidget import ImageWidget
    from roam.editorwidgets.listwidget import ListWidget, MultiList
    from roam.editorwidgets.checkboxwidget import CheckboxWidget
    from roam.editorwidgets.datewidget import DateWidget
    from roam.editorwidgets.numberwidget import NumberWidget, DoubleNumberWidget
    from roam.editorwidgets.textwidget import TextWidget, TextBlockWidget
    from roam.editorwidgets.tablewidget import TableWidget
    from roam.editorwidgets.optionwidget import OptionWidget
    registerwidgets(ImageWidget, ListWidget, MultiList, CheckboxWidget, DateWidget,
                    NumberWidget, DoubleNumberWidget, TextWidget, TextBlockWidget, OptionWidget)

def supportedwidgets():
    return widgets.keys()

def widgetwrapper(widgettype, widget, config, layer, label, field, parent=None):
    try:
        editorwidget = widgets[widgettype]
    except KeyError:
        raise EditorWidgetException("No widget wrapper for type {} was found".format(widgettype))

    widgetwrapper = editorwidget.for_widget(widget, layer, label, field, parent)
    widgetwrapper.initWidget(widget)
    widgetwrapper.config = config
    return widgetwrapper


def createwidget(widgettype, parent=None):
    try:
        wrapper = widgets[widgettype]
    except KeyError:
        raise EditorWidgetException("No widget wrapper for type {} was found".format(widgettype))

    return wrapper.createwidget(parent=parent)


class EditorWidget(QObject):
    validationupdate = pyqtSignal(object, bool)
    valuechanged = pyqtSignal(object)

    # Signal to emit when you need to show a large widget in the UI.
    largewidgetrequest = pyqtSignal(object, object, object, dict)

    def __init__(self, widget=None, layer=None, label=None, field=None, parent=None, *args, **kwargs):
        super(EditorWidget, self).__init__(parent)
        self._config = {}
        self.widget = widget
        self.layer = layer
        self.field = field
        self.label = label
        self.required = False
        self._readonly = True
        self.validationstyle = """QLabel[required=true]
                                {border-radius: 5px; background-color: rgba(255, 221, 48,150);}
                                QLabel[ok=true]
                                { border-radius: 5px; background-color: rgba(200, 255, 197, 150); }"""
        self.validationupdate.connect(self.updatecontrolstate)
        self.initconfig = kwargs.get('initconfig', {})

    @classmethod
    def for_widget(cls, widget, layer, label, field, parent, *args, **kwargs):
        """
        Create a new editor wrapper for the given widget.
        """
        editor = cls(widget, layer, label, field, parent, *args, **kwargs)
        return editor

    @classmethod
    def createwidget(cls, parent=None, config=None):
        """
        Creates the widget that wrapper supports.
        """
        if not config:
            config = {}
        try:
            return cls(initconfig=config).createWidget(parent)
        except TypeError as ex:
            print ex
            return cls().createWidget(parent)

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self.setEnabled(not value)

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        self._hidden = value
        self.widget.setVisible(not value)
        self.buddywidget.setVisible(not value)

    def raisevalidationupdate(self, passed):
        if self.required:
            self.validationupdate.emit(self.field, passed)

    def updatecontrolstate(self, field, passed):
        if self.required:
            self.buddywidget.setProperty('ok', passed)
            self.buddywidget.style().unpolish(self.buddywidget)
            self.buddywidget.style().polish(self.buddywidget)

    def setrequired(self):
        self.buddywidget.setStyleSheet(self.validationstyle)
        self.buddywidget.setProperty('required', True)
        self.required = True

    @property
    def buddywidget(self):
        if not self.label is None:
            return self.label
        else:
            return self.widget

    @property
    def labeltext(self):
        if self.label is None:
            return self.widget.objectName()
        else:
            return self.label.text()

    def setvalue(self, value):
        pass

    def value(self):
        pass

    def validate(self, *args):
        pass

    def setconfig(self, config):
        """
        Alias function for self.config so we can connect it to a signal.
        """
        self.config = config

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value
        self.updatefromconfig()

    def updatefromconfig(self):
        """
        Called when the config of the widget changes.

        When overloading you should call this base class function
        in order to save the current value before updating from the config.

        Your overloaded method should call endupdatefromconfig in order
        to restore the last value.
        """
        self._lastvalue = self.value()

    def endupdatefromconfig(self):
        self.setvalue(self._lastvalue)

    def createWidget(self, parent):
        pass

    def initWidget(self, widget):
        pass

    def setEnabled(self, enabled):
        if not self.widget is None:
            self.widget.setEnabled(enabled)

    def emitvaluechanged(self, *args):
        """
        Emit the value changed signal.
        :param args: Ignored.  Just a sink so we can connect it to any signal.
        :return:
        """
        self.valuechanged.emit(self.value())

class RejectedException(Exception):
    WARNING = 1
    ERROR = 2

    def __init__(self, message, level=WARNING):
        super(RejectedException, self).__init__(message)
        self.level = level

class LargeEditorWidget(EditorWidget):
    """
    A large editor widget will take up all the UI before the action is finished.
    These can be used to show things like camera capture, drawing pads, etc

    The only thing this class has extra is a finished signal and emits that once input is complete.
    """
    finished = pyqtSignal(object)
    cancel = pyqtSignal(object, int)

    def emitfished(self):
        self.finished.emit(self.value())

    def emitcancel(self, reason=None, level=1):
        self.cancel.emit(reason, level)

    def before_load(self):
        pass
