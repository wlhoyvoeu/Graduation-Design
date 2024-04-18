#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 引用包
import random
import Rose.code.TextSimilarityMeasure as TextSimilarityMeasure
import Rose.code.NgramSegment as Ngram
# 类
class Packet:
    """数据包类"""
    def __init__(self):
        self.index = 0                  # 该数据包的在数据集中的索引
        self.bytelen = 0                # 该数据包的字节长度
        self.content = []
class RecombPacket:
    """重组数据包类"""
    def __init__(self):
        self.packetnums = 0             # 该重组包由几条数据包组成
        self.packetindex = []           # 该重组包由哪几条数据包组成
        self.content = []               # 该重组包的内容
class Field:
    """字段类"""
    def __init__(self,field):
        """初始化字段的属性"""
        self.content = field
        self.offset = 0
        self.bytelen = len(field) // 2

    def update_offset(self,newoffset):
        """将字段的偏移量设置为指定的值"""
        self.offset = newoffset
# 函数
def Recomb_Packet(FieldSegment:list)->list:
    '''
    :param FieldSegment:每条packet的字段处理结果
    :return: 返回重组的packet的字段处理结果
    '''
    recomb_info = []            # 记录每条重组包的信息，重组包有几条
    L = len(FieldSegment)
    i = 0
    while(i < L):
        index = []              # 记录该重组包是哪几条数据包组合在一起
        rand = random.randint(2,4)
        count = 0
        pi = ''
        while(count < rand and i < L):
            pi += FieldSegment[i].strip()
            index.append(i)
            count += 1
            i += 1

        pi = pi.split(',')
        pi = pi[:-1]
        recomb_packet = RecombPacket()
        recomb_packet.packetnums = count
        recomb_packet.packetindex = index
        recomb_packet.content = pi
        recomb_info.append(recomb_packet)
    return recomb_info
def Cal_Fieldoffset(index:int,data:list)->int:
    """
    根据字段在数据包中的索引计算偏移量
    :param index: 字段在数据包的索引
    :param data: 数据包
    :return: 返回字段的偏移量
    """
    offset = 0
    for i in range(0,index):
        offset += len(data[i])
    offset = offset // 2
    return  offset
def FieldExpress(recomb:list)->list:
    """
    记录重组包中各字段的属性
    :param recomb:
    :return: 返回数据包中各字段，type：list
    """
    recomb_fieldsclass = []
    for i in range(len(recomb)):
        unit_recomb = recomb[i].content
        mid = []
        index_list = list(enumerate(unit_recomb)) # 将字段与索引组成元组，并将其加入列表
        for j in range(len(unit_recomb)):
            f = unit_recomb[j]
            f = Field(f)
            index = index_list[j][0]
            newoffset = Cal_Fieldoffset(index, unit_recomb)
            f.update_offset(newoffset)
            mid.append(f)
        recomb_fieldsclass.append(mid)
    return recomb_fieldsclass
def PacketLen(packet:list)->int:
    """
    计算数据包的长度
    :param packet: 列表元素为划分后的各个字段
    :return: 该数据包的字节长度
    """
    midlen = 0
    for i in range(len(packet)):
        midlen += len(packet[i])
    midlen = midlen // 2
    return midlen
def PacketsList(FieldSegment:list)->list:
    """
    :param FieldSegment:文件读取后的数据包的字段划分结果 ,列表元素为字符串形式的字段划分结果
    :return:数据包列表，其中字段为列表元素
    """
    packets_lists = []
    for i in range(len(FieldSegment)):
        pi = FieldSegment[i]
        pi = pi.split(',')
        pi = pi[0:-1]
        packets_lists.append(pi)
    return packets_lists
