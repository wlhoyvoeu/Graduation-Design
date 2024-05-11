import os
import sqlite3
from func.function import Function
import subprocess
class DatabaseFunc:
    """
        概述：数据库的各项功能
    """

    def __init__(self, func):
        # self.text_display = None
        # 为了使用Function中的设置text的功能
        self.func = func
        self.conn = None

    def save_sqlite_path_config(self, num, entry):
        self.func.save_config(num, entry)
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
            text_content = "成功创建链表\n" + text_content
            self.func.set_content(text_content)
            self.func.display_text()
            conn.commit()
        except sqlite3.Warning as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()
        except sqlite3.OperationalError as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()

        """# 关闭游标和数据库连接
        cursor.close()
        conn.close()"""

    def insert_database(self, entry_pcap, entry_result):
        """
            概述：选择pcap和输出结果关联
            参数：entry控件，里面的内容是pcap文件地址和result地址
        """
        # 分离出地址和文件名，数据库要用
        pcap_path = entry_pcap.get()
        result_path = entry_result.get()
        # 使用 os.path.split() 函数分割文件地址和文件名
        directory_pcap, filename_pcap = os.path.split(pcap_path)
        directory_result, filename_result = os.path.split(result_path)

        print("pcap文件地址（路径）:", directory_pcap)
        print("pcap文件名:", filename_pcap)
        print("result文件地址（路径）:", directory_result)
        print("result文件名:", filename_result)
        conn = self.conn
        # 创建一个游标对象，用于执行 SQL 语句
        cursor = conn.cursor()
        # 定义查询语句
        try:
            cursor.execute("INSERT INTO file_capturePackets (filename, filepath) VALUES (?, ?)",
                           (filename_pcap, directory_pcap))
            # 执行 SQL 查询上一布语句放入数据库中的文件id
            cursor.execute("SELECT id FROM file_capturePackets WHERE filename = ?", (filename_pcap,))
            result = cursor.fetchone()
            if result:
                pcap_id = result[0]
                print(f"The ID of {filename_pcap} is: {pcap_id}")
                # pcap插入数据库成功，执行下面语句
                cursor.execute(
                    "INSERT INTO file_out_result (filename, filepath, file_capturePackets_id) VALUES (?, ?, ?)",
                    (filename_result, directory_result, pcap_id))
                # 查询表一并反馈
                cursor.execute("SELECT * FROM file_capturePackets;")
                rows = cursor.fetchall()
                text_content = ''
                for row in rows:
                    print(row)
                    str_row = str(row) + '\n'
                    text_content += str_row
                text_content = "capturePacketsfile表格\n" + text_content + '\n'
                # 查询表二并反馈
                cursor.execute("SELECT * FROM file_out_result;")
                rows = cursor.fetchall()
                text_content = text_content + "output表格\n"
                for row in rows:
                    print(row)
                    str_row = str(row) + '\n'
                    text_content += str_row
                print("成功插入数据\n", text_content)
                text_content = "成功插入数据\n" + text_content
                self.func.set_content(text_content)
                self.func.display_text()
                conn.commit()
            else:
                print(f"No student with name {filename_pcap} found")
        except sqlite3.Warning as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()
        except sqlite3.OperationalError as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()

        """# 关闭游标和数据库连接
        cursor.close()
        conn.close()"""

    def delete_database(self, result_id):
        """
            概述：删除pcap和输出结果关联
            参数：传入result表格的id即可，因为其关联pcap
        """

        conn = self.conn
        # 创建一个游标对象，用于执行 SQL 语句
        cursor = conn.cursor()
        # 定义查询语句
        try:
            cursor.execute(
                "DELETE FROM file_capturePackets WHERE id = "
                "(SELECT file_capturePackets_id FROM file_out_result WHERE id = ?)",
                (result_id,))
            cursor.execute("DELETE FROM file_out_result WHERE id = ?", (result_id,))

            # 查询表一并反馈
            cursor.execute("SELECT * FROM file_capturePackets;")
            rows = cursor.fetchall()
            text_content = ''
            for row in rows:
                print(row)
                str_row = str(row) + '\n'
                text_content += str_row
            text_content = "capturePacketsfile表格\n" + text_content + '\n'
            # 查询表二并反馈
            cursor.execute("SELECT * FROM file_out_result;")
            rows = cursor.fetchall()
            text_content = text_content + "output表格\n"
            for row in rows:
                print(row)
                str_row = str(row) + '\n'
                text_content += str_row
            print("成功删除数据\n", text_content)
            text_content = "成功删除数据\n" + text_content
            self.func.set_content(text_content)
            self.func.display_text()
            conn.commit()
        except sqlite3.Warning as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()
        except sqlite3.OperationalError as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()

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
                text_content += "数据库链表查询结果：\n"
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

        """# 关闭游标和数据库连接
        cursor.close()
        conn.close()"""

    def execute_sql(self, text):
        """
            概述：用sql语句直接操纵数据库
            参数：text控件
        """
        content = text.get("1.0", "end")
        conn = self.conn
        cursor = conn.cursor()
        # 定义查询语句
        try:
            cursor.execute(content)
            rows = cursor.fetchall()
            text_content = ''
            for row in rows:
                print(row)
                str_row = str(row) + '\n'
                text_content += str_row
            print("成功执行用户输入的sql语句")
            text_content = "sql语句执行结果如下:\n" + text_content
            self.func.set_content(text_content)
            self.func.display_text()
            conn.commit()
        except sqlite3.Warning as e:
            print("出现异常：", e)
            text_content = "请检查sql语句是否正确：\n" + str(e)
            self.func.set_content(text_content)
            self.func.display_text()
        except sqlite3.OperationalError as e:
            print("出现异常：", e)
            self.func.set_content(str(e))
            self.func.display_text()

        """
        # 不能关闭，这里赋值用的是地址
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()"""
