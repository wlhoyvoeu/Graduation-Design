import threading
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
HEIGHT = 630
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
frame_right_top = tk.Frame(frame_right, bg="white")
# 创建下半部分的子框架
frame_right_bottom = tk.Frame(frame_right)

'''定义组件'''
# 抓取界面
button_graspData = tk.Button(frame_left, text='抓取数据包')
# 处理界面
button_preprocessing = tk.Button(frame_left, text='处理分析')
# 数据库
button_database = tk.Button(frame_left, text="数据库")

# 功能API,可全局调用
func = Function()

"""
    感觉这样不规范（应该放在一块定义？？？）
    但是这个布局确实只需要定义一次即可，下次要使用的时候直接调用设置即可
    一开始想的是，将控件等都放入布局中（省去了加载时间），但是这样每个按钮都需要额外定义两个框架（好像也可以）
    总共3个按钮，再创建6个子框架
    所有的创建框架布局改成，使用设定好的框架布局
        设置框架布局函数，重写成两部分
            一部分用于设置框架，并将控件放入布局中（所以这部分函数只需要调用一次即可，所以不写函数也可以，但是为了好看？结构清晰，还是创建函数）
            另一部分用于点击按钮时，将布局展示出来
"""
# 在这创建三个右上部分的框架，用于放置text控件
frame_top_grasp = tk.Frame(frame_right_top)
frame_top_handle = tk.Frame(frame_right_top)
frame_top_database = tk.Frame(frame_right_top)
# 右下角框架
frame_bottom_grasp = tk.Frame(frame_right_bottom)
frame_bottom_handle = tk.Frame(frame_right_bottom)
frame_bottom_database = tk.Frame(frame_right_bottom)
# 运行错误的，只是为了暂时观看方便
# set_right_top_frame(frame_top_grasp)
# 我们将设置框架放在init中

# 定义一个窗口线程
global progress_bar_thread


# 启动函数
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

    # 初始化不同按钮的初始化布局
    """
    这些放入设置右边布局的函数中
    set_right_top_frame(frame_top_grasp)
    set_right_top_frame(frame_top_handle)
    set_right_top_frame(frame_top_database)"""
    set_right_frame_grasp(frame_top_grasp, frame_bottom_grasp)
    set_right_frame_handle(frame_top_handle, frame_bottom_handle)
    set_right_frame_database(frame_top_database, frame_bottom_database)
    """# 测试按钮，用于测试当前创建的帧布局
    # 因为该问题不解决的话，很容易造成程序崩溃
    def show_frames(root):
        # 获取 root 的所有子控件
        children = root.winfo_children()

        # 遍历所有子控件
        for child in children:
            # 如果子控件是 Frame 类型，并且当前可见，则打印其名称
            if isinstance(child, tk.Frame):
                print("Frame名称:", child.winfo_name())

    button_test = tk.Button(frame_left, text="测试布局数量", command=lambda: show_frames(frame_right))
    button_test.pack()"""
    root.mainloop()


def set_right_top_frame(frame_top):
    """
        概述：创建右上半部分text控件
        参数：右上部分框架
        细节：将创建的text控件，放入传入的右上框架中
            该函数，每个右上角框架只需要调用一次即可
        返回值：text控件
    """

    # 原本的启动帧布局的方式
    # frame_top.place(relx=0, rely=0, relwidth=1, relheight=0.70)
    # 滚动条控件
    # 创建一个Scrollbar控件，设置orient为垂直方向
    scrollbar = tk.Scrollbar(frame_top, orient="vertical")
    # 创建一个Text控件，并设置yscrollcommand与Scrollbar的滚动事件绑定
    text_display = tk.Text(frame_top, yscrollcommand=scrollbar.set)
    # 将Scrollbar与Text的滚动事件绑定
    scrollbar.config(command=text_display.yview)
    # 设置Text控件的宽度和高度
    text_display.pack(fill='both', expand=True, side='left')
    scrollbar.pack(side="right", fill="y")
    return text_display


