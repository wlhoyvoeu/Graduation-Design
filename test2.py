import tkinter as tk

def load_settings():
    # 从文件中加载设置数据
    try:
        with open('settings.txt', 'r') as file:
            settings = file.read().splitlines()
            return settings
    except FileNotFoundError:
        # 如果文件不存在，则返回默认设置
        return ['default_value'] * 3  # 这里假设设置数据有三个值

def save_settings(settings):
    # 将设置数据保存到文件
    with open('settings.txt', 'w') as file:
        for setting in settings:
            file.write(setting + '\n')

def main():
    # 加载设置数据
    settings = load_settings()

    # 创建 Tkinter 窗口
    root = tk.Tk()

    # 在窗口中使用设置数据
    label1 = tk.Label(root, text="Setting 1: " + settings[0])
    label2 = tk.Label(root, text="Setting 2: " + settings[1])
    label3 = tk.Label(root, text="Setting 3: " + settings[2])
    label1.pack()
    label2.pack()
    label3.pack()

    # 运行 Tkinter 主循环
    root.mainloop()

    # 在程序关闭时保存设置数据
    save_settings(settings)

if __name__ == "__main__":
    main()
