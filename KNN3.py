# -*- coding:utf-8 -*-
from numpy import *
import operator
import time
from os import listdir

#knn实现
def classify(inputPoint,dataSet,labels,k):
    '''
    inputPoint:待判断的点
    dataSet:数据集合
    labels:标签向量，维数和dataSet行数相同，比如labels[1]代表dataSet[1]的类别
    k:邻居数目
    输出：inputPoint的标签
    '''
    dataSetSize = dataSet.shape[0]     
    # 先用tile函数将输入点拓展成与训练集相同维数的矩阵，再计算欧氏距离
    diffMat = tile(inputPoint,(dataSetSize,1))-dataSet  
    sqDiffMat = diffMat ** 2                   
    # 计算每一行元素之和
    sqDistances = sqDiffMat.sum(axis=1)         
    # 开方得到欧拉距离矩阵
    distances = sqDistances ** 0.5              
    # argsort返回的是数组从小到大的元素的索引
    # 按distances中元素进行升序排序后得到的对应下标的列表
    sortedDistIndicies = distances.argsort()    
    # 选择距离最小的k个点，统计每个类别的点的个数
    classCount = {}
    for i in range(k):
        voteIlabel = labels[ sortedDistIndicies[i] ]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    # 按classCount字典的第2个元素（即类别出现的次数）从大到小排序
    sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

# 将图片矩阵转换为向量
def img2vector(filename):
    '''
    filename:文件名字
    将这个文件的所有数据按照顺序写成一个一维向量并返回
    '''
    returnVect = []
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline() 
        for j in range(32):
            returnVect.append(int(lineStr[j]))
    return returnVect

# 从文件名中解析分类数字
def classnumCut(fileName):
    '''
    filename:文件名
    返回这个文件数据代表的实际数字
    '''
    fileStr = fileName.split('.')[0]
    classNumStr = int(fileStr.split('_')[0])
    return classNumStr

# 构建训练集数据向量及对应分类标签向量
def trainingDataSet():
    '''
    从trainingDigits文件夹下面读取所有数据文件，返回：
    trainingMat：所有训练数据，每一行代表一个数据文件中的内容
    hwLabels：每一项表示traningMat中对应项的数据到底代表数字几
    '''
    hwLabels = []
    # 获取目录traningDigits内容(即数据集文件名)，并储存在一个list中
    trainingFileList = listdir('trainingDigits')   
    m = len(trainingFileList) #当前目录文件数
    # 初始化m维向量的训练集，每个向量1024维
    trainingMat = zeros((m,1024))                  
    for i in range(m):
        fileNameStr = trainingFileList[i]
        # 从文件名中解析分类数字，作为分类标签
        hwLabels.append(classnumCut(fileNameStr))  
        # 将图片矩阵转换为向量并储存在新的矩阵中
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    return hwLabels,trainingMat

def createDataSet():
    '''
    从trainingDigits文件夹下面读取所有数据文件，返回：
    trainingMat：所有训练数据，每一行代表一个数据文件中的内容
    hwLabels：每一项表示traningMat中对应项的数据到底代表数字几
    '''
    hwLabels = []
    # 获取目录traningDigits内容(即数据集文件名)，并储存在一个list中
    trainingFileList = listdir('trainingDigits')   
    m = len(trainingFileList)   #当前目录文件数
    # 初始化m维向量的训练集，每个向量1024维
    trainingMat = zeros((m,1024))                  
    for i in range(m):
        fileNameStr = trainingFileList[i]
        # 从文件名中解析分类数字，作为分类标签
        hwLabels.append(classnumCut(fileNameStr))  
        # 将图片矩阵转换为向量并储存在新的矩阵中
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    return trainingMat,hwLabels

# 测试函数
def handwritingTest():
   
    # 构建训练集
    hwLabels,trainingMat = trainingDataSet()    
    #从testDigits里面拿到测试集
    testFileList = listdir('testDigits')
    # 错误数
    errorCount = 0.0                           
    # 测试集总样本数
    mTest = len(testFileList)                  
    # 获取程序运行到此处的时间（开始测试）
    t1 = time.time()
    for i in range(mTest):
        # 得到当前文件名
        fileNameStr = testFileList[i]
        # 从文件名中解析分类数字
        classNumStr = classnumCut(fileNameStr)  
        # 将图片矩阵转换为向量
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)  
        # 调用knn算法进行测试
        classifierResult = classify(vectorUnderTest, trainingMat, hwLabels, 5)
        print ("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        # 预测结果不一致，则错误数+1
        if (classifierResult != classNumStr): errorCount += 1.0      
    print( "\nthe total number of tests is: %d" % mTest)               
    print ("the total number of errors is: %d" % errorCount )          
    print ("the total error rate is: %f" % (errorCount/float(mTest)))  
    # 获取程序运行到此处的时间（结束测试）
    t2 = time.time()
    # 测试耗时
    print ("Cost time: %.2fmin, %.4fs."%((t2-t1)//60,(t2-t1)%60) )     

if __name__ == "__main__":
    handwritingTest()
