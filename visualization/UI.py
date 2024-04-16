import time
import tkinter as tk
from tkinter import filedialog
from func.function import Function
from sqlite.function import DatabaseFunc
from tkinter import ttk

# 定义变量，因为这些变量全局都要使用，所以在这定义
root = tk.Tk()
# 获取电脑屏幕尺寸
window_x = root.winfo_screenwidth()
window_y = root.winfo_screenheight()
# 设置窗口大小
WIDTH = 880
HEIGHT = 680
# 获取窗口左上角坐标
x = (window_x - WIDTH) / 2
y = (window_y - HEIGHT) / 2
# 定位窗口位置
root.geometry(f'{WIDTH}x{HEIGHT}+{int(x)}+{int(y)}')

'''定义布局框架'''
# 创建左侧Frame
frame_left = tk.Frame(root, bg="lightblue")
# 创建右侧Frame
frame_right = tk.Frame(root, bg="lightgreen")
# 创建上半部分的子框架
frame_right_top = tk.Frame(frame_right, bg='red')
# 创建下半部分的子框架
frame_right_bottom = tk.Frame(frame_right, bg='yellow')

'''定义组件'''
# 抓取界面
button_graspData = tk.Button(frame_left, text='抓取数据包')
# 处理界面
button_preprocessing = tk.Button(frame_left, text='处理分析')
# 数据库
button_database = tk.Button(frame_left, text="数据库")

# 功能API,可全局调用
func = Function()


def init():
    """
        概述：初始化界面
        细节：展示一个左边是按钮，右上是展示框，右下是左边按钮的拓展功能，的界面
    """

    '''管理布局'''
    frame_left.place(relx=0, rely=0, relwidth=0.25, relheight=1)
    frame_right.place(relx=0.25, rely=0, relwidth=0.75, relheight=1)
    frame_right_top.place(relx=0, rely=0, relwidth=1, relheight=0.70)
    frame_right_bottom.place(relx=0, rely=0.70, relwidth=1, relheight=0.3)
    '''创建控件，并放入布局框架中'''
    # 将按钮控件放入frame控件中
    # 抓取数据包按钮控件
    button_graspData.pack(fill=tk.BOTH, expand=True)
    button_graspData.bind('<ButtonRelease-1>', button_graspData_click)
    # 处理分析按钮控件
    button_preprocessing.pack(fill=tk.BOTH, expand=True)
    button_preprocessing.bind('<ButtonRelease-1>', button_preprocessing_click)
    # 数据库功能按钮
    button_database.pack(fill=tk.BOTH, expand=True)
    button_database.bind('<ButtonRelease-1>', button_database_click)

    root.mainloop()


def set_right_top_frame():
    """
        概述：创建上半部分text控件
    """
    frame_top = tk.Frame(frame_right, bg='red')
    frame_top.place(relx=0, rely=0, relwidth=1, relheight=0.70)
    # 滚动条控件
    # 创建一个Scrollbar控件，设置orient为垂直方向
    scrollbar = tk.Scrollbar(frame_top, orient="vertical")
    # 创建一个Text控件，并设置yscrollcommand与Scrollbar的滚动事件绑定
    text_display = tk.Text(frame_top, bg='black', fg='white', yscrollcommand=scrollbar.set)
    # 将Scrollbar与Text的滚动事件绑定
    scrollbar.config(command=text_display.yview)
    # 设置Text控件的宽度和高度
    text_display.pack(fill='both', expand=True, side='left')
    scrollbar.pack(side="right", fill="y")
    return text_display


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
    win_x = (win_width - WAITWIDTH) / 2
    win_y = (win_height - WAITHEIGHT) / 2
    waiting_window.geometry(f'{WAITWIDTH}x{WAITHEIGHT}+{int(win_x) + int(root_x)}+{int(win_y) + int(root_y)}')

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


