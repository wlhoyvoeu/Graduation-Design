# This is a sample Python script.
import tkinter as tk
from tkinter import ttk
from scapy.all import *
import subprocess
import sys
from fractions import Fraction as F
import numpy as np
import Rose.code.NgramSegment as Ngram
import Rose.code.MessageSegment as MS
import Rose.code.LinearRegression as LR
import sqlite3
from tkinter import filedialog

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def show_waiting_window():
    """
        概述：创建一个等待窗口
        详情：略
        内涵函数：run_task
        返回值：无
    """
    def run_task():
        """
            概述：创建进度条
            详情：模拟进度条进度
        """
        progress_bar['value'] = 0  # 初始化进度条的值为0
        for i in range(101):
            progress_bar['value'] = i  # 更新进度条的值
            progress_label.config(text=f"任务进度: {i}%")  # 更新进度标签的文本
            root.update()  # 实时更新界面
            time.sleep(0.1)  # 模拟任务执行过程中的延迟

    # 创建一个顶层窗口作为等待窗口
    waiting_window = tk.Toplevel(root)
    waiting_window.title("等待窗口")
    WAITWIDTH = 300
    WAITHEIGHT = 150
    # 获取root窗口信息
    root.update()  # 刷新一下前面的配置
    win_width = root.winfo_width()  # 获取窗口宽度（单位：像素）
    win_height = root.winfo_height()  # 获取窗口高度（单位：像素）
    root_x = root.winfo_x()  # 获取窗口左上角的 x 坐标（单位：像素）
    root_y = root.winfo_y()  # 获取窗口左上角的 y 坐标（单位：像素）
    win_x = (win_width-WAITWIDTH)/2
    win_y = (win_height-WAITHEIGHT)/2
    waiting_window.geometry(f'{WAITWIDTH}x{WAITHEIGHT}+{int(win_x)+int(root_x)}+{int(win_y)+int(root_y)}')

    # 在等待窗口中添加一些文本和进度条
    label = tk.Label(waiting_window, text="请稍等...")
    label.pack(pady=10)
    # 创建任务进度标签
    progress_label = tk.Label(waiting_window, text="任务进度: 0%")
    progress_label.pack()
    # 创建进度条,这里使用不确定进度条参数
    progress_bar = ttk.Progressbar(waiting_window, orient='horizontal', mode='indeterminate')
    progress_bar.pack(fill='y', pady=20)

    # 执行进度条
    run_task()

    # 关闭等待窗口
    waiting_window.destroy()


def temp_path(filepath):
    """
        概述：用于存放临时路径
        作用：便于在不同函数间传递数据
    :return: 临时路径
    """
    return filepath


def get_unique_filename(directory, filename):
    """
        概述：处理相同文件名
    :param directory:
    :param filename:
    :return: 返回新文件名
    """
    base, ext = os.path.splitext(filename)  # 将路径分割成文件名和扩展名
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename


def choose_file():
    """
        概述：选择文件
    :return: 文件路径
    """
    filename = filedialog.askopenfilename()
    return filename




