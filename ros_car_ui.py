import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import paramiko


class WorkThread(QThread):
    """
    使用 pyqtsignalo函数创建信号时,信号可以传递多个参数,并指定信号传递参
    数的类型,参数类型是标准的 Python数据类型(字符串、日期、布尔类型、数字、
    列表、元组和字典)
    """
    # 写在这里是有讲究的,类外也用到了这个trigger
    trigger = pyqtSignal()

    def __int__(self):
        super(WorkThread, self).__init__()

    def run(self):
        os.system(
            "gnome-terminal -x bash -c 'source ~/catkin_ws/devel/setup.bash; roslaunch ros_car_py car_running.launch'"
        )
        # 循环完毕后发出信号
        self.trigger.emit()


class WorkThreadA(QThread):
    trigger = pyqtSignal()

    def __int__(self):
        super(WorkThreadA, self).__init__()
        self.hostname = "192.168.7.2"
        self.port = 22
        self.username = "root"
        self.password = ""
        self.execmd = "python"

    def run(self):
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        s.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
        stdin, stdout, stderr = s.exec_command(self.execmd)
        stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
        # print(stdout.read())
        s.close()
        # 循环完毕后发出信号
        self.trigger.emit()


class WorkThreadB(QThread):
    trigger = pyqtSignal()

    def __int__(self):
        super(WorkThreadB, self).__init__()

    def run(self):
        os.system(
            "gnome-terminal -x bash -c 'source ~/catkin_ws/devel/setup.bash; roslaunch ros_car_py car_gmapping.launch'"
        )
        # 循环完毕后发出信号
        self.trigger.emit()


class WorkThreadC(QThread):
    trigger = pyqtSignal()

    def __int__(self):
        super(WorkThreadC, self).__init__()

    def run(self):
        os.system(
           "gnome-terminal -x bash -c 'source ~/catkin_ws/devel/setup.bash; roslaunch ros_car_py car_navigation.launch'"
        )
        # 循环完毕后发出信号
        self.trigger.emit()


class ThirdWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("小车的速度状态")
        self.resize(600, 300)
        self.center()

        # 实例化指针
        self.pointer = QPixmap()        # 创建一个pixmap对象
        self.pointer.load("./yellow_pin.png")

        # 开一个定时器来进行自动旋转演示
        self.angle = 0
        self.i = 1

        self.change_pix()

        self.timer = QTimer(self)
        self.timer.setInterval(50)  # 50毫秒
        self.timer.timeout.connect(self.timeChange)
        self.timer.start()

    def change_pix(self):
        self.left = {1: './left.png', 2: "./left2.png", 3: './left3.png'}
        self.right = {1: './right.png', 2: "./right2.png", 3: './right3.png'}
        self.up = {1: './up.png', 2: "./up2.png", 3: './up3.png'}
        self.down = {1: './down.png', 2: "./down2.png", 3: './down3.png'}
        self.pix_left = QPixmap(self.left[self.i], "0", Qt.AvoidDither | Qt.ThresholdDither | Qt.ThresholdAlphaDither)
        self.pix_right = QPixmap(self.right[self.i], "0", Qt.AvoidDither | Qt.ThresholdDither | Qt.ThresholdAlphaDither)
        self.pix_up = QPixmap(self.up[self.i], "0", Qt.AvoidDither | Qt.ThresholdDither | Qt.ThresholdAlphaDither)
        self.pix_down = QPixmap(self.down[self.i], "0", Qt.AvoidDither | Qt.ThresholdDither | Qt.ThresholdAlphaDither)

    # 每500毫秒修改paint
    def timeChange(self):
        self.update()
        self.i += 1
        if self.i == 4:
            self.i = 1
        self.change_pix()

    def paintEvent(self, event):
        painter_left = QPainter(self)
        painter_left.drawPixmap(50, 170, self.pix_left.width(), self.pix_left.height(), self.pix_left)
        painter_right = QPainter(self)
        painter_right.drawPixmap(150, 170, self.pix_right.width(), self.pix_right.height(), self.pix_right)
        painter_up = QPainter(self)
        painter_up.drawPixmap(100, 120, self.pix_up.width(), self.pix_up.height(), self.pix_up)
        painter_down = QPainter(self)
        painter_down.drawPixmap(100, 220, self.pix_down.width(), self.pix_down.height(), self.pix_down)

        painter = QPainter(self)
        painter.drawPixmap(0, 0, 300, 113, QPixmap("./forum.png"))
        painter.drawPixmap(300, 0, 300, 113, QPixmap("./forum.png"))
        painter.setRenderHint(QPainter.Antialiasing)    # 绘制图像反锯齿
        self.angle += 1
        if self.angle > 360:
            self.angle = 0
        self.drawspeedPoniter(self.angle)

    def drawspeedPoniter(self, angle):
        painter1 = QPainter(self)
        painter1.setRenderHint(QPainter.Antialiasing)    # 绘制图像反锯齿
        painter1.translate(150, 50)  # 将坐标远点重新放置在表盘中央
        painter1.save()
        painter1.rotate(angle)
        # 计算大小以及坐标
        painter1.drawPixmap(-5.9, -22.5, self.pointer.width()/10, self.pointer.height()/10, self.pointer)
        painter1.restore()

        painter2 = QPainter(self)
        painter2.setRenderHint(QPainter.Antialiasing)    # 绘制图像反锯齿
        painter2.translate(450, 50)  # 将坐标重新放置在窗口中央
        painter2.save()
        painter2.rotate(angle)
        """
        计算好我们的旋转中心，也就是我们的表盘的中心，这个位置不是我们整张图片或者是整个窗口的中心，而是我们表盘的圆心所在坐标
        计算好之后，我们使用translate函数将我们窗口的坐标原点转换为我们的圆心点
        并且将我们指针这张图片的圆心移动到这里，使我们的仪表盘的圆心、窗口坐标原点、以及指针的圆心重合
        """
        painter2.drawPixmap(-5.9, -22.5, self.pointer.width() / 10, self.pointer.height() / 10, self.pointer)
        painter2.restore()

    def closeEvent(self, event):
        # 重写关闭事件，回到第一界面
        self.close()
        event.accept()

    def center(self):
        # 获取屏幕尺寸
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        # move函数是设置窗口的位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class SecondWindow(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setWindowTitle(name)
        self.resize(400, 300)
        # 主窗口居中显示(相对于屏幕)
        self.center()
        self.windowList = []
        layout = QVBoxLayout()

        # 设置中间文本
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label1.setText("1.请先确保ros_car_py包安装成功,并且编译成功")
        self.label1.setAlignment(Qt.AlignTop)
        self.label1.setFont(QFont("Roman times", 12, QFont.Bold))
        self.label2.setText("2.请将Logitech或飞行遥感的usb连接上")
        self.label2.setAlignment(Qt.AlignTop)
        self.label2.setFont(QFont("Roman times", 12, QFont.Bold))
        self.label3.setText("3.请检查各项硬件接线和电源的状态")
        self.label3.setAlignment(Qt.AlignTop)
        self.label3.setFont(QFont("Roman times", 12, QFont.Bold))

        self.button1 = QPushButton("启动服务器")
        self.button2 = QPushButton("启动客户端")
        self.button3 = QPushButton("启动建图")
        self.button4 = QPushButton("启动导航")
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        self.workThread = WorkThread()
        self.workThreada = WorkThreadA()

        self.button1.clicked.connect(self.Communicat_with_terminal)
        self.button2.clicked.connect(self.Communicat_with_client)
        self.button5 = QPushButton("显示小车状态")
        self.button5.clicked.connect(self.show_car_info)
        self.button6 = QPushButton("重新选择")
        self.button6.clicked.connect(self.close)

        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button5)
        layout.addWidget(self.button6)
        self.setLayout(layout)

    def Communicat_with_terminal(self):
        # 终端ros_running开始
        self.workThread.start()
        # 当获得终端任务完毕的信号时，停止计数
        # self.workThread.trigger.connect()

    def Communicat_with_client(self):
        # 服务器终端开始
        self.workThreada.start()
        # 当获得终端任务完毕的信号时，停止计数
        # self.workThread.trigger.connect()

    def closeEvent(self, event):
        # 重写关闭事件，回到第一界面
        the_window = Radiodemo()
        self.windowList.append(the_window)
        self.close()
        the_window.show()
        event.accept()

    def center(self):
        # 获取屏幕尺寸
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        # move函数是设置窗口的位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def show_car_info(self):
        car_velocity = ThirdWindow()
        self.windowList.append(car_velocity)
        car_velocity.show()


