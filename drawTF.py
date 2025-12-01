import json
import os

import numpy as np
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt

def TrainModel():
    global model
    # 1、获取tensorflow手写数字集的对象
    mnist = tf.keras.datasets.mnist

    # 2、获取训练集、测试集
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # 2.1、增加自己的数据集
    jsonPath = './MyDigits.json'
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r') as f:
            jsonDigits = json.load(f)
            # print(x_train[0])
            # 转换数字图片容器的格式
            x_my_train = np.array(jsonDigits[0])
            x_my_train_reshape = x_my_train.reshape(len(jsonDigits[0]), 28, 28)
            print(x_my_train_reshape.shape)
            y_my_train = np.array(jsonDigits[1])
            # 添加至训练集
            x_train = np.concatenate((x_my_train_reshape, x_my_train), axis=0)
            y_train = np.concatenate((y_train, y_my_train), axis=0)

    # 5、建立神经网络模型
    model = tf.keras.models.Sequential([
        # 拉平，维度由28*28 变成一维
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        # 定义神经元个数
        tf.keras.layers.Dense(128, activation='relu'),
        # 设置遗忘率
        tf.keras.layers.Dropout(0.2),
        # 定义最终输出,0~9共计10个输出
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    # 6、模型编译
    model.compile(
        # 选择优化器
        optimizer='adam',
        # 定义模型的损失函数
        loss='sparse_categorical_crossentropy',
        # 定义模型评估
        metrics=['accuracy']
    )

    # 7、训练模型
    # epochs:训练次数
    model.fit(x_train, y_train, epochs=20)

    # 8、验证模型
    print('开始验证模型')
    model.evaluate(x_test, y_test)

def szClassify(lis):
    model = tf.keras.models.load_model('./my_model')
    res = model.predict(tf.reshape(lis, (1, 28, 28)))
    print(f'识别结果：{np.argmax(res)}')
    return np.argmax(res)


# xsImg = Image.open('sz3.png').convert('L')
# # （2）创建28*28的numpy 全零矩阵
# xsImgData = np.zeros((28, 28))
# # （3）遍历图片对象的所有像素点，并获得每个像素点的颜色值，存储到矩阵中
# for i in range(28):
#     for j in range(28):
#         xsImgData[j][i] = 255 - xsImg.getpixel((i, j))
#
#
# plt.imshow(xsImgData, cmap=plt.cm.gray_r)
# plt.show()
# print(szClassify(xsImgData))