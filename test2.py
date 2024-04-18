import tkinter as tk
from tkinter import ttk
import threading
import time

def create_waiting_window():
    # 创建主窗口
    waiting_window = tk.Toplevel()
    waiting_window.title("请稍等...")

    # 添加标签
    label = tk.Label(waiting_window, text="任务进行中，请稍候...")
    label.pack(pady=10)

    # 创建进度条
    progress_bar = ttk.Progressbar(waiting_window, orient='horizontal', mode='indeterminate')
    progress_bar.pack(pady=10)

    # 启动进度条动画
    progress_bar.start()

    # 设置窗口大小并居中显示
    waiting_window.geometry("300x100")
    waiting_window.update_idletasks()
    x = (waiting_window.winfo_screenwidth() - waiting_window.winfo_width()) // 2
    y = (waiting_window.winfo_screenheight() - waiting_window.winfo_height()) // 2
    waiting_window.geometry("+{}+{}".format(x, y))

    return waiting_window

def task():
    # 模拟任务执行
    time.sleep(5)

    # 任务完成后关闭等待窗口
    waiting_window.destroy()

def start_task():
    # 创建等待窗口
    global waiting_window
    waiting_window = create_waiting_window()

    # 启动子线程执行任务
    t = threading.Thread(target=task)
    t.start()

# 创建主窗口
root = tk.Tk()
root.title("主窗口")

# 创建按钮来触发任务
button = tk.Button(root, text="启动任务", command=start_task)
button.pack(pady=20)

root.mainloop()