def PacketsExpress(packets_list:list)->list:
    """
    记录每条数据包的属性：索引和字节长度
    :param FieldSegment: 文件读取后的数据包的字段划分结果 ,列表元素为字符串形式的字段划分结果
    :return: 返回包含每个数据包类实例的列表
    """
    packetclass_list = []
    # for j in range(len(FieldSegment)):
    #     packets_list = PacketsList(FieldSegment[j])
    for i in range(len(packets_list)):
        unit = packets_list[i]
        packetlen = PacketLen(packets_list[i])
        packet = Packet()
        packet.index = i
        packet.bytelen = packetlen
        packet.content = unit
        packetclass_list.append(packet)
    return packetclass_list
def FieldSimilarity(field1:Field,field2:Field)->int:
    """
    计算两个字段的文本相似度
    :param field1:
    :param field2:
    :return: 返回文本相似度
    """
    return TextSimilarityMeasure.TSM(field1,field2)
def NW_Cluster(recombfield:list)->list:
    """
    计算数据包各字段的初始聚类质心
    :param recombfield: 数据包的字段划分结果，列表元素为划分出的各个字段
    :return: 返回初始质心
    """
    mid_recombfield = []
    for i in range(len(recombfield)):
        mid_recombfield.append(recombfield[i])
    centroids = []                                  # 存放各个聚类的质心
    initial_centroid = random.choice(mid_recombfield)   # 随机选择一个字段作为初始聚类中心
    similar_dict = {}                               # 相似度字典，key是与质心比较的字段，value是两者的相似度
    # fields_cluster = []                             # 字段聚类
    end = True                                      # 循环开关，初始化为True
    while end:
        for i in range(len(mid_recombfield)):
            similar_dict[mid_recombfield[i]] = FieldSimilarity(initial_centroid.content,mid_recombfield[i].content)
            max_similarity = similar_dict[max(similar_dict,key=similar_dict.get)]
            min_similarity = similar_dict[min(similar_dict,key=similar_dict.get)]
        d_similar = (max_similarity + min_similarity) / 2   # 计算相似值d_similar

        for key,value in similar_dict.items():              # 序列相似度大于d_similar的样本归于一类，并从样本集中删除
            if value >= d_similar:
                # fields_cluster.append(key)
                mid_recombfield.pop(mid_recombfield.index(key))

        centroids.append(initial_centroid)
        new_centroid = min(similar_dict,key=similar_dict.get)   # 将与聚类中心相似度最小的点作为新质心
        initial_centroid = new_centroid
        if len(mid_recombfield) == 0:
            end = False
        similar_dict = {}
    return centroids
def Kmeans(single_recombfield:list)->list:
    """
    对每条数据包的字段划分结果聚类，输出多个聚类
    :param single_recombfield: 数据包的字段划分结果，列表元素是划分出的每个字段
    :return: 输出多个聚类，列表元素是聚类
    """
    end = True                  # 循环结束标记
    while end:
        fields_cluster = []     # 列表元素是聚类，每个聚类存放相似的字段
        # new_centroids = []      # 列表元素是质心
        field_similarity = 0    #
        sum_similarity = []     # 统计同一簇内的字段与簇质心的相似度
        count = 0
        centroids = NW_Cluster(single_recombfield)     # 获取初始质心
        k = len(centroids)      # 获取簇的数量
        for i in range(k):
            fields_cluster.append([])
            # new_centroids.append(0)
        for member in single_recombfield:
            max_similarity = -100000
            cluster_index = 0   # 簇的索引
            for centroidindex, centroid in enumerate(centroids):    # 将字段与每个质心比较，和谁的相似度最大，该字段归谁
                mid_similarity = FieldSimilarity(member.content,centroid.content)
                if mid_similarity > max_similarity:
                    max_similarity = mid_similarity
                    cluster_index = centroidindex
            fields_cluster[cluster_index].append(member)
        for i in range(k):
            for j in fields_cluster[i]:
                field_similarity += FieldSimilarity(j.content,centroids[i].content)
            sum_similarity.append(field_similarity)
        # for i in range(len(sum_similarity)):
        #     tmp = abs((sum_similarity[i % len(sum_similarity)] / sum_similarity[(i+1) % len(sum_similarity)] + 1e-9)-1)
        #     if tmp <= 10:
        #         count += 1
        m = 0
        while(m < len(sum_similarity)-1):
            tmp = abs((sum_similarity[m] / sum_similarity[m+1] + 1e-9)-1)   # sum_similarity[i]是簇内相似度的分值总和
            if tmp <= 10:
                count += 1
            m += 1
        if count == len(sum_similarity)-1:
            end = False
    return fields_cluster