def create_window(root, width, height):
    """
        概述：创建一个顶层窗口
        参数：父类窗口，窗口长宽
        详情：在该父类窗口的中间位置创建一个窗口600*200
        返回值：窗口对象
    """
    # 创建一个顶层窗口
    new_window = tk.Toplevel(root)
    new_window.title("默认窗口（可以自行设置）")
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


def show_waiting_window():
    """
        概述：创建一个等待窗口
        返回值：等待窗口
    """

    # 创建一个顶层窗口
    waiting_window = create_window(root, 300, 150)
    waiting_window.title("waiting a moment")
    # 在等待窗口中添加一些文本和进度条
    label = tk.Label(waiting_window, text="请稍等...")
    label.pack(pady=10)
    # 创建任务进度标签
    # progress_label = tk.Label(waiting_window, text="任务进度: 0%")
    # progress_label.pack()
    # 创建进度条,这里使用不确定进度条参数
    progress_bar = ttk.Progressbar(waiting_window, orient='horizontal', mode='indeterminate')
    progress_bar.pack(fill='y', pady=20)
    """
        注释：进度条使用start才会启动动画
            mainloop会自动检测内部所有控件
            所以如果程序在某处执行了耗时操作，此操作会占用主线程，导致无法检测内部控件，进度条自然就不动了
    """
    progress_bar.start()
    waiting_window.update()
    # waiting_window.mainloop()

    return waiting_window


def destroy_waiting_window(waiting_window):
    """
        概述：删除等待窗口
        参数：窗口
    """
    waiting_window.destroy()


