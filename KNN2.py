from numpy import *
import operator
import time

# 将文本记录转换为NumPy的解析程序
def file2matrix(filename):
    fr = open(filename)
    #得到文件行数
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    #创建返回的Numpy矩阵
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    #解析文件数据到列表
    index = 0
    for line in arrayOfLines:
        line = line.strip() #注释1
        listFromLine = line.split('\t') #注释2
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index +=1
    return returnMat,classLabelVector


# 归一化特征值
def autoNorm(dataSet):
    minVals = dataSet.min(0) 
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals 
    #创建一个与dataSet同大小的零矩阵
    normDataSet = zeros(shape(dataSet)) 
    #数据行数
    m = dataSet.shape[0]           
    #tile()函数将变量内容复制成输入矩阵同等的大小
    normDataSet = dataSet - tile(minVals,(m,1)) 
    #特征值相除
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

# k近邻算法
def classify0(inX,dataSet,labels,k):  
    #inX用于分类的输入向量
    #dataSet输入的训练样本集,
    #labels为标签向量, 
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


# 分类器针对约会网站的测试代码
def datingClassTest():
    #测试样本的比例
    hoRatio = 0.10      
    datingDataMat,datingLabels = file2matrix("datingTestSet2.txt")
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    #测试样本的数量
    numTestVecs = int(m*hoRatio)  
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],
                                     datingLabels[numTestVecs:m],4)
        print("the classifier came back with: %d, the real answer is :%d" %(classifierResult,datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount +=1.0
    print("the total error rate is: %f" % (errorCount/float(numTestVecs)))


def classifyPerson():
    resultList = ['not at all','in small doses','in large doses']
    percentTats = float(input("percentage of time spent playing video games?"))
    ffMiles = float(input("frequent flier miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr - minVals)/ranges,normMat,datingLabels,3)
    print("You will probably like this person:",resultList[classifierResult - 1])
