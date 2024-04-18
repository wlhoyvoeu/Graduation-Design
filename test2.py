import tkinter as tk


def show_frames(root):
    # 获取 root 的所有子控件
    children = root.winfo_children()

    # 遍历所有子控件
    for child in children:
        # 如果子控件是 Frame 类型，并且当前可见，则打印其名称
        if isinstance(child, tk.Frame) :
            print("Frame名称:", child.winfo_name())
def show_frame(frame):
    # 隐藏所有帧布局
    frame1.pack_forget()
    frame2.pack_forget()

    # 显示指定的帧布局
    frame.pack()


# 创建主窗口
root = tk.Tk()

# 创建两个帧布局
frame1 = tk.Frame(root, width=200, height=200, bg="red")
frame2 = tk.Frame(root, width=200, height=200, bg="blue")

# 创建按钮
button1 = tk.Button(root, text="显示红色帧布局", command=lambda: show_frame(frame1))
button2 = tk.Button(root, text="显示蓝色帧布局", command=lambda: show_frame(frame2))
button3 = tk.Button(root, text="查看当前存在的布局", command=lambda: show_frames(root))

# 将按钮放置在主窗口上
button1.pack()
button2.pack()
button3.pack()

# 初始化时显示第一个帧布局
show_frame(frame1)

# 查看当前开启的帧
# show_frames(root)

# 运行主事件循环
root.mainloop()
