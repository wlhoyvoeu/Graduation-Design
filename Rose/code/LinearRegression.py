#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 导入的包
from fractions import Fraction as F
import numpy as np
import Rose.code.NgramSegment as Ngram
import Rose.code.MessageSegment as MS
import Rose.code.MessageSegment as msg
import sys


# 函数
def MaxDimension(ngrams:list)->int:
    """
    计算ngram数据集中，最多的gram数
    :param ngrams: ngrams数据集，其中元素是每条包的ngram处理结果
    :return: 返回最多的gram维度
    """
    dimensions = []
    for i in range(len(ngrams)):
        dimensions.append(len(ngrams[i]))
    max_dimension = max(dimensions)
    return max_dimension
def BigEndian(gram:list)->str:
    """
    返回大端模式的字段
    :param gram: 一条数据包的其中的一个gram，列表形式，列表元素是准备拼接在一起的字节序列
    :return: 返回拼接好的且大端模式下的字节序列
    """
    string = ''
    for i in gram:
        string += i
    return string
def LittleEndian(gram:list)->str:
    """
    返回小端模式下的字段
    :param gram: 一条数据包的其中的一个gram，列表形式，列表元素是准备拼接在一起的字节序列
    :return: 返回拼接好的且小端模式下的字节序列
    """
    s = ''
    if gram == ['middle_part']:
        s = 'middle_part'
    else:
        string = ''
        for i in gram:
            string += i
        j = len(string)
        while(j > 0):
            s += string[j-2:j]
            j -= 2
    return s
def HextoDecimal(grams_list:list)->list:
    """
    将十六进制形式的字段转为十进制整数
    :param grams_list: 记录字段形式为十六进制字节序列的列表
    :return: 将列表中的字段转为十进制整数
    """
    decimal = []
    for i in grams_list:
        if i == 'middle_part':
            decimal.append(0)
        else:
            decimal.append(int(i,16))
    return decimal
def PrimaryEquation(ngrams:list,max_gramdimension:int)->list:
    """
    将数据包的字段，数据包包长和截距b组成其次线性方程组
    :param ngrams: 数据包的候选长度字段
    :param infer_len: 数据包的包长
    :param max_gramdimension: ngram的最大维度
    :return: 返回初始方程
    """
    primary_equation = []           # 记录每条数据包的十进制字段。 形式形如[ [f11,f12,...,f1n],...,[fi1,fi2,...,fin],[fm1,fm2,...,fmn] ]
    for i in range(len(ngrams)):    # i: 每条数据包
        grams_list = []              #  存储大端模式或小端模式下的每条数据包的gram字段,列表元素是字段的字符串形式
        for j in range(len(ngrams[i])): # j 每条数据包的每个gram
            grams_list.append(LittleEndian(ngrams[i][j]))
        while (len(grams_list) != max_gramdimension):
            grams_list.append('00')
        grams_list = HextoDecimal(grams_list)   # 将十六进制字符串形式的列表元素转为十进制整数
        # grams_list.append(infer_len[i])         # 添加数据包的长度
        # grams_list.append(1)                    # 添加截距，初始值为1
        primary_equation.append(grams_list)
    return primary_equation
def P1(A, i, j, row=True):              #第一种初等变换
    if row:
        A[[i,j]]=A[[j,i]]               #交换两行
    else:
        A[:,[i,j]]=A[:,[j,i]]           #交换两列
def P2(A,i,k, row=True):				#第二种初等变换
    if row:
        A[i]=k*A[i]						#k乘第i行
    else:
        A[:,i]=k*A[:,i]					#k乘第i列
def P3(A,i,j,k,row=True):               #第三种初等变换
    if row:
        A[j]+=k*A[i]                    #k乘以第i行加到第j行
    else:
        A[:,j]+=k*A[:,i]                #k乘以第i列加到第j列
def simplestLadder(A,rank):
    for i in range(rank-1,0,-1):                #自下而上逐行处理
        for j in range(i-1, -1,-1):             #自下而上将A[i,i]上方元素消零
            P3(A,i,j,-A[j,i])
def rowLadder(A, m, n):
    rank=0                                      #非零行数初始化为0
    zero=m                                      #全零行首行下标
    i=0                                         #当前行号
    order=np.array(range(n))                    #未知量顺序
    while i<min(m,n) and i<zero:                #自上向下处理每一行
        flag=False                              #A[i,i]非零标志初始化为False
        index=np.where(abs(A[i:,i])>1e-10)      #当前列A[i,i]及其以下的非零元素下标
        if len(index[0])>0:                     #存在非零元素
            rank+=1                             #非零行数累加1
            flag=True                           #A[i,i]非零标记
            k=index[0][0]                       #非零元素最小下标
            if k>0:                             #若非第i行
                P1(A,i,i+k)                     #交换第i，k+i行
        else:                                   #A[i:,i]内全为0
            index=np.where(abs(A[i,i:n])>1e-10) #当前行A[i,i:n]的非零元素下标
            if len(index[0])>0:                 #存在非零元素，交换第i，k+i列
                rank+=1
                flag=True
                k=index[0][0]
                P1(A,i,i+k,row=False)           #列交换
                order[[i, k+i]]=order[[k+i, i]] #跟踪未知量顺序
        if flag:                                #A[i,i]不为零，A[i+1:m,i]消零
            P2(A,i,1/A[i,i])
            for t in range(i+1, zero):
                P3(A,i,t,-A[t,i])
            i+=1                                #下一行
        else:                                   #将全零元素行交换到矩阵底部
            P1(A,i,zero-1)
            zero-=1                             #更新全零行首行下标
    return rank, order
