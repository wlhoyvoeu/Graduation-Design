#!/usr/bin/python
# -*- coding: UTF-8 -*-

if __name__ == '__main__':
    pass
def fieldjoint(fieldlist:list):
    s = ''
    for i in range(len(fieldlist)):
        s += fieldlist[i]
    return s


def ngram_segment(packets:list,n:int)->list:
    """
    输出值为n的ngrams
    :param packets:数据包
    :param n: value of n
    :return: ngrams
    """
    sep_ngrams = []  # 用于存放不同报文的n-grams列表的大列表
    num = len(packets)
    for i in range(num):
        message = packets[i]
        length = len(message)
        list_ngrams = []  # 每条消息的n-grams
        repeat = length - n + 1  # 循环次数
        for j in range(repeat):
            Pad_list = []
            field = message[j]
            message_ngrams = []  # 存储该报文每个字段的n-grams的小列表
            Message_Byte = len(message[j]) / 2  # 获取当前字段的字节数
            if Message_Byte < n:  # 若当前字段的字节数不满足所需n,就向下一个字段借不足的字节位
                p = j
                left_index = p - 1
                right_index = p + 1
                message_ngrams.append(message[p])  # 先添加当前的字段
                if left_index >= 0:
                    Message_Byte += 1
                    message_ngrams.insert(0, message[left_index][-2:])

                while (Message_Byte < n and right_index < length - 1):
                    patch_length = n - Message_Byte  # 计算所缺少的字节数
                    if len(message[right_index]) / 2 < patch_length:  # 计算下一个字段的字节数是否满足所需的字节数
                        Message_Byte += len(message[right_index]) / 2
                        message_ngrams.append(message[right_index])
                        right_index += 1
                    elif len(message[right_index]) / 2 >= patch_length:  # 若下一字段满足所需字节数，则在该字段上取相应的字节数
                        Message_Byte += patch_length
                        message_ngrams.append(message[right_index][0:int(patch_length * 2)])
            elif Message_Byte == n:
                if n != 1:
                    Pad_list.append(
                        message[j - 1][-2:])  # 应对 STUN中 '00,01,0021,...' 和'00,01,00,4c,...'这两种情况造成的ngarms分割，使长度字段不在同列
                    Pad_list.append(message[j][0:2 * (n - 1)])
                message_ngrams.append(message[j])
            elif Message_Byte > n:
                # if Message_Byte - n == 1 and n != 1:                       # 应对STUN '00,01,000021' 和 '00,01,00,4c,21'的拆分不同
                #     message_ngrams.append(message[j-1][-2:])
                #     message_ngrams.append(message[j][0:2*(n-1)])
                #     # if message_ngrams not in list_ngrams:
                #     # if message_ngrams != list_ngrams[-1]:
                #     list_ngrams.append(message_ngrams)
                #     message_ngrams = []
                #     message_ngrams.append(message[j][0:2*n])
                #     # if message_ngrams not in list_ngrams:
                #     # if message_ngrams != list_ngrams[-1]:
                #     list_ngrams.append(message_ngrams)
                #     message_ngrams = []
                #     message_ngrams.append(message[j][-(2*n):])
                #     # if message_ngrams not in list_ngrams:
                #     # if message_ngrams != list_ngrams[-1]:
                #     list_ngrams.append(message_ngrams)
                message_ngrams = []
                if len(message[j - 1]) == 2 and n != 1:
                    message_ngrams.append(message[j - 1])
                    message_ngrams.append(message[j][0:2 * (n - 1)])
                    # if message_ngrams not in list_ngrams:
                    # if fieldjoint(message_ngrams) != fieldjoint(list_ngrams[-1]):    # 检测当前字段是否已经存在于前一个中
                    if list_ngrams:
                        if message_ngrams != list_ngrams[-1]:
                            list_ngrams.append(message_ngrams)
                    message_ngrams = []
                # 取前一字段的后一个字节和本字段的前ngram-1字节
                message_ngrams.append(message[j - 1][-2:])
                message_ngrams.append(message[j][0:2 * (n - 1)])
                # if fieldjoint(message_ngrams) != fieldjoint(list_ngrams[-1]):        # 检测当前字段是否已经存在于前一个中
                if list_ngrams:
                    if n == 1:
                        if fieldjoint(message_ngrams) != fieldjoint(list_ngrams[-1]):
                            list_ngrams.append(message_ngrams)
                    elif message_ngrams != list_ngrams[-1]:
                        list_ngrams.append(message_ngrams)
                message_ngrams = []
                # 取该字段的前n个字节和后n个字节作备选字段
                message_ngrams.append(message[j][0:2 * n])
                # if message_ngrams not in list_ngrams:
                # if message_ngrams != list_ngrams[-1]:
                list_ngrams.append(message_ngrams)
                # 记录该字段前n字节中的后n-1个字节
                if Message_Byte >= 2 * n:
                    gap = n - 1
                    for i in range(gap):
                        message_ngrams = []
                        message_ngrams.append('middle_part')
                        list_ngrams.append(message_ngrams)

                middle_byte = int(Message_Byte - 2 * n)
                for i in range(middle_byte):
                    message_ngrams = []
                    message_ngrams.append('middle_part')  # 长度为一字节
                    list_ngrams.append(message_ngrams)
                # 记录该字段后n字节中的前n-2个字节
                if Message_Byte >= 2 * n:
                    gap = n - 1 - 1
                    for i in range(gap):
                        message_ngrams = []
                        message_ngrams.append('middle_part')
                        list_ngrams.append(message_ngrams)

                message_ngrams = []
                message_ngrams.append(message[j][-(2 * n):])
                # if message_ngrams not in list_ngrams:
                if n == 1:
                    if fieldjoint(message_ngrams) != fieldjoint(list_ngrams[-1]):
                        list_ngrams.append(message_ngrams)
                        message_ngrams = []
                else:
                    list_ngrams.append(message_ngrams)

            # if message_ngrams in list_ngrams:
            #     continue
            if Pad_list != []:
                list_ngrams.append(Pad_list)
            if len(list_ngrams) > 0:
            # #     # if fieldjoint(message_ngrams) == fieldjoint(list_ngrams[-1]):       # 检测当前字段是否已经存在于前一个中
            #     if n == 1:
            #         if fieldjoint(message_ngrams) == fieldjoint(list_ngrams[-1]):
            #             continue
                if n!=1:
                    if message_ngrams == list_ngrams[-1]:
                            continue
                elif n == 1:
                    if message_ngrams == []:
                        continue

            list_ngrams.append(message_ngrams)  # 大列表
        sep_ngrams.append(list_ngrams)
    return sep_ngrams
