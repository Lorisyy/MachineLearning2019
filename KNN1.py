# -*- coding=utf-8 -*-

#导入必要的库
from numpy import *
#函数主要分为几类：对象比较、逻辑比较、算术运算和序列操作
import operator  

#创建简单数据集
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels
    
# k近邻算法
def classify(inX,dataSet,labels,k): 
    # inX用于分类的输入向量 
    # dataSet输入的训练样本集
    # labels为标签向量 
    #k用于选择最近的邻居数目
    
    #计算距离
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1) 
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    
    #选择距离最小的k个点
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) +1 
    #排序
    sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse= True) 
    return sortedClassCount[0][0]