# 抓取界面
def button_graspData_click(event):
    """
        概述：展示抓取数据的界面布局
    """

    # print(button_graspData)

    # 注意这里要加一个entry_path才不会报错
    # 好像是因为函数先定义的，变量在后面？？
    # 变量的作用域需要好好研究一下
    def save_file(entry_path):
        """
            概述：调用功能接口，实现选择文件功能
            细节：调用Function.select_file(entry_path)
                将用户选择路径展示到窗口上
        """
        # 之前直接使用不行，所以多了一步函数
        # 但是这样的结构也有好处，可以在UI中直接添加功能（但是我好像就是为了降低耦合，才分开处理的）
        # 不想改了，就这样吧，有空再说吧
        Function.save_file(entry_path)

    def save_config(entry_num, entry_path):
        """
            概述：调用功能接口，实现保存配置功能
            细节：调用Function.save_config(entry_num, entry_path)的实例方法
                将两个entry控件中的内容，保存到Function实例中（实际保存在func.list_config中）
        """
        # 第一个参数含义，详情见function
        func.save_config(0, entry_num)
        func.save_config(1, entry_path)

    def grasp_data():
        """
            概述：调用功能接口，实现抓取数据包
            细节：调用Funtion.grasp_data()实例方法
                将按照用户提供的路径和抓取数据包的数量进行抓取
                后期可以将协议筛选也加入
        """
        func.grasp_data()

    # main中定义的变量好像有点特殊，应该是全局都可以搜索到
    # 但是在函数外面定义的好像，有点区别

    """设置右上角展示界面"""
    text_display = set_right_top_frame()
    """设置右下角组件"""
    frame_bottom = tk.Frame(frame_right, bg='yellow')
    frame_bottom.place(relx=0, rely=0.70, relwidth=1, relheight=0.3)
    # 设置抓取数据包的数量组件
    label_num = tk.Label(frame_bottom, text="抓取数据包的数量:")
    label_num.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
    entry_num = tk.Entry(frame_bottom, width=10)
    entry_num.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
    # 设置保存pcap文件路径组件
    label_path = tk.Label(frame_bottom, text="保存路径:")
    label_path.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
    entry_path = tk.Entry(frame_bottom, width=50)
    entry_path.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
    button_browse = tk.Button(frame_bottom, text="浏览", command=lambda: save_file(entry_path))
    button_browse.grid(row=1, column=2, padx=5, pady=10, sticky="ew")
    # 废弃：button_browse.bind('<ButtonRelease-1>', select_file)
    # 保存配置组件
    button_save = tk.Button(frame_bottom, text="保存设置", command=lambda: save_config(entry_num, entry_path))
    button_save.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
    # 抓取数据包
    button_graspData = tk.Button(frame_bottom, text='抓取数据包', command=lambda: grasp_data())
    button_graspData.grid(row=2, column=1, padx=5, pady=10, columnspan=2, sticky="ew")
    # 创建一个label用于提示
    label_cue = tk.Label(frame_bottom, text="注意:请在数据库板块设置数据库, 默认xxx")
    label_cue.grid(row=4, column=0, padx=5, pady=10, columnspan=3, sticky="ew")

    # 设置右上角展示框架
    default_text = "功能介绍：\n" \
                   "\t请设置抓取文件的保存路径\n" \
                   "\t请设置抓取数据包的数量\n" \
                   "\t请设置数据库（默认xxx）\n"
    func.set_text(text_display)
    func.set_content(default_text)
    func.display_text()


