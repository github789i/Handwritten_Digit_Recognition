import json
import imageio
import numpy as np
from PIL import ImageQt
from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter, \
    QComboBox, QLabel, QSpinBox, QFileDialog

from PyQt5.QtGui import (QPainter, QPen, QFont, QPalette)
import drawTF
from PaintBoard import PaintBoard
import sys
import os
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

class MainWidget(QWidget):

    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData()  # 先初始化数据，再初始化界面
        self.__InitView()

    def __InitData(self):
        '''
                  初始化成员变量
        '''
        self.__paintBoard = PaintBoard(self)
        # 获取颜色列表(字符串类型)
        self.__colorList = QColor.colorNames()

    def __InitView(self):
        '''
                  初始化界面
        '''
        self.setFixedSize(400, 320)
        self.setWindowTitle("手写数字识别")

        # 新建一个水平布局作为本窗体的主布局
        main_layout = QHBoxLayout(self)
        # 设置主布局内边距以及控件间距为10px
        main_layout.setSpacing(10)

        # 在主界面左侧放置画板
        main_layout.addWidget(self.__paintBoard)

        # 新建垂直子布局用于放置按键
        sub_layout = QVBoxLayout()

        # 设置此子布局和内部控件的间距为10px
        sub_layout.setContentsMargins(10, 10, 10, 10)

        self.__btn_Quit = QPushButton("退出")
        self.__btn_Quit.setParent(self)  # 设置父对象为本界面
        self.__btn_Quit.clicked.connect(self.Quit)
        sub_layout.addWidget(self.__btn_Quit)


        #
        # self.__cbtn_Eraser = QCheckBox("  使用橡皮擦")
        # self.__cbtn_Eraser.setParent(self)
        # self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        # sub_layout.addWidget(self.__cbtn_Eraser)

        self.label_classify = QLabel("识别结果：")
        self.label_classify.setFont(QFont("Roman times", 10, QFont.Bold))
        self.label_classify.setParent(self)
        sub_layout.addWidget(self.label_classify)

        self.button_classify = QPushButton("识别")
        self.button_classify.setParent(self)
        self.button_classify.clicked.connect(self.on_btn_classify)
        sub_layout.addWidget(self.button_classify)

        self.__btn_Clear = QPushButton("清空画板")
        self.__btn_Clear.setParent(self)  # 设置父对象为本界面

        # 将按键按下信号与画板清空函数相关联
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear)
        sub_layout.addWidget(self.__btn_Clear)

        splitter = QSplitter(self)  # 占位符
        sub_layout.addWidget(splitter)

        # 下拉框，加入训练集时选择
        self.comboBox_num = QComboBox()
        self.comboBox_num.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.comboBox_num.setParent(self)
        sub_layout.addWidget(self.comboBox_num)

        self.__btn_Save = QPushButton("加入训练集")
        self.__btn_Save.setParent(self)
        self.__btn_Save.clicked.connect(self.on_btn_Save_Clicked)
        # 将按键按下信号与画板清空函数相关联
        self.__btn_Save.clicked.connect(self.__paintBoard.Clear)
        sub_layout.addWidget(self.__btn_Save)

        # self.__label_penThickness = QLabel(self)
        # self.__label_penThickness.setText("画笔粗细")
        # self.__label_penThickness.setFixedHeight(20)
        # sub_layout.addWidget(self.__label_penThickness)
        #
        # self.__spinBox_penThickness = QSpinBox(self)
        # self.__spinBox_penThickness.setMaximum(20)
        # self.__spinBox_penThickness.setMinimum(2)
        # self.__spinBox_penThickness.setValue(10)  # 默认粗细为10
        # self.__spinBox_penThickness.setSingleStep(2)  # 最小变化值为2
        # self.__spinBox_penThickness.valueChanged.connect(
        #     self.on_PenThicknessChange)  # 关联spinBox值变化信号和函数on_PenThicknessChange
        # sub_layout.addWidget(self.__spinBox_penThickness)
        #
        # self.__label_penColor = QLabel(self)
        # self.__label_penColor.setText("画笔颜色")
        # self.__label_penColor.setFixedHeight(20)
        # sub_layout.addWidget(self.__label_penColor)
        #
        # self.__comboBox_penColor = QComboBox(self)
        # self.__fillColorList(self.__comboBox_penColor)  # 用各种颜色填充下拉列表
        # self.__comboBox_penColor.currentIndexChanged.connect(
        #     self.on_PenColorChange)  # 关联下拉列表的当前索引变更信号与函数on_PenColorChange
        # sub_layout.addWidget(self.__comboBox_penColor)

        main_layout.addLayout(sub_layout)  # 将子布局加入主布局


    def __fillColorList(self, comboBox):

        index_black = 0
        index = 0
        for color in self.__colorList:
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70, 20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix), None)
            comboBox.setIconSize(QSize(70, 20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        comboBox.setCurrentIndex(index_black)

    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.ChangePenColor(color_str)

    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)

    def on_btn_Save_Clicked(self):
        # savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        # image = self.__paintBoard.GetContentAsQImage()
        # image.save(savePath[0])

        # 1、准备数据
        image = self.__paintBoard.GetContentAsQImage()
        image_new = ImageQt.fromqimage(image).convert('L').resize((28, 28))
        # 二维数组
        xsImageData = 255 - np.asarray(image_new)
        # 对应数字
        y_train = self.comboBox_num.currentText()
        print(f'当前选择数字：{y_train}')

        # 2、打开本地的Json文件
        jsonPath = './MyDigits.json'
        # 判断json文件是否存在
        jsonDigits = [[], []]
        # (1)存在该文件
        if os.path.exists(jsonPath):
            with open(jsonPath, 'r') as f:
                jsonDigits = json.load(f)
        # （2）不管存在与否，都将图片数据 和 对应数字写入列表
        jsonDigits[0].append(list(xsImageData.ravel()))
        jsonDigits[1].append(int(y_train))
        print(jsonDigits)

        with open(jsonPath, 'w') as f:
            json.dump(jsonDigits, f, cls=MyEncoder)


        # # 保存图片到本地列表
        # savePath_x = './x_train'
        # savePath_y = './y_train'
        # if not os.path.exists(savePath_x):
        #     os.mkdir(savePath_x)
        # if not os.path.exists(savePath_y):
        #     os.mkdir(savePath_y)
        # print(f'保存路径：{savePath_x}')
        # # 追加写入
        # with open(savePath_x+'/x_train.txt', 'a', encoding='utf-8') as file:
        #     file.write(str(x_train) + "\n")
        #     file.close()
        # with open(savePath_y + '/y_train.txt', 'a', encoding='utf-8') as file:
        #     file.write(str(y_train) + "\n")
        #     file.close()


        print('加入成功！！！')


    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.EraserMode = True  # 进入橡皮擦模式
        else:
            self.__paintBoard.EraserMode = False  # 退出橡皮擦模式

    def on_btn_classify(self):
        print('识别')
        image = self.__paintBoard.GetContentAsQImage()
        image_new = ImageQt.fromqimage(image).convert('L').resize((28, 28))

        image_new = 255 - np.asarray(image_new)

        # 可视化显示图片
        plt.imshow(image_new, cmap=plt.cm.gray_r)
        plt.show()

        res = drawTF.szClassify(image_new)
        self.label_classify.setText('识别结果：'+str(res))

        return res

    def Quit(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWidget = MainWidget()  # 新建一个主界面
    mainWidget.show()  # 显示主界面

    exit(app.exec_())  # 进入消息循环