# 功能接口
import tkinter as tk
from tkinter import filedialog
from scapy.all import *
from io import StringIO
import Rose.code.NgramSegment as Ngram
import Rose.code.MessageSegment as MS
import Rose.code.LinearRegression as LR
import numpy as np
from fractions import Fraction as F

# 感觉可以将所有的控件，都放在一个列表中一并传入？？？
# 其实该函数的所有功能基本都可以静态，因为不依赖实例
# 后期可以将str_config抽象出来，写入另一个文件中config


class Function:

    def __init__(self):
        # 列表的初始化有点特别，当然可以直接[]，但是为了后续方便操作，我们这样初始化
        """
            list_config[0]--->抓取数据包的数量
            list_config[1]--->数据包的保存路径
            list_config[2]--->选择数据包路径
            list_config[3]--->处理结果的保存路径
            list_config[4]--->数据库的路径
        """
        self.list_config = [-1, '', '', '', '']   # 配置以列表的形式存储
        self.content_default = None
        self.content_current = None
        self.text_display = None

    """设置text的功能"""
    def set_text(self, text_display):
        self.text_display = text_display

    def set_content(self, content_default):
        """
            概述：设置text内容
            参数：默认内容（其他内容都可，后期要改，这样有误解）
            细节：设置默认内容的同时，保存当前内容
        """
        self.content_default = content_default
        self.content_current = self.content_default

    def display_text(self):
        """
            概述：展示text内容
        """

        ''' '''
        self.text_display.delete('1.0', 'end')
        self.text_display.insert('1.0', self.content_current)

    """抓取数据包所需的功能"""
    @staticmethod
    def save_file(entry_path):
        """
            概述：保存文件
            参数：关于用户选择路径的entry控件
        """
        directory = os.getcwd()  # 当前工作的绝对路径
        # linux和windows中的路径斜杠好像有点不同
        dir_path = directory + '/data'
        print(dir_path)
        file_path = filedialog.asksaveasfilename(
            initialdir=dir_path,
            title="保存文件",
            filetypes=(("pcap files", "*.pcap"), ("result files", "*.txt"), ("All files", "*.*")),
            defaultextension=''
        )
        if file_path:
            entry_path.delete(0, tk.END)  # 清空文本框内容
            entry_path.insert(0, file_path)  # 将选中的文件路径插入文本框

    @staticmethod
    def select_file(entry_path):
        """
            概述：选择文件
            参数：关于用户选择路径的entry控件
        """
        directory = os.getcwd()  # 当前工作的绝对路径
        # linux和windows中的路径斜杠好像有点不同
        dir_path = directory + '/data'
        print("保存路径：", dir_path)
        file_path = filedialog.askopenfilename(
            initialdir=dir_path,
            title="选择数据包",
            filetypes=(("pcap files", "*.pcap"), ("database files", "*.db"), ("All files", "*.*"))
        )
        if file_path:
            entry_path.delete(0, tk.END)  # 清空文本框内容
            entry_path.insert(0, file_path)  # 将选中的文件路径插入文本框

    @staticmethod
    def select_file_root(root, entry_path):
        """
            概述：选择文件
            参数：参数1：根窗口
                参数2：关于用户选择路径的entry控件
            细节：因为上述选择文件全部都是在root中执行的，所以无需指定
                但是应为使用的过多修改起来太麻烦，在此直接写个新方法
                这里和java略有区别，不能直接更改参数，重写函数
        """
        directory = os.getcwd()  # 当前工作的绝对路径
        # linux和windows中的路径斜杠好像有点不同
        dir_path = directory + '/data'
        print("保存路径：", dir_path)
        file_path = filedialog.askopenfilename(
            parent=root,
            initialdir=dir_path,
            title="选择数据包",
            filetypes=(("pcap files", "*.pcap"), ("database files", "*.db"), ("All files", "*.*"))
        )
        if file_path:
            entry_path.delete(0, tk.END)  # 清空文本框内容
            entry_path.insert(0, file_path)  # 将选中的文件路径插入文本框

    def save_config(self, num, entry_text):
        """
            概述：保存配置
            细节：将获取两个输入框的内容，并保存
        """
        if num:# num!=0
            self.list_config[num] = entry_text.get()
        else:
            self.list_config[num] = int(entry_text.get())

        print(self.list_config[num])


    def grasp_data(self):
        """
            概述：抓取数据包
            细节；按照entry_num设置的数量抓取，将结果保存只entry_path中
        """

        def packet_callback(packet):
            """
                综述：定义回调函数，处理捕获到的数据包
                细节：将抓取到的数据包转换成pcap文件格式，并保存到设定好的文件目录中
                返回值：成功与否
            """
            try:
                # 将抓取到的数据包转换成pcap格式
                wrpcap(self.list_config[1], packet, append=True)
                # 将输出结果展示到控制台上
                print("展示捕获到的数据包：")
                packet.show()
                return True
            except Scapy_Exception as e:
                print("处理数据包时出现异常：", e)
                return False

        try:
            # 使用用户输入的数量
            packets = sniff(prn=packet_callback, count=self.list_config[0])
        except Scapy_Exception as e:
            print("抓取数据包出现问题", e)
        else:
            # 创建一个 StringIO 对象来捕获输出
            string_buffer = StringIO()
            # 将标准输出重定向到 StringIO 对象
            sys.stdout = string_buffer
            # 执行 packet.show() 并输出结果
            for packet in packets:
                packet.show()
            # 恢复标准输出
            sys.stdout = sys.__stdout__
            # 从 StringIO 对象中获取捕获的输出并转换为字符串
            output_str = string_buffer.getvalue()
            str_tmp = "成功抓取数据包\n" + output_str[:256]
            self.set_content(str_tmp)
            self.display_text()

    def handle_data(self):
        """
            概述：处理解析数据包
            细节：包括预处理数据，和算法处理
        """

        def extract_colored_text(file_path):
            """
                概述：删除颜色字段并划分
                详情：用于处理nemesys.py工具的输出结果，将字段以颜色划分的同时，删除颜色代码并用逗号隔开
                返回值：字符串
            """
            with open(file_path, 'r') as file:
                # 读取文件内容并将其转换为字符串
                file_content = file.read()
                # file_content = "\033[38;5;1m这是带有颜色代码的文本\033[0m"
                # 正则表达式匹配颜色代码
                color_pattern_end = re.compile(r'\x1b\[0m')
                color_pattern_start = re.compile(r'\x1b\[[\d:]*m')
                # 使用 sub 方法将颜色代码替换为空字符串
                file_content = color_pattern_end.sub(',', file_content)
                file_content = color_pattern_start.sub('', file_content)

                # 这里只是当时为了测试数据用的，后期可以注释掉
                print("查看前几位二进制数字:")
                for char in file_content[:20]:
                    # 将字符转换为ASCII码，然后再转换为16进制
                    hex_value = hex(ord(char))
                    print(hex_value, end=' ')
                # print(hex(ord(file_content[:2])))
                print("删除完颜色代码的数据" + file_content)
                return file_content

        def preprocessing():
            """
                概述：预处理数据包
                细节：第一步nemesys工具输出带颜色字段的数据
                    第二部按照颜色字段划分数据
            """
            # 该操作比较耗时，创建等待窗口处理
            # show_waiting_window()

            directory = os.getcwd()  # 当前工作的绝对路径
            # 使用中转的colordata前需要清空文件
            color_path = directory + '/data/nemesysOutData/colordata.txt'
            with open(color_path, 'w') as f:
                f.truncate(0)
            # 利用脚本命令启动预处理工具，但是感觉这样处理并不好
            # command = 'python3 nemesys-master/src/nemesys.py '+path_global  这里的命令需要有一个空格注意！！！
            # list_config[2]--->选择预处理文件路径
            command = 'python3 nemesys-master/src/nemesys.py ' + self.list_config[2]
            print("选取的文件路径：", self.list_config[2])
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # 获取命令执行的输出
            output, error = process.communicate()
            # 打印命令执行结果
            if output:
                # 成功执行
                print("成功预处理文件：（颜色字段）")
                print(output.decode('utf-8', errors='ignore'))
                # 使用默认相对；路径即可
                file_path_color = 'data/nemesysOutData/colordata.txt'
                without_color = extract_colored_text(file_path_color)
                file_path_Bfile = 'data/nemesysOutData/Bfile.txt'
                # 将没有颜色的字段写入二进制文件中
                with open(file_path_Bfile, 'w') as file:
                    file.write(without_color)

                # 将结果输出到text文本中
                # 设置右上角文本内容
                default_text = "解析成功：\n" + "部分输出结果如下：\n" + output.decode('utf-8', errors='ignore')[:256]
                self.set_content(default_text)
                self.display_text()

            if error:
                print("错误信息：")
                print(error.decode('utf-8', errors='ignore'))
            else:
                print("启动预处理脚本命令出现问题")
                print("可能的原因：windows系统不适用，请使用linux系统")

        def run_LinearRegression():
            """
                概述：用于启动算法
                详情：需要LinearRegression的支持,
                    该函数的运行结果将不会在控制台展示，因为我们重定义了输出
                    后续应该使其能在控制台展示，以提高代码的可维护性
                返回值：文件路径(输出结果)
            """
            directory = os.getcwd()  # 当前工作的绝对路径
            print("当前的工作路径：", directory)
            file_path = self.list_config[3]
            # 将标准输出重定向到文件
            with open(file_path, 'w') as f:
                # 重定向输出
                sys.stdout = f
                # 输入文件的地址 如下格式
                # file = 'D:\STUN_2000.txt'
                # file = '/home/why/workspace/pythonProject/Bfile.txt'
                # file = path_global  # 'data/Binary/Bfile_int.txt'
                file = directory + '/data/nemesysOutData/Bfile.txt'

                ran = 0  # 数据集的第i组
                gap = 50  # 每组的数据包数量

                print("输出结果将存放在：", file_path)
                print('最大长度提取算法输出结果')

                packet_content, infer_len = MS.MessageSegment(file, ran, gap)

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
                    max_gramdimension = LR.MaxDimension(ngrams)

                    # 建立初始方程
                    primary_equation = LR.PrimaryEquation(ngrams,
                                                          max_gramdimension)  # 记录每条数据包的十进制字段。 形式形如[ [f11,f12,...,f1n],...,[fi1,fi2,...,fin],[fm1,fm2,...,fmn] ]

                    # 降维
                    final_equation, right_column = LR.DimensionReduction(primary_equation, max_gramdimension, ngrams,
                                                                         infer_len)
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
                    np.set_printoptions(
                        formatter={'all': lambda x: str(F(x).limit_denominator())})  # 设置输出数据格式 使其输出分数形式的结果
                    A = np.array(final_equation, dtype='float')
                    constant = []
                    for i in range(len(ngrams)):
                        constant.append(0)
                    constant = np.array(constant)
                    X = LR.mySolve(A, constant)
                    print('第' + str(member) + 'grams情况：')
                    print("方程组的解：")
                    print(X)
                    print('----------------')
            # 恢复标准输出
            sys.stdout = sys.__stdout__

            # 改变函数间传递的全局路径
            # path_global = file_path
            return file_path

        def output_result(file_path):
            """
                概述：将Rose算法结果输出到text中
            """
            with open(file_path, 'r') as file:
                out_result = file.read()
                print("注意该结果应为重定向的缘故，保存到文件中了，不会在控制台输出")
                self.set_content(out_result)
                self.display_text()
                # 顺带将结果输出到数据库中
                # 无需顺带了，反正输出都有文件，数据库到时候直接连接文件即可

        preprocessing()
        file_path = run_LinearRegression()
        output_result(file_path)

    def database_function(self):
        """
            概述：详情见sqlite.function
        """
        pass