def FieldClustering(recomb_fields):
    """
    输出整个文件的字段聚类
    :param recomb_fields: 所有重组包的字段划分结果
    :return:
    """
    recomb_cluster = []
    for i in range(len(recomb_fields)):
        single_recombfield = recomb_fields[i]
        single_recombfield_clusters = Kmeans(single_recombfield)
        recomb_cluster.append(single_recombfield_clusters)
    return recomb_cluster
def PacketOffset(recomb_cluster:list)->int and list:
    """
    输入数据集的字段聚类，输出数据集的最大频率偏移量差值
    :param recomb_cluster:
    :return: 最大频率偏移量差值
    """
    offsetdiff_freq = {}                                           # 偏移量差值字典，key:偏移量差值，value:偏移量差值出现次数
    recomb_offsetdiff = []                                         # 偏移量插值列表，记录每条重组包的偏移量差值
    recomb_offsetdiffdic = []                                      # 记录每条重组包中产生偏移量差值及其字段组合，key为偏移量差值，value为字段组合[{},{},{}]

    for i in range(len(recomb_cluster)):                           # i：每条重组包的聚类
        recomb_offsetdiff.append([])
        # recomb_offsetdiffdic.append([])
        unit_cluster = recomb_cluster[i]
        mid_dic = {}
        for j in range(len(unit_cluster)):                         # j: 每个重组包聚类中的每个聚类
            count = len(unit_cluster[j])                           # 每个聚类内的字段数量
            while (count > 1):
                for k in range(count - 1):
                    offsetdiff = unit_cluster[j][count-1].offset - unit_cluster[j][k].offset
                    if offsetdiff not in mid_dic:
                        mid_dic[offsetdiff] = []
                    mid_dic[offsetdiff].append(tuple([unit_cluster[j][k],unit_cluster[j][count-1]]))
                    recomb_offsetdiff[i].append(offsetdiff)

                    if offsetdiff not in offsetdiff_freq.keys():        # 若字典中为含有该偏移量差值，则加入字典，否则value+1
                        offsetdiff_freq[offsetdiff] = 1
                    else:
                        offsetdiff_freq[offsetdiff] += 1
                count -= 1
        recomb_offsetdiffdic.append(mid_dic)
    print('偏移量差值字典：')
    print(offsetdiff_freq)
    sortdict = sorted(offsetdiff_freq.items(),key=lambda x:x[1],reverse=True)   # 将偏移量差值按出现次数从大到小排序
    p = 0
    end = True
    while(p < len(sortdict) and end):
        maxfreq_offsetdiff = sortdict[p][0]
        if maxfreq_offsetdiff > 4:      # 最大偏移差值起码要大于长度字段的长度
            end = False
        p += 1

    # maxfreq_offsetdiff = max(offsetdiff_freq, key=lambda x: offsetdiff_freq[x])
    return maxfreq_offsetdiff,recomb_offsetdiff,recomb_offsetdiffdic
def Maxoffsetdif_PacketIndex(maxfreq_offdif:int,recomb:list,recomb_offsetdiff:list)->list:
    """
    确定具有最大频率偏移量差值的重组包索引,并以列表形式返回
    :param maxfreq_offdif: 最大频率偏移量差值
    :param recomb: 重组包
    :param recomb_offsetdiff: 记录每条重组包存在的偏移量差值
    :return: 索引列表
    """
    maxfreq_offdif_packetindex = []
    for i in range(len(recomb)):
        if maxfreq_offdif in recomb_offsetdiff[i]:
            maxfreq_offdif_packetindex.append(i)
    return maxfreq_offdif_packetindex