def button_preprocessing_click(event):
    """
        概述：展示处理进程的界面
    """

    def save_config(entry_select_packet, entry_path):
        """
            概述：保存处理进程界面的配置
        """
        func.save_config(2, entry_select_packet)
        func.save_config(3, entry_path)

    def handle_data():
        """
            概述：处理解析数据（包含预处理和算法）
        """

        def preprocessing():
            """
                概述：预处理程序
                详情：利用脚本命令启动nemesys工具，将输出结果用extract_colored_text方法处理
                返回值：无需返回值
            """

        print("处理解析数据测试")
        func.handle_data()

    """设置右上角展示界面"""
    text_display = set_right_top_frame()
    """设置右下角组件"""
    frame_bottom = tk.Frame(frame_right, bg='yellow')
    frame_bottom.place(relx=0, rely=0.70, relwidth=1, relheight=0.3)
    # 设置抓取数据包的数量组件
    label_select_packet = tk.Label(frame_bottom, text="选择数据包:")
    label_select_packet.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
    entry_select_packet = tk.Entry(frame_bottom, width=10)
    entry_select_packet.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
    button_select_packet = tk.Button(frame_bottom, text="浏览",
                                     command=lambda: Function.select_file(entry_select_packet))
    button_select_packet.grid(row=0, column=2, padx=5, pady=10, sticky="ew")
    # 设置保存pcap文件路径组件
    label_path = tk.Label(frame_bottom, text="保存路径:")
    label_path.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
    entry_path = tk.Entry(frame_bottom, width=50)
    entry_path.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
    button_browse = tk.Button(frame_bottom, text="浏览", command=lambda: Function.save_file(entry_path))
    button_browse.grid(row=1, column=2, padx=5, pady=10, sticky="ew")
    # 废弃：button_browse.bind('<ButtonRelease-1>', select_file)
    # 保存配置组件
    button_save = tk.Button(frame_bottom, text="保存设置", command=lambda: save_config(entry_select_packet, entry_path))
    button_save.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
    # 算法处理
    button_graspData = tk.Button(frame_bottom, text='处理解析', command=lambda: handle_data())
    button_graspData.grid(row=2, column=1, padx=5, pady=10, columnspan=2, sticky="ew")
    # 创建一个label用于提示
    label_cue = tk.Label(frame_bottom, text="注意:请在数据库板块设置数据库, 默认xxx")
    label_cue.grid(row=4, column=0, padx=5, pady=10, columnspan=3, sticky="ew")
    # 设置右上角展示框架
    default_text = "功能介绍：\n" \
                   "\t请选择想要处理的数据包\n" \
                   "\t请设置处理结果保存路径\n" \
                   "\t请设置数据库（默认xxx）\n"
    func.set_text(text_display)
    func.set_content(default_text)
    func.display_text()

def create_window(root, width, height):
    """
        概述：创建一个顶层窗口
        参数：父类窗口，窗口长宽
        详情：在该父类窗口的中间位置创建一个窗口600*200
        返回值：窗口对象
    """
    # 创建一个顶层窗口
    new_window = tk.Toplevel(root)
    new_window.title("数据库可视化操作")
    WAITWIDTH = width
    WAITHEIGHT = height
    # 获取root窗口信息
    root.update()  # 刷新一下前面的配置
    win_width = root.winfo_width()  # 获取窗口宽度（单位：像素）
    win_height = root.winfo_height()  # 获取窗口高度（单位：像素）
    root_x = root.winfo_x()  # 获取窗口左上角的 x 坐标（单位：像素）
    root_y = root.winfo_y()  # 获取窗口左上角的 y 坐标（单位：像素）
    win_x = (win_width - WAITWIDTH) / 2
    win_y = (win_height - WAITHEIGHT) / 2
    new_window.geometry(f'{WAITWIDTH}x{WAITHEIGHT}+{int(win_x) + int(root_x)}+{int(win_y) + int(root_y)}')
    return new_window


