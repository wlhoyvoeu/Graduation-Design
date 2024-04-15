import sqlite3
from func.function import Function

class DatabaseFunc:
    """
        概述：数据库的各项功能
    """

    def __init__(self, func):
        # self.text_display = None
        # 为了使用Function中的设置text的功能
        self.func = func
        # 连接到 SQLite 数据库（如果不存在则会创建一个新的数据库文件）
        print("选择数据库的位置：", self.func.list_config[4])
        if self.func.list_config[4] == '':
            print("数据库不存在")
        else:
            self.conn = sqlite3.connect(self.func.list_config[4])

    def set_text(self, text_display):
        """
            概述：设置text框架实例
        """
        self.func.set_text(text_display)
        pass

    def excute_sql(self):
        """
            概述：使用sql语句查询数据库
        """

    def create_database(self):
        """
            概述：创建表格
        """
        conn = self.conn
        print(self.func.list_config[4])
        # 创建一个游标对象，用于执行 SQL 语句
        cursor = conn.cursor()
        # 定义查询语句
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS file_capturePackets (
                                        id INTEGER PRIMARY KEY,
                                        filename TEXT NOT NULL,
                                        filepath TEXT NOT NULL
                                    )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS file_out_result (
                                        id INTEGER PRIMARY KEY,
                                        filename TEXT NOT NULL,
                                        filepath TEXT NOT NULL,
                                        file_capturePackets_id INTEGER NOT NULL,
                                        FOREIGN KEY (file_capturePackets_id) REFERENCES file_capturePackets_id(id)
                                    )''')
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            rows = cursor.fetchall()
            text_content = ''
            for row in rows:
                print(row)
                str_row = str(row) + '\n'
                text_content += str_row
            print("成功创建表格")
            text_content = "成功创建表格\n" + text_content
            self.func.set_content(text_content)
            self.func.display_text()
        except sqlite3.OperationalError as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()

        # 关闭游标和数据库连接
        cursor.close()
        conn.close()

    def insert_database(self):
        conn = self.conn
        # 创建一个游标对象，用于执行 SQL 语句
        cursor = conn.cursor()
        # 定义查询语句
        try:
            cursor.execute("INSERT INTO file_capturePackets (filename, filepath) VALUES (?, ?, ?)",
                           ('0000', 'DBtestNoneData', '/path/to/you'))
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            rows = cursor.fetchall()
            text_content = ''
            for row in rows:
                print(row)
                str_row = str(row) + '\n'
                text_content += str_row
            print("成功创建表格")
            text_content = "成功创建表格\n" + text_content
            self.func.set_content(text_content)
            self.func.display_text()
        except sqlite3.OperationalError as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()

        # 关闭游标和数据库连接
        cursor.close()
        conn.close()


    def view_database(self):
        """
            概述：查看数据库
        """
        conn = self.conn
        print(self.func.list_config[4])
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
        text_content = ""
        for index, query in enumerate(queries):
            cursor.execute(query)
            rows = cursor.fetchall()
            print("\nQuery result:\n")
            if index == 0:
                text_content += "数据库查询结果：\n"
            elif index == 1:
                text_content += "pcap文件列表如下：\n"
            elif index == 2:
                text_content += "运算结果列表如下：\n"
            else:
                text_content += "数据库查询出错\n"
            for row in rows:
                print(row)
                str_row = str(row) + '\n'
                text_content += str_row

        self.func.set_content(text_content)
        self.func.display_text()


        # 关闭游标和数据库连接
        cursor.close()
        conn.close()