def MaxFreq_fieldcomb(maxfreq_offdif_packetindex:list,recomb_cluster:list,maxfreq_offdif:int)->tuple:
    """
    根据最大频率偏移量差值确定分割字段组合，并返回其中出现频率最高的字段组合
    :param maxfreq_offdif_packetindex: 含有最大频率偏移量差值的重组包索引表
    :param recomb_cluster: 重组包的字段聚类
    :param maxfreq_offdif: 最大频率偏移量差值
    :return: 最大频率分割字段
    """
    freq_fieldcomb = {}             # 记录可以得出最大频率偏移量差值的字段组合，value：出现次数
    for i in range(len(maxfreq_offdif_packetindex)):            # 每个数据包
        unit_recombcluster = recomb_cluster[maxfreq_offdif_packetindex[i]]
        for j in range(len(unit_recombcluster)):                # 每个字段聚类
            count = len(unit_recombcluster[j])                  # 每个聚类内的字段数量
            while (count > 1):
                for k in range(count - 1):
                    offsetdiff = unit_recombcluster[j][count - 1].offset - unit_recombcluster[j][k].offset
                    if offsetdiff == maxfreq_offdif:
                        fieldcomb = tuple([unit_recombcluster[j][k].content,unit_recombcluster[j][count - 1].content])
                        if fieldcomb not in freq_fieldcomb.keys():
                            freq_fieldcomb[fieldcomb] = 1
                        else:
                            freq_fieldcomb[fieldcomb] += 1
                count -= 1
    sortdict = sorted(freq_fieldcomb.items(), key=lambda x: x[1],reverse = True)  # 将字典按value值从大到小排序 输出类型为列表，列表内元素类型为元组
    print('分割字段组合字典：')
    print(sortdict)
    end = True
    p = 0
    while(p < len(sortdict) and end):
        maxfreq_fieldcomb = sortdict[p][0]
        if len(sortdict[p][0][1]) >= 30 or len(sortdict[p][0][0]) >= 30:       # '00' 填充字节无意义
            end = True
        else:
            end = False
        p += 1

    return maxfreq_fieldcomb,sortdict
def InferredPacketlen(recomb_fields:list,fix_field:str,gap_num)->dict:
    """
    根据固定字段推断重组包中单包长度
    :param recomb_fields:重组包字段聚类
    :param fix_field:固定字段
    :return: 返回字典，key是重组包的索引，value是重组包中含有的单包的包长
    """
    extract_packetlen = {}
    extract_packetlen1 = {}                 # 重组包中分割字段的偏移量
    for i in range(len(recomb_fields)):
        unit_recomb = recomb_fields[i]
        t = []
        for p in range(len(unit_recomb)):
            t.append(unit_recomb[p].content)
        if t.count(fix_field)>=2:
            mid = []
            mid1 = []
            packet_len = []
            for j in range(len(unit_recomb)):
                if unit_recomb[j].content == fix_field:
                    mid.append(unit_recomb[j])          # 提取重组包中的固定字段
                    mid1.append(unit_recomb[j].offset)

            # for m in range(len(mid)):                           # 计算重组包中的单包长度
            #     if m+1 <= len(mid) - 1:
            #         packet_len.append(abs(mid[m].offset - mid[m+1].offset))
            try:
                packet_len.append(mid1[0+gap_num+1]-mid1[0])    # 只取第一条包的长度
            except IndexError:
                continue
            else:
                extract_packetlen[i] = packet_len               # 将重组包索引与推测长度组成字典
                extract_packetlen1[i] = mid1
    return extract_packetlen,extract_packetlen1