def button_database_click(event):
    """
        概述：展示数据库功能界面
        细节：包括增删改查
    """
    def insert_database():
        """
            概述：可视化插入数据
        """
        insert_window = create_window(root, 600, 200)
        label_insert_pcapfile = tk.Label(insert_window, text="选择pcapfile")
        label_insert_pcapfile.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        entry_insert_pcapfile = tk.Entry(insert_window, width=50)
        entry_insert_pcapfile.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        button_insert_pcapfile = tk.Button(insert_window, text="浏览",
                                           command=lambda: func.select_file_root(insert_window, entry_insert_pcapfile))
        button_insert_pcapfile.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        label_insert_result = tk.Label(insert_window, text="选择算法输出结果")
        label_insert_result.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        entry_insert_result = tk.Entry(insert_window, width=50)
        entry_insert_result.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        button_insert_result = tk.Button(insert_window, text="浏览",
                                         command=lambda: func.select_file_root(insert_window, entry_insert_result))
        button_insert_result.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

        button_execute = tk.Button(insert_window, text="关联文件",
                                   command=lambda: func_sqlite.insert_database(entry_insert_pcapfile,
                                                                               entry_insert_result))
        button_execute.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
        pass

    def delete_database():
        """
            概述：可视化删除数据
        """
        delete_window = create_window(root, 250, 100)
        label_delete = tk.Label(delete_window, text="result_file_id")
        label_delete.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        entry_delete = tk.Entry(delete_window, width=10)
        entry_delete.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        button_delete = tk.Button(delete_window, text="删除",
                                           command=lambda: func_sqlite.delete_database(entry_delete.get()))
        button_delete.grid(row=1, column=0, padx=5, pady=10, columnspan=2, sticky="ew")
    # 数据库功能实例
    func_sqlite = DatabaseFunc(func)
    """设置右上角展示界面"""
    text_display = set_right_top_frame()
    # func_sqlite.set_text(text_display)  # 将text组件设置到数据库功能实例中
    """设置右下角组件"""
    frame_bottom = tk.Frame(frame_right, bg='yellow')
    frame_bottom.place(relx=0, rely=0.70, relwidth=1, relheight=0.3)
    # 选择数据库
    label_select_database = tk.Label(frame_bottom, text="选择数据库:")
    label_select_database.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
    entry_select_database = tk.Entry(frame_bottom, width=50)
    entry_select_database.grid(row=0, column=1, padx=5, pady=10, columnspan=3, sticky="ew")
    button_select_database = tk.Button(frame_bottom, text="浏览",
                                       command=lambda: Function.select_file(entry_select_database))
    button_select_database.grid(row=0, column=4, padx=5, pady=10, sticky="ew")
    # 保存配置组件
    button_save = tk.Button(frame_bottom, text="保存设置", command=lambda: func_sqlite.save_sqlite_path_config(4, entry_select_database))
    button_save.grid(row=0, column=5, padx=5, pady=10, sticky="ew")
    # SQL语句
    label_SQL = tk.Label(frame_bottom, text="SQL语句")
    label_SQL.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
    text_SQL = tk.Text(frame_bottom, width=5, height=3)
    text_SQL.grid(row=1, column=1, padx=5, pady=10, columnspan=4, sticky="ew")
    button_SQL = tk.Button(frame_bottom, text="执行", command=lambda: func_sqlite.execute_sql(text_SQL))
    button_SQL.grid(row=1, column=5, padx=5, pady=10, sticky="ew")
    # 快捷指令
    label_quick_instruction = tk.Label(frame_bottom, text="快捷指令")
    label_quick_instruction.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
    # 创建数据库按钮
    button_create_database = tk.Button(frame_bottom, text="创建数据库",
                                       command=lambda: func_sqlite.create_database())
    button_create_database.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
    # 增加数据
    button_insert_database = tk.Button(frame_bottom, text="添加数据", command=insert_database)
    button_insert_database.grid(row=2, column=2, padx=5, pady=10, sticky="ew")
    # 删除数据
    button_delete_database = tk.Button(frame_bottom, text="删除数据", command=delete_database)
    button_delete_database.grid(row=2, column=3, padx=5, pady=10, sticky="ew")
    # 查找数据
    button_view_database = tk.Button(frame_bottom, text="查找数据",
                                     command=lambda: func_sqlite.view_database())
    button_view_database.grid(row=2, column=4, padx=5, pady=10, columnspan=2, sticky="ew")

    # 设置右上角展示框架
    default_text = "功能介绍：\n" \
                   "\t请设置数据库\n" \
                   "\t数据库快捷指令：创增删查\n" \
                   "\t\t创建表格：创建算法所需的两张表格\n" \
                   "\t\t添加数据：将本次运算结果和数据包关联到数据库中\n" \
                   "\t\t删除数据：\n" \
                   "\t\t查看数据：查看数据库（包含表格具体内容）\n"
    func.set_text(text_display)
    func.set_content(default_text)
    func.display_text()

