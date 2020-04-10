# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget

from Ui_layout_demo_LayoutManage import Ui_MainWindow
from ChildrenForm import Ui_ChirldrenForm


class ChildrenForm(QWidget, Ui_ChirldrenForm):
    def __init__(self):
        super(ChildrenForm, self).__init__()
        self.setupUi(self)


class LayoutDemo(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(LayoutDemo, self).__init__(parent)
        self.setupUi(self)

        # 生成子窗口实例
        # self.child = ChildrenForm()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        print('利润:', self.doubleSpinBox.text())
        # self.childshow()
    #
    # def childshow(self):
    #     # 显示子窗口(将子窗口放到父窗口中的珊格区域)
    #     self.MaingridLayout.addWidget(self.child)
    #     self.child.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = LayoutDemo()
    ui.show()
    sys.exit(app.exec_())