def InferredPacketlen1(maxfreq_offdif_packetindex,maxfreq_offdif,recomb_fields:list,fix_field:str)->dict:

    extract_packetlen = {}                  #重组包中的单包长度
    extract_packetlen1 = {}                 # 重组包中分割字段的偏移量
    for index in maxfreq_offdif_packetindex:
        unit_recomb = recomb_fields[index]
        field = []
        # 记录与固定字段相等的
        for i in range(len(unit_recomb)):
            if unit_recomb[i].content == fix_field:
                field.append(unit_recomb[i])
        # 记录与最大频率偏移差值相等的分割字段组合，且该重组包的第一个包长要等于最大频率偏移差值
        # for j in range(len(field)-1):
        #     offset = abs(field[j].offset - field[j+1].offset)
        #     if offset == maxfreq_offdif:


    for i in range(len(recomb_fields)):
        unit_recomb = recomb_fields[i]
        mid = []
        mid1 = []
        packet_len = []
        for j in range(len(unit_recomb)):
            if unit_recomb[j].content == fix_field:
                mid.append(unit_recomb[j])          # 提取重组包中的固定字段
                mid1.append(unit_recomb[j].offset)

        for m in range(len(mid)):                           # 计算重组包中的单包长度
            if m+1 <= len(mid) - 1:
                packet_len.append(abs(mid[m].offset - mid[m+1].offset))

        if len(packet_len) > 1:
            extract_packetlen[i] = packet_len               # 将重组包索引与推测长度组成字典
            extract_packetlen1[i] = mid1
    return extract_packetlen,extract_packetlen1
def RealPacketlen(extract_packetlen:dict,recomb:list,packets:list)->dict:
    """
    根据所推测出的重组包的索引，得到其组成的相应单包索引，并计算各自真实长度
    :param extract_packetlen: 可以推测出包长的重组包字典
    :param recomb: 重组包数据集
    :param packets: 单包数据集
    :return: 返回真实单包长度
    """
    real_packetlen = {}
    key_list = list(extract_packetlen.keys())
    for key in key_list:
        packetlen = []
        packet_index = recomb[key].packetindex
        for i in range(len(packet_index)):
            packetlen.append(packets[packet_index[i]].bytelen)
        real_packetlen[key] = packetlen
    return real_packetlen
def InferPacketlenAcc(real_len:list,infer_packetlen:list)->float:
    """
    与真实包长作比较，计算推测包长的准确率
    :param real_len:
    :param infer_packetlen:
    :return:
    """
    count = 0
    for i in range(len(infer_packetlen)):
        if real_len[i] - infer_packetlen[i] ==0:
            count += 1
    acc = count / len(real_len)
    return acc
def FilterFixfield(maxfreq_fieldcomb:tuple,sortdict: list, recomb_fields: list, recomb: list, packets: list):
    """
    根据排序后的字典进行筛选，条件是组合内的字段是一样的；其相减得到的包长数量小于重组包内真实单包包长数量；
    :param sortdict:
    :param recomb_fields:
    :param recomb:
    :param packets:
    :return: 返回字段组合
    """
    end = True
    while (end):
        for i in range(len(sortdict)):
            count = 0
            if sortdict[i][0][0] == sortdict[i][0][1]:
                fix_field = sortdict[i][0][0]
                extract_packetlen,extract_packetlen1 = InferredPacketlen(recomb_fields, fix_field)  # type :dict
                real_packetlen = RealPacketlen(extract_packetlen, recomb, packets)  # type:dict
                key_list = list(extract_packetlen.keys())
                for key in key_list:
                    index = recomb[key].packetindex
                    if len(extract_packetlen1[key]) == len(real_packetlen[key]):
                        count += 1
                if count == len(extract_packetlen):
                    end = False
                    newmaxfreq_fieldcomb = sortdict[i][0]
                    break
        if end != False:        # 若没找到，则依旧使用原来的字段组合
            newmaxfreq_fieldcomb = maxfreq_fieldcomb
            end = False
    return newmaxfreq_fieldcomb
