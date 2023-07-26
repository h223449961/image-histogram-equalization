# -*- coding: utf-8 -*-
import cv2
import numpy as np
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
root = tk.Tk()
radioValue = tk.IntVar()
mediaFrame = tk.Frame(root).pack()
"""
創建 tkinker label
"""
media = tk.Label(mediaFrame)
media.pack()
fig = plt.figure()
"""
創建初始畫布
"""
f_plot =fig.add_subplot(111)
"""
創建 histogram 畫布
"""
canva = FigureCanvasTkAgg(fig,root)
canva.get_tk_widget().pack(side='right')
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img

def validate():
    value = radioValue.get()
    global mode
    '''
    1 cv2.COLOR_BGR2RGB
    2 cv2.COLOR_BGR2HSV
    3 cv2.COLOR_BGR2HLS
    4 cv2.COLOR_BGR2Lab
    5 cv2.COLOR_BGR2Luv
    6 cv2.COLOR_BGR2YCrCb
    7 cv2.COLOR_BGR2XYZ
    '''
    if (value == 1):
        mode = cv2.COLOR_BGR2RGB
    if( value == 2):
        mode = cv2.COLOR_BGR2HSV
    if( value == 3):
        mode = cv2.COLOR_BGR2HLS
    if( value == 4):
        mode = cv2.COLOR_BGR2Lab
    if( value == 5):
        mode = cv2.COLOR_BGR2Luv
    if( value == 6):
        mode = cv2.COLOR_BGR2YCrCb
    if( value == 7):
        mode = cv2.COLOR_BGR2XYZ
def oas():
    plt.cla()
    global mode
    try:
        sfname = filedialog.askopenfilename(title='選擇',filetypes=[('All Files','*'),("jpeg files","*.jpg"),("png files","*.png"),("gif files","*.gif")])
        cv2image = cv2.cvtColor(cv2.resize(cv_imread(sfname),(500,250)),mode)
        (high,width,path) = cv2image.shape
        x = np.arange(0,256)
        y = np.zeros((256))
        for i in range(0,high):
            for j in range(0,width):
                y[cv2image[i,j]] += 1
        plt.bar(x,y,color="gray",align="center")
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        media.imgtk = imgtk
        media.configure(image=imgtk)
        canva.draw()
    except:
        print('no open file or no choose mode')
r1 = tk.Radiobutton(root,text = " bgr 、 rgb 互轉模式",variable=radioValue, value=1,command = validate).pack()
r2 = tk.Radiobutton(root,text = " hsv ",variable=radioValue, value=2,command = validate).pack()
r3 = tk.Radiobutton(root,text = " hls ",variable=radioValue, value=3,command = validate).pack()
r4 = tk.Radiobutton(root,text = " lab ",variable=radioValue, value=4,command = validate).pack()
r5 = tk.Radiobutton(root,text = " luv ",variable=radioValue, value=5,command = validate).pack()
r6 = tk.Radiobutton(root,text = " ycrcb ",variable=radioValue, value=6,command = validate).pack()
r7 = tk.Radiobutton(root,text = " xyz ",variable=radioValue, value=7,command = validate).pack()
b1 = tk.Button(root, text="打開",command = oas).pack()
root.mainloop()