def set_right_frame_grasp(frame_top, frame_bottom):
    """
        概述：创建抓取数据包的右边框架
        参数：抓取数据包的右上布局框架，右下布局框架
        细节：这玩意指向性有点强，只是为了设置抓取数据包的框架,和控件功能
        开发者注：但是为什么用函数呢？只是为了结构清晰
            但是好像不符合规范，因为函数就是为了避免许多相同功能的代码重复
            按照我理解的规范，这段函数应该写在启动函数中
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

    def save_config(entry_num, entry_path, entry_filter):
        """
            概述：调用功能接口，实现保存配置功能
            参数：抓取数据包的数量
                pcap保存路径
                抓取数据包过滤器
            细节：调用Function.save_config(entry_num, entry_path)的实例方法
                将两个entry控件中的内容，保存到Function实例中（实际保存在func.list_config中）
        """
        # 第一个参数含义，详情见function
        func.save_config(0, entry_num)
        func.save_config(1, entry_path)
        func.save_config(5, entry_filter)

    def grasp_data():
        """
            概述：调用功能接口，实现抓取数据包
            细节：调用Funtion.grasp_data()实例方法
                将按照用户提供的路径和抓取数据包的数量进行抓取
                后期可以将协议筛选也加入
        """

        def task():
            """
                概述:将抓取数据包这样的耗时操作放入线程中处理
            """
            # 设置一下展示容器
            func.set_text(text_display)
            # print("休眠5秒")
            # time.sleep(5)
            func.grasp_data()
            waiting_window.destroy()

        # 耗时操作，创建等待窗口
        waiting_window = show_waiting_window()

        # 启动子线程执行任务
        t = threading.Thread(target=task)
        t.start()

    # main中定义的变量好像有点特殊，应该是全局都可以搜索到
    # 但是在函数外面定义的好像，有点区别
    """设置右上角布局"""
    text_display = set_right_top_frame(frame_top)
    """设置右下角组件"""
    # 设置抓取数据包的数量组件
    label_num = tk.Label(frame_bottom, text="抓取数据包的数量:")
    label_num.grid(row=0, column=0, padx=5, pady=8, sticky="ew")
    entry_num = tk.Entry(frame_bottom, width=10)
    entry_num.grid(row=0, column=1, padx=5, pady=8, columnspan=2, sticky="ew")
    # 设置抓取数据包的过滤条件
    label_filter = tk.Label(frame_bottom, text="过滤条件")
    label_filter.grid(row=1, column=0, padx=5, pady=8, sticky="ew")
    entry_filter = tk.Entry(frame_bottom, width=10)
    entry_filter.grid(row=1, column=1, padx=5, pady=8, columnspan=4, sticky="ew")
    # 设置保存pcap文件路径组件
    label_path = tk.Label(frame_bottom, text="保存路径:")
    label_path.grid(row=2, column=0, padx=5, pady=8, sticky="ew")
    entry_path = tk.Entry(frame_bottom, width=55)
    entry_path.grid(row=2, column=1, padx=5, pady=8, columnspan=5, sticky="ew")
    button_browse = tk.Button(frame_bottom, text="浏览", command=lambda: save_file(entry_path))
    button_browse.grid(row=2, column=6, padx=5, pady=8, sticky="ew")
    # 废弃：button_browse.bind('<ButtonRelease-1>', select_file)
    # 保存配置组件
    button_save = tk.Button(frame_bottom, text="保存设置",
                            command=lambda: save_config(entry_num, entry_path, entry_filter))
    button_save.grid(row=3, column=0, padx=5, pady=8, sticky="ew")
    # 抓取数据包
    button_graspData = tk.Button(frame_bottom, text='抓取数据包', command=lambda: grasp_data())
    button_graspData.grid(row=3, column=1, padx=5, pady=8, columnspan=6, sticky="ew")
    # 创建一个label用于提示
    # label_cue = tk.Label(frame_bottom, text="注意:请在数据库板块设置数据库, 默认xxx")
    # label_cue.grid(row=4, column=0, padx=5, pady=10, columnspan=3, sticky="ew")

    # 设置右上角展示框架
    default_text = ("功能介绍：\n"
                    "\t本模块将根据你设定的过滤条件和数量抓取数据包，并储存为pcap文件\n"
                    "配置需求：\n"
                    "\t请设置抓取数据包的数量\n"
                    "\t请设置过滤条件\n"
                    "\t请设置抓取文件的保存路径\n"
                    "\t注意保存设置\n"
                    "过滤规则: \n"
                    "\t过滤源地址：src host 192.168.1.1\n"
                    "\t过滤目的地址：dst host 192.168.1.1\n"
                    "\t过滤协议：tcp\n"
                    "\t过滤源端口：src port 50152\n"
                    "\t过滤目的端口：dst port 80\n"
                    "\t(多个过滤条件可以用and叠加)\n")

    func.set_text(text_display)
    func.set_content(default_text)
    func.display_text()


def set_right_frame_handle(frame_top, frame_bottom):
    """
        概述：设置数据处理的右边框架
        参数：数据处理的右上布局框架，右下布局框架
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
                废弃：该功能在func.function中
            """

        def task():
            """
                概述：将解析处理这一耗时操作放到线程中处理
            """
            print("处理解析数据测试")
            try:
                # 设置一下展示容器
                func.set_text(text_display)
                func.handle_data()
            except PermissionError as e:
                # time.sleep(10)
                print("大概率权限有问题")
            finally:
                waiting_window.destroy()

        waiting_window = show_waiting_window()
        # 启动子线程执行任务
        t = threading.Thread(target=task)
        t.start()

    """设置右上角展示界面"""
    text_display = set_right_top_frame(frame_top)
    """设置右下角组件"""
    # 设置选择数据包的组件
    label_select_packet = tk.Label(frame_bottom, text="选择数据包:")
    label_select_packet.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
    entry_select_packet = tk.Entry(frame_bottom, width=10)
    entry_select_packet.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
    button_select_packet = tk.Button(frame_bottom, text="浏览",
                                     command=lambda: Function.select_file(entry_select_packet))
    # command=functools.partial(Function.select_file, entry_select_packet)
    button_select_packet.grid(row=0, column=2, padx=5, pady=10, sticky="ew")
    # 设置保存pcap文件路径组件
    label_path = tk.Label(frame_bottom, text="保存路径:")
    label_path.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
    entry_path = tk.Entry(frame_bottom, width=55)
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
    # label_cue = tk.Label(frame_bottom, text="注意:请在数据库板块设置数据库, 默认xxx")
    # label_cue.grid(row=4, column=0, padx=5, pady=10, columnspan=3, sticky="ew")
    # 设置右上角展示框架
    default_text = ("功能介绍：\n"
                    "\t本模块将从抓取的大量数据包中，推断出可能的字段长度和字段偏移量\n"
                    "配置需求：\n"
                    "\t请选择想要处理的数据包\n"
                    "\t请设置处理结果保存路径\n")
    func.set_text(text_display)
    func.set_content(default_text)
    func.display_text()


def set_right_frame_database(frame_top, frame_bottom):
    """
        概述：设置数据库的右边框架
        参数：数据库的右上布局框架，右下布局框架
    """

    def insert_database():
        """
            概述：可视化插入数据
        """

        def select_file_root(window, entry):
            """
                概述：选择文件
                参数：所在窗口
            """
            func.set_text(text_display)
            Function.select_file_root(window, entry)

        # def associated_files()关联文件，没必要设置text控件了，因为关联前肯定要选择文件，此时已经设定过了
        # 创建弹窗
        insert_window = create_window(root, 600, 200)
        insert_window.title("向数据库插入数据")
        label_insert_pcapfile = tk.Label(insert_window, text="选择pcapfile")
        label_insert_pcapfile.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        entry_insert_pcapfile = tk.Entry(insert_window, width=50)
        entry_insert_pcapfile.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        button_insert_pcapfile = tk.Button(insert_window, text="浏览",
                                           command=lambda: select_file_root(insert_window, entry_insert_pcapfile))
        button_insert_pcapfile.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        label_insert_result = tk.Label(insert_window, text="选择算法输出结果")
        label_insert_result.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        entry_insert_result = tk.Entry(insert_window, width=50)
        entry_insert_result.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        button_insert_result = tk.Button(insert_window, text="浏览",
                                         command=lambda: select_file_root(insert_window, entry_insert_result))
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

        def delete(entry):
            """
                概述：删除数据
                细节：顺带设定text控件，删除结果和与其关联的数据包在数据库中的记录
            """
            func.set_text(text_display)
            func_sqlite.delete_database(entry.get())

        delete_window = create_window(root, 200, 100)
        delete_window.title("删除数据")
        label_delete = tk.Label(delete_window, text="result_file_id")
        label_delete.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        entry_delete = tk.Entry(delete_window, width=10)
        entry_delete.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        button_delete = tk.Button(delete_window, text="删除",
                                  command=lambda: delete(entry_delete))
        button_delete.grid(row=1, column=0, padx=5, pady=10, columnspan=2, sticky="ew")

    def execute_sql(text):
        """
            概述：执行sql语句
            参数：sql_text控件
        """
        func.set_text(text_display)
        func_sqlite.execute_sql(text)

    def view_database():
        """
            概述：查找数据
            参数：
        """
        func.set_text(text_display)
        func_sqlite.view_database()

    # 数据库功能实例
    func_sqlite = DatabaseFunc(func)
    """设置右上角展示界面"""
    text_display = set_right_top_frame(frame_top)
    # func_sqlite.set_text(text_display)  # 将text组件设置到数据库功能实例中
    """设置右下角组件"""
    # 选择数据库
    label_select_database = tk.Label(frame_bottom, text="选择数据库:")
    label_select_database.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
    entry_select_database = tk.Entry(frame_bottom, width=50)
    entry_select_database.grid(row=0, column=1, padx=5, pady=10, columnspan=3, sticky="ew")
    button_select_database = tk.Button(frame_bottom, text="浏览",
                                       command=lambda: Function.select_file(entry_select_database))
    button_select_database.grid(row=0, column=4, padx=5, pady=10, sticky="ew")
    # 保存配置组件
    button_save = tk.Button(frame_bottom, text="保存设置",
                            command=lambda: func_sqlite.save_sqlite_path_config(4, entry_select_database))
    button_save.grid(row=0, column=5, padx=5, pady=10, sticky="ew")
    # SQL语句
    label_SQL = tk.Label(frame_bottom, text="SQL语句")
    label_SQL.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
    text_SQL = tk.Text(frame_bottom, width=5, height=3)
    text_SQL.grid(row=1, column=1, padx=5, pady=10, columnspan=4, sticky="ew")
    button_SQL = tk.Button(frame_bottom, text="执行", command=lambda: execute_sql(text_SQL))
    button_SQL.grid(row=1, column=5, padx=5, pady=10, sticky="ew")
    # 快捷指令
    label_quick_instruction = tk.Label(frame_bottom, text="快捷指令")
    label_quick_instruction.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
    # 创建数据库按钮
    # 可能会出现问题，因为这个函数在text控件打印前，没有设置text控件，如果出问题设置一下就行，不想改了
    button_create_database = tk.Button(frame_bottom, text="创建数据库链表",
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
                                     command=lambda: view_database())
    button_view_database.grid(row=2, column=4, padx=5, pady=10, columnspan=2, sticky="ew")

    # 设置右上角展示框架
    default_text = ("功能介绍：\n"
                    "\t提供快捷指令代替常用的数据库操作\n"
                    "\t提供sql语句接口\n"                    
                    "配置需求：\n"
                    "\t请设置数据库\n"
                    "快捷指令：\n"
                    "\t创建表格：创建算法所需的两张表格\n"
                    "\t添加数据：将本次运算结果和数据包关联到数据库中\n"
                    "\t删除数据：选择不需要的运算结果，会自动关联删除数据包记录\n"
                    "\t查看数据：查看数据库（包含表格具体内容）\n"
                    )
    func.set_text(text_display)
    func.set_content(default_text)
    func.display_text()


def show_frame(frame_top, frame_bottom):
    """
        概述：展示界面
        参数：右上布局，和右下布局
        细节：隐藏其他界面，展示当前界面
    """
    # 隐藏所有frame
    frame_top_grasp.place_forget()
    frame_top_handle.place_forget()
    frame_top_database.place_forget()
    frame_bottom_grasp.place_forget()
    frame_bottom_handle.place_forget()
    frame_bottom_database.place_forget()
    # 展示frame
    frame_top.place(relx=0, rely=0, relwidth=1, relheight=1)
    frame_bottom.place(relx=0, rely=0, relwidth=1, relheight=1)
    """
    两种布局都可以实现
    frame_top_grasp.pack_forget()
    frame_bottom_grasp.pack_forget()
    frame_top_handle.pack_forget()
    frame_bottom_handle.pack_forget()
    frame_top.pack(fill=tk.BOTH, expand=True)
    frame_bottom.pack(fill=tk.BOTH, expand=True)"""


def button_graspData_click(event):
    """
        概述：展示抓取数据的界面布局
        细节：将抓取数据界面的frame，展现出来
        开发者注：其实直接调用show_frame作为点击事项即可，但是不想该了，毕竟前面写了那么久，有感情了
    """
    show_frame(frame_top_grasp, frame_bottom_grasp)


def button_preprocessing_click(event):
    """
        概述：展示处理进程的界面
        开发者：其实直接调用show_frame作为点击事项即可，但是不想该了，毕竟前面写了那么久，有感情了
    """
    show_frame(frame_top_handle, frame_bottom_handle)


def button_database_click(event):
    """
        概述：展示数据库功能界面
        细节：包括增删改查
        开发者注：其实直接调用show_frame作为点击事项即可，但是不想该了，毕竟前面写了那么久，有感情了
    """
    show_frame(frame_top_database, frame_bottom_database)