def button_graspData_click(event):
    """
        抓取数据包
        该函数需要管理员权限，因为需要抓取数据包的权限有点高

        因为后续使用的长度提取算法会截取数据包长度
        所以一次性抓取多个数据包没用？？？
        不对，好像会包含在头部，数据包信息会包含在开头
    """

    def packet_callback(packet):
        """
            综述：定义回调函数，处理捕获到的数据包
            细节：将抓取到的数据包转换成pcap文件格式，并保存到设定好的文件目录中
            返回值：成功与否
        """
        try:
            # 将抓取到的数据包转换成pcap格式
            wrpcap(file_path, packet, append=True)
            # 将输出结果展示到控制台上
            print("展示捕获到的数据包：")
            packet.show()
            return True
        except Scapy_Exception as e:
            print("处理数据包时出现异常：", e)
            return False

    if button_graspData.winfo_containing(event.x_root, event.y_root) == button_graspData:
        # 设置pcap文件保存目录
        directory = os.getcwd()  # 当前工作的绝对路径
        dir_path = directory+"/data/pcapFile"
        file_path = filedialog.asksaveasfilename(
            initialdir=dir_path,
            title="保存文件",
            filetypes=(("pcap files", "*.pcap"), ("All files", "*.*")),
            defaultextension=".pcap"
        )
        """这里设置的都是默认路径
        # 获取文件路径和文件名
        directory = os.getcwd()  # 当前工作的绝对路径
        print("查看当前的工作目录：", directory)
        # directory = "/home/why/workspace"
        filename = 'data/pcapFile/captured_packets.pcap'
        unique_filename = get_unique_filename(directory, filename)
        print("Unique filename:", unique_filename)
        # 存放目录
        file_path = os.path.join(directory, unique_filename)
        # 将该目录放入全局路径中，用于下一步预处理
        global path_global
        path_global = file_path"""
        try:
            '''
            好像不需要逐个抓取数据包
            count = 1  # 抓取数据包数量
            i = 0
            while i < count:
                packets = sniff(prn=packet_callback, count=1)  # 捕获10个数据包
                i += 1
            '''
            # 暂时只抓取一个数据包用于测试
            packets = sniff(prn=packet_callback, count=10)
        except Scapy_Exception as e:
            print("抓取数据包出现问题", e)
        else:
            text_display.delete(1.0, "end")     # 清空显示文本框
            text_display.insert(1.0, '成功抓取数据包\n')  # 插入文本内容
            text_display.insert('end', '文件已存储至：'+file_path)