def mySolve(A,b):
    m,n=A.shape                                     #系数矩阵结构
    b=b.reshape(b.size, 1)                          #常量列向量
    B=np.hstack((A, b))                             #构造增广矩阵
    r, order=rowLadder(B, m, n)                     #消元
    X=np.array([])                                  #解集初始化为空
    index=np.where(abs(B[:,n])>1e-10)               #常数列非零元下标
    nonhomo=index[0].size>0                         #判断是否非齐次
    r1=r                                            #初始化增广矩阵秩
    if nonhomo:                                     #非齐次
        r1=np.max(index)+1                          #修改增广阵秩
    solvable=(r>=r1)                                #判断是否可解
    if solvable:                                    #若可解
        simplestLadder(B, r)                        #回代
        X=np.vstack((B[:r,n].reshape(r,1),          #特解
                            np.zeros((n-r,1))))
        if r<n:                                     #导出组基础解系
            x1=np.vstack((-B[:r,r:n],np.eye(n-r)))
            X=np.hstack((X,x1))
        X=X[order]
    return X
def DimensionReduction(primary_equation:list,max_gramdimension:int,ngrams:list,infer_len:list)->list:
    """
    对方程筛选，进行简单降维
    :param primary_equation:
    :param max_gramdimension:
    :param ngrams:
    :param infer_len:
    :return: 返回降维后的方程
    """
    right_column = []
    for i in range(max_gramdimension):                  # 方程的第i列
        flag = True
        column_list = []
        for j in range(len(primary_equation)):          # 方程的第j行
            column_list.append(primary_equation[j][i])
        fieldvariety = len(list(set(column_list)))        # 记录第i列字段值的种类数量
        packetlenvariety = len(list(set(infer_len)))      # 记录包长值的种类数量
        if fieldvariety != packetlenvariety:              # 与数据包长种类数量不一致的字段列过滤
            flag = False
        if flag == True:
            right_column.append(i)
    final_equation = []
    for i in range(len(ngrams)):
        row = []
        for j in right_column:
            row.append(primary_equation[i][j])
        row.append(infer_len[i])            # 添加第i包的包长
        row.append(1)                       # 添加截距
        final_equation.append(row)
    return final_equation,right_column


if __name__ == '__main__':
    pass

# 将标准输出重定向到文件
with open('output.txt', 'w') as f:
    # 重定向输出
    sys.stdout = f

    # 输入文件的地址 如下格式
    # file = 'D:\STUN_2000.txt'
    file = '/home/why/workspace/pythonProject/Bfile.txt'

    ran = 0  # 数据集的第i组
    gap = 69  # 每组的数据包数量

    packet_content, infer_len, acc = MS.MessageSegment(file, ran, gap)

    print('进行下一步的包的数量：')
    print(len(packet_content))
    print(len(infer_len))  # 形式为列表，其中列表元素是每条包推测的包长
    print('推测的包长：')
    print(infer_len)
    for member in range(1, 5):
        # 进行ngrams分割
        ngrams = Ngram.ngram_segment(packet_content, member)  # 形式为列表，其中列表元素是每条包的ngram处理结果
        print('ngrams的内容：')
        # for i in range(len(ngrams)):
        #     print(ngrams[i])
        print(ngrams[0])
        print(ngrams[1])

        # 记录最大维度
        max_gramdimension = MaxDimension(ngrams)

        # 建立初始方程
        primary_equation = PrimaryEquation(ngrams,
                                           max_gramdimension)  # 记录每条数据包的十进制字段。 形式形如[ [f11,f12,...,f1n],...,[fi1,fi2,...,fin],[fm1,fm2,...,fmn] ]

        # 降维
        final_equation, right_column = DimensionReduction(primary_equation, max_gramdimension, ngrams, infer_len)
        print("筛选后的列索引(字段偏移量)：")
        print(right_column)
        # temp = []
        # temp1 = []
        # for index in right_column:
        #     temp.append(primary_equation[0][index])
        #     temp1.append(primary_equation[-1][index])
        # print("筛选后的列的内容")
        # print(temp)
        # print(temp1)

        # 解方程
        np.set_printoptions(formatter={'all': lambda x: str(F(x).limit_denominator())})  # 设置输出数据格式 使其输出分数形式的结果
        A = np.array(final_equation, dtype='float')
        constant = []
        for i in range(len(ngrams)):
            constant.append(0)
        constant = np.array(constant)
        X = mySolve(A, constant)
        print('第' + str(member) + 'grams情况：')
        print("方程组的解：")
        print(X)
        print('----------------')

# 恢复标准输出
sys.stdout = sys.__stdout__