def PacketIndex(extract_packetlen:dict,recomb:list)->list:
    """
    根据重组包中提取出的包长和数量，计算相应的单包索引
    :param extract_packetlen: 可以提取出包长的重组包，key为重组包的索引，value是该重组包提取出来的单包长度
    :return:
    """
    recomb_index = list(extract_packetlen.keys())    # 记录提取出包长的重组包的索引,并以列表形式存储
    # print('提取出包长的重组包的索引',recomb_index)
    packet_index = []                                # 记录推测包长对应的单包索引
    # for i in range(len(recomb_index)):
    #     mid = recomb[recomb_index[i]].packetindex    # 重组包中的单包索引
    #     value = extract_packetlen[recomb_index[i]]   # 重组包中提取出的单包长的数量
    #
    #     # 从第一条数据包开始算
    #     for j in range(len(value)):
    #         packet_index.append(mid[j])

    for i in range(len(recomb_index)):
        mid = recomb[recomb_index[i]].packetindex    # 重组包中的单包索引
        packet_index.append(mid[0])                  # 只取第一条单包的索引
    return packet_index

def FieldComb_gap(sortdict:list,maxfreq_offdif_packetindex:list,recomb_offsetdiffdic,maxfreq_offdif):
    process = True
    field = 0
    gapdic_list = []
    while(process and field < len(sortdict)):
        maxfreq_fieldcomb = sortdict[field][0]
        fieldoffset_comb = []
        for i in range(len(maxfreq_offdif_packetindex)):
            unit_recomb = recomb_offsetdiffdic[maxfreq_offdif_packetindex[i]]
            value = unit_recomb[maxfreq_offdif]        # 取得出最大频率偏移量差值的字段组合
            temp = []
            for j in range(len(value)):
                if value[j][0].content == maxfreq_fieldcomb[0] and value[j][1].content == maxfreq_fieldcomb[1]:
                    temp.append(tuple([value[j][0].offset,value[j][1].offset]))
            fieldoffset_comb.append(sorted(temp,key=lambda x:x[0]))
        while [] in fieldoffset_comb:
            fieldoffset_comb.remove([])
        gap_dic = {}
        for i in range(len(fieldoffset_comb)):
            unit_list = fieldoffset_comb[i]
            tup = unit_list[0]
            temp = []
            for j in range(len(unit_list)):
                temp.append(unit_list[j][0])
                temp.append(unit_list[j][1])
            temp = sorted(temp)
            fieldgap = temp.index(tup[1]) - temp.index(tup[0]) - 1
            if fieldgap not in gap_dic.keys():
                gap_dic[fieldgap] = 1
            else:
                gap_dic[fieldgap] += 1
        gapdic_list.append(sorted(gap_dic.items(),key= lambda x:x[1],reverse=True))
        if len(gap_dic) == 1:           # 若间隔种类只有一种则选取该间隔
            # if gap_dic[gap] == len(fieldoffset_comb):
            gap_num = fieldgap
            process = False
        else:                           # 若间隔长度种类有多种，则重新选取分割字段
            field += 1
    if process == True:                 # 若循环一圈后找不到合适的，直接取第一个字段组合
        maxfreq_fieldcomb = sortdict[0][0]
        gap_num = gapdic_list[0][0][0]
    return gap_num,maxfreq_fieldcomb

