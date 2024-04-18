#!/usr/bin/python
# -*- coding: UTF-8 -*-

def LCS(s1:str,s2:str)->str:
    """
    计算两个字符串的连续最大公共子字符串
    :param s1:字符串1
    :param s2:字符串2
    :return:最大公共子字符串
    """
    size1 = len(s1) + 1
    size2 = len(s2) + 1
    chess = [[["",0] for j in list(range(size2))] for i in list(range(size1))]
    for i in list(range(1,size1)):
        chess[i][0][0] = s1[i-1]
    for j in list(range(1,size2)):
        chess[0][j][0] = s2[j-1]
    for i in list(range(1, size1)):
        for j in list(range(1, size2)):
            if s1[i - 1] == s2[j - 1]:
                chess[i][j] = ['↖', chess[i - 1][j - 1][1] + 1]
            elif chess[i][j - 1][1] > chess[i - 1][j][1]:
                chess[i][j] = ['←', chess[i][j - 1][1]]
            else:
                chess[i][j] = ['↑', chess[i - 1][j][1]]
    i = size1 - 1
    j = size2 - 1
    s3 = []
    while i > 0 and j > 0:
        if chess[i][j][0] == '↖':
            s3.append(chess[i][0][0])
            i -= 1
            j -= 1
        if chess[i][j][0] == '←':
            j -= 1
        if chess[i][j][0] == '↑':
            i -= 1
    s3.reverse()
    return ''.join(s3)

def Levenshtein_Distance(str1:str,str2:str)->int:
    """
    动态规划计算两个字符串间的编辑距离
    :param str1:
    :param str2:
    :return:
    """
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if (str1[i - 1] == str2[j - 1] and abs(len(str1) - len(str2)) < 4):
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)
    return matrix[len(str1)][len(str2)]
def str_inx(word_, string_):
    return [i for i in range(len(string_)) if string_[i] == word_]
def ab_max_inx(s_a, s_b):
    i, len_a, len_b = 0, len(s_a), len(s_b)
    while len_a > i and len_b > i and s_a[i] == s_b[i]:
        i += 1
    return i
def common_substr(s_a, s_b):
    """
    两个字符串的所有公共子串，包含长度为1的
    :param s_a:
    :param s_b:
    :return:
    """
    res = []
    if s_a:
        a0_inx_in_b = str_inx(s_a[0], s_b)
        if a0_inx_in_b:
            b_end_inx, a_end_inx = -1, 0
            for inx in a0_inx_in_b:
                if b_end_inx > inx:
                    continue
                this_inx = ab_max_inx(s_a, s_b[inx:])
                a_end_inx = max(a_end_inx, this_inx)
                res.append(s_a[:this_inx])
                b_end_inx = this_inx + inx
            res += common_substr(s_a[a_end_inx:], s_b)
        else:
            res += common_substr(s_a[1:], s_b)
    return res
def CCI(S):
    count = 0
    for i in range(len(S)):
        count += len(S[i])
    return count
def TSM(string_a:str,string_b:str):
    """
    计算字符串间的文本相似度
    :param string_a:
    :param string_b:
    :return:
    """
    a_len = len(string_a)
    b_len = len(string_b)
    ab_Lcs_len = len(LCS(string_a,string_b))
    p = 1 - 2 * ab_Lcs_len/(a_len + b_len + 1e-9)
    common_substrings = common_substr(string_a,string_b)
    q = 2 * p * CCI(common_substrings)/(a_len + b_len + 1e-9)
    ed_len = Levenshtein_Distance(string_a,string_b)
    u = ab_Lcs_len + (max(a_len,b_len) - ed_len)
    tsm = u + q
    return tsm


if __name__ == '__main__':
    pass