def button_preprocessing_click(event):
    """
        概述：预处理程序
        详情：利用脚本命令启动nemesys工具，将输出结果用extract_colored_text方法处理
        返回值：无需返回值
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
            for char in file_content[:20]:
                # 将字符转换为ASCII码，然后再转换为16进制
                hex_value = hex(ord(char))
                print(hex_value, end=' ')
            # print(hex(ord(file_content[:2])))
            print("删除完颜色代码的数据"+file_content)
            return file_content

    # 释放时，鼠标依旧在按钮上，启动鼠标点击事项
    if button_preprocessing.winfo_containing(event.x_root, event.y_root) == button_preprocessing:
        # 该操作比较耗时，创建等待窗口处理
        show_waiting_window()
        """
        之前用来清空文件的
        # 因为我知道nemesys.py输出的文件路径在哪
        # 又因为打开方式的问题，再这先使用清空文件内容的方式来处理
        # 获取文件路径和文件名
        with open(file_path, 'w') as f:
            f.truncate(0)
        """
        # 利用脚本命令启动预处理工具，但是感觉这样处理并不好
        # 这里使用全局的路径，所以可能会报错，如果没有进行预处理的话
        # command = 'python3 nemesys-master/src/nemesys.py '+path_global  这里的命令需要有一个空格注意！！！
        # command = 'python3 nemesys-master/src/nemesys.py nemesys-master/dns_2000.pcap'
        # 后续还得加一个文件处理事项
        directory = os.getcwd()  # 当前工作的绝对路径
        dir_path = directory + "/data/pcapFile"
        file_path = filedialog.askopenfilename(
            initialdir=dir_path,
            title="选择预处理文件",
            filetypes=(("pcap files", "*.pcap"), ("All files", "*.*"))
        )

        # 使用中转的colordata前需要清空文件
        color_path = directory + '/data/nemesysOutData/colordata.txt'
        with open(color_path, 'w') as f:
            f.truncate(0)

        command = 'python3 nemesys-master/src/nemesys.py '+file_path
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取命令执行的输出
        output, error = process.communicate()

        # 打印命令执行结果
        if output:
            # 成功执行
            print("成功预处理文件：")
            print(output.decode('utf-8', errors='ignore'))

            # 将控制台中输出的彩色字段，按颜色划分，并以逗号相隔
            # 提取颜色文本
            # 不需要选择了，都是预处理的功能，应该放一块
            """# 该文件是包含颜色代码的路径，需要选择
            dir_path_color = directory + "/data/nemesysOutData"
            file_path_color = filedialog.askopenfilename(
                initialdir=dir_path_color,
                title="选择颜色文件",
                filetypes=(("color files", "*.txt"), ("All files", "*.*"))
            )"""
            # 使用默认相对；路径即可
            file_path_color = 'data/nemesysOutData/colordata.txt'
            without_color = extract_colored_text(file_path_color)
            # print(str)
            # 将颜色文本以逗号分隔输出
            # output_text = ','.join(segments)
            dir_path_Bfile = directory + '/data/Binary'
            file_path_Bfile = filedialog.asksaveasfilename(
                initialdir=dir_path_Bfile,
                title="保存二进制文件",
                filetypes=(("Binary files", "*.txt"), ("All files", "*.*")),
                defaultextension='.txt'
            )

            """默认储存位置
            directory = os.getcwd()  # 当前工作的绝对路径
            print("查看当前的工作目录：", directory)
            filename = 'data/Binary/Bfile.txt'
            unique_filename = get_unique_filename(directory, filename)
            print("Unique filename:", unique_filename)
            # 预处理完成后的二进制文件存放目录
            file_path = os.path.join(directory, unique_filename)
            global path_global
            path_global = file_path"""
            with open(file_path_Bfile, 'w') as file:
                file.write(without_color)

            # 将结果输出到text文本中
            text_display.delete('1.0', 'end')
            text_display.insert('1.0', "成功预处理文件：\n文件已存放至:" + file_path_Bfile + '\n')
            str_out = "部分输出结果如下：\n" + output.decode('utf-8', errors='ignore')[:256]
            text_display.insert('end', str_out)
            # text_display.delete('1.0', 'end')

        if error:
            print("错误信息：")
            print(error.decode('utf-8', errors='ignore'))
        '''
        use docker for running nemesys.py
        # 要执行的脚本命令
        command = ('docker run -ti --mount type=bind,source=$(pwd),target=/nemere/ nemere:latest;')  # 这里以执行 'ls -l' 命令为例

        # 使用 subprocess 执行脚本命令
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 等待Docker容器启动
        time.sleep(15)  # 假设容器需要一些时间来启动，这个等待时间可能需要根据你的实际情况调整
        # 运行docker命令
        docker_command = 'ls -al'
        process.stdin.write(docker_command.encode('utf-8'))
        process.stdin.write(b'\n')

        # 获取命令执行的输出
        output, error = process.communicate()

        # 打印命令执行结果
        if output:
            print("命令执行结果：")
            print(output.decode('utf-8', errors='ignore'))
        if error:
            print("错误信息：")
            print(error.decode('utf-8', errors='ignore'))
        '''
    else:
        print("异常信息：鼠标点击不规范")


def run_LinearRegression():
    """
        概述：用于启动算法
        详情：需要LinearRegression的支持,
            该函数的运行结果将不会在控制台展示，因为我们重定义了输出
            后续应该使其能在控制台展示，以提高代码的可维护性
        返回值：文件路径(输出结果)
    """
    directory = os.getcwd()  # 当前工作的绝对路径
    dir_path = directory + '/data/result'
    file_path = filedialog.asksaveasfilename(
        initialdir=dir_path,
        title="保存输出结果",
        filetypes=(("output files", "*.txt"), ("All files", "*.*")),
        defaultextension=".txt"
    )
    """默认路径
    directory = os.getcwd()  # 当前工作的绝对路径
    print("查看当前的工作目录：", directory)
    filename = 'data/result/output.txt'
    unique_filename = get_unique_filename(directory, filename)
    # 预处理完成后的二进制文件存放目录
    file_path = os.path.join(directory, unique_filename)
    print("输出结果路径:", file_path)
    global path_global"""
    # 将标准输出重定向到文件
    with open(file_path, 'w') as f:
        # 重定向输出
        sys.stdout = f

        # 输入文件的地址 如下格式
        # file = 'D:\STUN_2000.txt'
        # file = '/home/why/workspace/pythonProject/Bfile.txt'
        # file = path_global  # 'data/Binary/Bfile_int.txt'
        dir_path = directory + '/data/Binary'
        file = filedialog.askopenfilename(
            initialdir=dir_path,
            title="选择二进制文件",
            filetypes=(("Binary files", "*.txt"), ("All files", "*.*"))
        )
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
            final_equation, right_column = LR.DimensionReduction(primary_equation, max_gramdimension, ngrams, infer_len)
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


def button_outputResult_click(event):
    """
        概述：算法输出结果
        详情：将预处理的数据，通过Rose包下的算法，输出结果
        返回值：无

    """
    if button_outputResult.winfo_containing(event.x_root, event.y_root) == button_outputResult:
        # 还是采用脚本命令启动，感觉这样处理，耦合度较低（相比于嵌入代码）
        # 但是我感觉不如，在这调用接口处理，但是这就一个独立的功能，哪有什么接口啊
        # 但是我好想可以在这写个函数，然后把linearRegression中的内容放进去
        file_path = run_LinearRegression()
        # 后续在这加入结果输出即可

        """这应该是另一个功能了，可以选择查看输出文件，不过为什么我不直接从文件夹中打开查看呢，非要用我这里的txt框架？
            directory = os.getcwd()
            dir_path = directory + '/data/result'
            file_path = filedialog.askopenfilename(
            initialdir=dir_path,
            title="选择输出文件",
            filetypes=(("output files", "*.txt"), ("All files", "*.*"))
        )"""
        with open(file_path, 'r') as file:
            out_result = file.read()
            print("注意该结果应为重定向的缘故，保存到文件中了，不会在控制台输出")
            # 将text中之前的文本清空，并将输出结果展示到窗口中
            text_display.delete('1.0', 'end')
            text_display.insert('end', out_result)
            # 顺带将结果输出到数据库中
            # 无需顺带了，反正输出都有文件，数据库到时候直接连接文件即可




def button_insertToDatabase_click(event):
    """
        概述：将本次结果插入数据库中
        详情：将输入pcap与输出文件关联起来
    :param event:
    :return:
    """
    if button_insertToDatabase.winfo_containing(event.x_root, event.y_root) == button_insertToDatabase:
        text_display.delete("1.0", 'end')
        text_display.insert("1.0", "ERROR：无法获取文件输入和输出的文件路径\n")
        text_display.insert("end", "数据库关系？？？\n")


def button_preprocessingAll_click(event):
    '''
        处理全部
        ...
    '''
    # 可以提供一个输入框，选取抓取数据包个数
    # 可以更改文件保存位置
    #
    if button_preprocessingAll.winfo_containing(event.x_root, event.y_root) == button_preprocessingAll:
        # text_display.delete('1.0', 'end')
        text_display.insert('end', "一键处理功能还没写\n将用于处理上述全部操作")


def button_databaseView_click(event):
    """
        概述：查看数据库
        细节：

    """
    if button_databaseView.winfo_containing(event.x_root, event.y_root) == button_databaseView:
        # 连接到 SQLite 数据库（如果不存在则会创建一个新的数据库文件）
        conn = sqlite3.connect('databaseTest.db')
        # 创建一个游标对象，用于执行 SQL 语句
        cursor = conn.cursor()
        # 定义要插入的数据
        # 后续应该创建一个file1&2,用于插入输入
        # data_to_insert = ('0001', 'captured_packets.pcap', 'pcapFile')
        # 执行插入数据的 SQL 语句
        # cursor.execute("INSERT INTO file_capturePackets (id, filename, filepath) VALUES (?, ?, ?)", data_to_insert)
        # INSERT INTO file_out_result (id, filename, filepath, file_capturePackets_id) VALUES ('0002', 'test2', 'path2','0002');
        # 定义查询语句
        queries = [
            "SELECT name FROM sqlite_master WHERE type='table';",
            "SELECT * FROM file_capturePackets;",
            "SELECT * FROM file_out_result;"
        ]

        # 执行并打印查询结果
        text_display.delete("1.0", "end")
        for query in queries:
            cursor.execute(query)
            rows = cursor.fetchall()
            print("\nQuery result:\n")
            text_display.insert('end', '查询结果：\n')
            for row in rows:
                print(row)
                str_row = str(row)+'\n'
                text_display.insert('end', str_row)

        # 关闭游标和数据库连接
        cursor.close()
        conn.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    root = tk.Tk()
    '''创建窗口'''
    # 获取电脑屏幕尺寸
    window_x = root.winfo_screenwidth()
    window_y = root.winfo_screenheight()
    # 设置窗口大小
    WIDTH = 600
    HEIGHT = 400
    # 获取窗口左上角坐标
    x = (window_x - WIDTH) / 2
    y = (window_y - HEIGHT) / 2
    # 定位窗口位置
    root.geometry(f'{WIDTH}x{HEIGHT}+{int(x)}+{int(y)}')

    '''创建布局框架'''
    # 创建左侧Frame
    frame_left = tk.Frame(root, bg="lightblue")
    frame_left.place(relx=0, rely=0, relwidth=0.25, relheight=1)
    """
    好像不加这个框架更好看
    # 创建上半部分的子框架
    frame_left_top = tk.Frame(frame_left, bg="red")
    frame_left_top.place(relx=0, rely=0, relwidth=1, relheight=0.70)
    # 创建下半部分的子框架
    frame_left_bottom = tk.Frame(frame_left, bg="yellow")
    frame_left_bottom.place(relx=0, rely=0.72, relwidth=1, relheight=0.25)
    """
    # 创建右侧Frame
    frame_right = tk.Frame(root, bg="lightgreen")
    frame_right.place(relx=0.25, rely=0, relwidth=0.75, relheight=1)

    '''创建控件，并放入布局框架中'''
    # 将按钮控件放入frame控件中
    # 抓取数据包按钮控件
    button_graspData = tk.Button(frame_left, text='抓取数据包')
    button_graspData.pack(fill=tk.BOTH, expand=True)
    button_graspData.bind('<ButtonRelease-1>', button_graspData_click)
    # 预处理按钮控件
    button_preprocessing = tk.Button(frame_left, text='预处理')
    button_preprocessing.pack(fill=tk.BOTH, expand=True)
    button_preprocessing.bind('<ButtonRelease-1>', button_preprocessing_click)
    # 输出结果按钮控件
    button_outputResult = tk.Button(frame_left, text='输出结果')
    button_outputResult.pack(fill=tk.BOTH, expand=True)
    button_outputResult.bind('<ButtonRelease-1>', button_outputResult_click)
    # 插入数据库按钮控件
    button_insertToDatabase = tk.Button(frame_left, text='插入数据库')
    button_insertToDatabase.pack(fill=tk.BOTH, expand=True)
    button_insertToDatabase.bind('<ButtonRelease-1>', button_insertToDatabase_click)
    # 以下控件可以放入左下框架中处理
    # 一键处理按钮控件
    button_preprocessingAll = tk.Button(frame_left, text='一键处理')
    button_preprocessingAll.pack(fill=tk.BOTH, expand=True)
    button_preprocessingAll.bind('<ButtonRelease-1>', button_preprocessingAll_click)
    # 查看数据库
    button_databaseView = tk.Button(frame_left, text='查看数据库')
    button_databaseView.pack(fill=tk.BOTH, expand=True)
    button_databaseView.bind('<ButtonRelease-1>', button_databaseView_click)

    # 滚动条控件
    # 创建一个Scrollbar控件，设置orient为垂直方向
    scrollbar = tk.Scrollbar(root, orient="vertical")
    # 创建一个Text控件，并设置yscrollcommand与Scrollbar的滚动事件绑定
    text_display = tk.Text(frame_right, bg='black', fg='white', yscrollcommand=scrollbar.set)
    # 将Scrollbar与Text的滚动事件绑定
    scrollbar.config(command=text_display.yview)
    # 设置Text控件的宽度和高度
    text_display.pack(fill='both', expand=True, side='left')
    scrollbar.pack(side="right", fill="y")

    # 获取文本内容
    contents = text_display.get(1.0, "end")
    text_display.insert('1.0', "你还没有做任何操作，是操作界面丑到你了麻。。。")

    # 创建一个全局的路径变量，用于传递数据
    # 如果程序报错，因为处理顺序的问题，就是这个全局变量的锅
    # 后续加入选择文件的功能，应该可以解决
    global path_global
    '''

    '''

    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/