def MessageSegment(file,ran:int,gap:int)->list:
    """
    根据输入的文件地址，输出分割的数据包内容与相应的包长
    :param file:文件地址
    :param ran: 起始索引
    :param gap: 间隔的数据包数量
    :return: 返回分割的数据包内容和相应的包长
    """
    # 读取字段划分的文件
    # FieldSegment_File = 'D:\Thesis Information\拆包处理\Web_extend1000.txt'
    FieldSegment_File = file
    with open(FieldSegment_File) as FS:
        FieldSegment = FS.readlines()
    # FieldSegment = FieldSegment[0:100]
    FieldSegment = FieldSegment[ran:ran+gap]
    print(FieldSegment[0])
    print(FieldSegment[1])
    # 对每条重组前的packet的属性进行记录
    packets_list = PacketsList(FieldSegment)            # 将字符串形式的字段划分结果转为列表形式
    packets = PacketsExpress(packets_list)              # [<class.packet>,...,<class.packet>]
    # print('单包的数量：',len(packets))

    # 进行packet的重组
    recomb = Recomb_Packet(FieldSegment)                # [<class.recombpacket>,...,<class.recombpacket>]
    # print("重组包的数量：",len(recomb))

    # 对每条重组后的packet的字段进行属性记录
    recomb_fields = FieldExpress(recomb)                # [[<class.field>,...,<class.field>],...,[<class.field>,...,<class.field>]]
    # print("重组包的数量：",len(recomb_fields))

    # 进行字段聚类
    recomb_cluster = FieldClustering(recomb_fields)     # [[[],[],[]] ,..., [[],[],[]]]
    # print("总聚类的数量",len(recomb_cluster))

    # 计算最大频率偏移量差值
    maxfreq_offdif,recomb_offsetdiff,recomb_offsetdiffdic = PacketOffset(recomb_cluster)     # recomb_offsetdiff 记录每条重组包的各种偏移量插值
    print('最大频率偏移量差值：',maxfreq_offdif)

    # 根据最大偏移量差值回溯数据包得到固定字段

    # 确定具有最大偏移量差值的重组包索引
    maxfreq_offdif_packetindex = Maxoffsetdif_PacketIndex(maxfreq_offdif,recomb,recomb_offsetdiff)
    print('具有最大偏移量差值的重组包索引表：',maxfreq_offdif_packetindex)

    # fields = []
    # for i in range(len(maxfreq_offdif_packetindex)):
    #     unit_offsetdiffdic = recomb_offsetdiffdic[maxfreq_offdif_packetindex[i]]
    #     temp = unit_offsetdiffdic[maxfreq_offdif]
    #     fields.append(sorted(temp,key=lambda x:x[0]))





    # 确定分割出最大频率偏移量差值的字段组合
    maxfreq_fieldcomb,sortdict = MaxFreq_fieldcomb(maxfreq_offdif_packetindex,recomb_cluster,maxfreq_offdif)
    print('最大频率分割字段：')
    print(maxfreq_fieldcomb)

    gap_num,maxfreq_fieldcomb = FieldComb_gap(sortdict,maxfreq_offdif_packetindex,recomb_offsetdiffdic,maxfreq_offdif)
    print("更新后的分割字段")
    print(maxfreq_fieldcomb)
    print('字段间隔距离')
    print(gap_num)
    # 根据字段组合确定可提取的重组包的单包长度
    fix_field = maxfreq_fieldcomb[0]
    extract_packetlen,extract_packetlen1 = InferredPacketlen(recomb_fields,fix_field,gap_num)
    print('提取包中分割字段的偏移量：')
    print(extract_packetlen1)
    print('提取包长结果：')
    print(extract_packetlen)

    # 对应可提取的重组包中真实的单包长度
    real_packetlen = RealPacketlen(extract_packetlen,recomb,packets)
    real_len = []  # 记录对应推测包长的真实包长
    for key in extract_packetlen.keys():
        infer_value = extract_packetlen[key]
        real_value = real_packetlen[key]
        # real_len.extend(real_value[0:0+len(infer_value)])   # 从重组包中的第一条单包算起
        real_len.append(real_value[0])                      # 只取第一条包
        # real_len.extend(real_value[1:1+len(infer_value)])   # 从重组包中的第二条单包算起
    print('真实包长结果')
    print(real_packetlen)
    print(real_len)
    print(len(real_len))

    # 提取推测的包长
    infer_packetlen = []                             # 记录推测的包长，并以列表形式存储
    for key in extract_packetlen.keys():
        # infer_packetlen.extend(extract_packetlen[key])    # 提取所有推测的包长
        infer_packetlen.append(extract_packetlen[key][0]) # 只提取第一个包长

    # 真实的第一条包

    # 提取真实单包的索引
    packet_index = PacketIndex(extract_packetlen,recomb)
    # print('提取出了包长的单包的索引')
    # print(packet_index)

    packet_content = []                 # 记录提取出了包长的单包的字段分割结果
    for i in range(len(packet_index)):
        packet_content.append(packets[packet_index[i]].content)

    acc = InferPacketlenAcc(real_len,infer_packetlen)
    print("推断包长准确率：")
    print(acc)
    return packet_content,infer_packetlen


