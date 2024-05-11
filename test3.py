import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.frame = None
        self.label = tk.Label(root)
        self.label.pack()
        self.update_frame()
        self.root.mainloop()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=frame)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            self.label.after(10, self.update_frame)
        else:
            self.cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tkinter Video Player")
    video_path = askopenfilename()  # 让用户选择视频文件
    player = VideoPlayer(root, video_path)