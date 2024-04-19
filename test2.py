from scapy.all import *

# 读取 pcap 文件
# packets = rdpcap(func.list_config[1])
packets = rdpcap("data/pcapfile/7.pcap")
# packets = rdpcap("Rose/dataset/NBNS/nbns.pcap")
# packets = rdpcap("Rose/dataset/websocket/web_2000.pcapng")
# 存放路径
file_path = "data/temp/pcapToTxt.txt"

with open(file_path, "w+") as f:
    for packet in packets[:10]:
        f.write(str(packet.summary()) + "\n")
        f.write(str(packet.show()) + "\n")

    # 移动文件指针到文件开头以便读取写入的内容
    f.seek(0)
    pcap_txt_content = f.read()

# 在这之后可以使用 pcap_txt_content 变量来访问读取的文件内容


