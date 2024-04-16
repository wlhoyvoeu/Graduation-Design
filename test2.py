import tkinter as tk
from tkinter import ttk

# 创建窗口
waiting_window = tk.Tk()
waiting_window.title("等待窗口")
waiting_window.geometry("300x150")

# 在等待窗口中添加一些文本和进度条
label = tk.Label(waiting_window, text="请稍等...")
label.pack(pady=10)

# 创建进度条，使用不确定模式
progress_bar = ttk.Progressbar(waiting_window, orient='horizontal', mode='indeterminate', length=200)
progress_bar.pack(fill='y', pady=20)

waiting_window.mainloop()  # 启动事件循环