class SecondWindowgmapping(SecondWindow):
    def __init__(self, name):
        super().__init__(name)
        self.button3.setEnabled(True)
        self.workThreadb = WorkThreadB()
        self.button3.clicked.connect(self.Communicat_with_map)

    def Communicat_with_map(self):
        self.workThreadb.start()


class SecondWindownavigation(SecondWindow):
    def __init__(self, name):
        super().__init__(name)
        self.button4.setEnabled(True)
        self.workThreadc = WorkThreadC()
        self.button4.clicked.connect(self.Communicat_with_nav)

    def Communicat_with_nav(self):
        self.workThreadc.start()


class Radiodemo(QWidget):
    """两个互斥的按钮"""
    def __init__(self, parent=None):
        super(Radiodemo, self).__init__(parent)
        self.setWindowTitle("ROS")
        self.resize(400, 300)
        # 主窗口居中显示(相对于屏幕)
        self.center()
        self.windowList = []

        layout = QVBoxLayout()

        label1 = QLabel(self)
        label1.setText("请选择您要进行的实验")
        label1.setFont(QFont("Roman times", 15, QFont.Bold))
        label1.setAutoFillBackground(True)
        # 固定方式对齐
        label1.setAlignment(Qt.AlignTop)

        self.btn1 = QRadioButton("TurnAround")
        self.btn2 = QRadioButton("Gmapping")
        self.btn3 = QRadioButton("Navigation")
        self.btn4 = QPushButton("下一步")
        self.btn5 = QPushButton("关闭")

        # 气泡提示信息
        QToolTip.setFont(QFont('SansSerif', 10))  # 字体和大小
        self.btn1.setToolTip('控制小车运动')
        self.btn2.setToolTip('控制小车运动并完成Gmapping建图')
        self.btn3.setToolTip('小车规划路径自动避障运动到目标点')

        self.btn1.setChecked(False)
        self.btn1.toggled.connect(lambda: self.btnstate(self.btn1))

        self.btn2.setChecked(False)
        self.btn2.toggled.connect(lambda: self.btnstate(self.btn2))

        self.btn3.setChecked(False)
        self.btn3.toggled.connect(lambda: self.btnstate(self.btn3))

        self.btn4.clicked.connect(self.nextButtonClick)
        self.btn5.clicked.connect(self.onButtonClick)

        layout.addWidget(label1)
        # #水平居左 垂直居上
        layout.addWidget(self.btn1, 0, Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.btn2, 0, Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.btn3, 0, Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.btn4)
        layout.addWidget(self.btn5)
        self.setLayout(layout)

    def center(self):
        # 获取屏幕尺寸
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        # move函数是设置窗口的位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def btnstate(self, btn):
        if btn.text() == "TurnAround":
            if btn.isChecked():
                print(btn.text() + "将要被执行")
            else:
                print(btn.text() + "被取消")

        if btn.text() == "Gmapping":
            if btn.isChecked():
                print(btn.text() + "将要被执行")
            else:
                print(btn.text() + "被取消")

        if btn.text() == "Navigation":
            if btn.isChecked():
                print(btn.text() + "将要被执行")
            else:
                print(btn.text() + "被取消")

    def nextButtonClick(self):
        if self.btn1.isChecked():
            turn_around_window = SecondWindow("TurnAround")
            self.windowList.append(turn_around_window)
            # 先关闭第一个窗口,视觉上好看
            self.close()
            turn_around_window.show()

        elif self.btn2.isChecked():
            gmapping_window = SecondWindowgmapping("Gmapping")
            self.windowList.append(gmapping_window)
            self.close()
            gmapping_window.show()

        elif self.btn3.isChecked():
            navigation_window = SecondWindownavigation("Navigation")
            self.windowList.append(navigation_window)
            self.close()
            navigation_window.show()

    def onButtonClick(self):
        q = QApplication.instance()
        print("程序关闭!")
        q.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    radioDemo = Radiodemo()
    radioDemo.show()
    sys.exit(app.exec_())

