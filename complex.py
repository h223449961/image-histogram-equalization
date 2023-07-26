# -*- coding: utf-8 -*-
import cv2
import numpy as np
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
def histogram_equalization(inputphoto):
    '''
    按照 b 、 g 、 r （藍、綠、紅）的順序剝離出三通道
    '''
    b, g, r = cv2.split(inputphoto)
    '''
    取得代表 y 軸的 pixel 值
    '''
    yb, xb = np.histogram(b.flatten(), 256, [0, 256])
    yg, xg = np.histogram(g.flatten(), 256, [0, 256])
    yr, xr = np.histogram(r.flatten(), 256, [0, 256])
    '''
    加總 pixel 值
    '''
    cdf_b = np.cumsum(yb)
    cdf_g = np.cumsum(yg)
    cdf_r = np.cumsum(yr)
    '''
    去除零
    '''
    cdf_m_b = np.ma.masked_equal(cdf_b, 0)
    cdf_m_b = (cdf_m_b - cdf_m_b.min()) * 255 / (cdf_m_b.max() - cdf_m_b.min())
    cdf_final_b = np.ma.filled(cdf_m_b, 0).astype('uint8')
    cdf_m_g = np.ma.masked_equal(cdf_g, 0)
    cdf_m_g = (cdf_m_g - cdf_m_g.min()) * 255 / (cdf_m_g.max() - cdf_m_g.min())
    cdf_final_g = np.ma.filled(cdf_m_g, 0).astype('uint8')
    cdf_m_r = np.ma.masked_equal(cdf_r, 0)
    cdf_m_r = (cdf_m_r - cdf_m_r.min()) * 255 / (cdf_m_r.max() - cdf_m_r.min())
    cdf_final_r = np.ma.filled(cdf_m_r, 0).astype('uint8')
    img_b = cdf_final_b[b]
    img_g = cdf_final_g[g]
    img_r = cdf_final_r[r]
    outputphoto = cv2.merge((img_b, img_g, img_r))
    return outputphoto
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img
def opfile():
    plt.figure(0).clear()
    fname = filedialog.askopenfilename(title='選擇',filetypes=[('All Files','*'),("jpeg files","*.jpg"),("png files","*.png"),("gif files","*.gif")])
    cvoriphoto = cv2.cvtColor(cv2.resize(cv_imread(fname),(500,170)),cv2.COLOR_BGR2RGB)
    oriy = np.zeros((256))
    for i in range(0,cvoriphoto.shape[0]):
        for j in range(0,cvoriphoto.shape[1]):
            oriy[cvoriphoto[i,j]] += 1
    plt.figure(0)
    plt.bar(np.arange(0,256),oriy,color="gray",align="center")
    oricanva.draw()
    oriphoto = Image.fromarray(cvoriphoto)
    oriimgtk = ImageTk.PhotoImage(image=oriphoto)
    orilabel.imgtk = oriimgtk
    orilabel.configure(image=oriimgtk)
    return fname
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
def oas(filename):
    plt.figure(1).clear()
    plt.figure(2).clear()
    global mode
    cvtranphoto = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,170)),mode)
    trany = np.zeros((256))
    for i in range(0,cvtranphoto.shape[0]):
        for j in range(0,cvtranphoto.shape[1]):
            trany[cvtranphoto[i,j]] += 1   
    plt.figure(1)
    plt.bar(np.arange(0,256),trany,color="blue",align="center")
    trancanva.draw()
    tranphoto = Image.fromarray(cvtranphoto)
    tranimgtk = ImageTk.PhotoImage(image=tranphoto)
    tranlabel.imgtk = tranimgtk
    tranlabel.configure(image = tranimgtk)
    eqpho = histogram_equalization(cvtranphoto)
    eqy = np.zeros((256))
    for i in range(0,eqpho.shape[0]):
        for j in range(0,eqpho.shape[1]):
            eqy[eqpho[i,j]] += 1
    plt.figure(2)
    plt.bar(np.arange(0,256),eqy,color="red",align="center")
    eqcanva.draw()
    eqphoto = Image.fromarray(eqpho)
    eqimgtk = ImageTk.PhotoImage(image=eqphoto)
    eqlabel.imgtk = eqimgtk
    eqlabel.configure(image = eqimgtk)
def oand():
    filename = opfile()
    oas(filename)
def main():
    root = tk.Tk()
    global radioValue
    radioValue = tk.IntVar()
    oriFrame = tk.Frame(root).pack()
    global orilabel
    orilabel = tk.Label(oriFrame)
    orilabel.pack()
    tranFrame = tk.Frame(oriFrame).pack()
    global tranlabel
    tranlabel = tk.Label(oriFrame)
    tranlabel.pack()
    eqFrame = tk.Frame(oriFrame).pack()
    global eqlabel
    eqlabel = tk.Label(oriFrame)
    eqlabel.pack() 
    orifig = plt.figure(0)
    oriplot =orifig.add_subplot(111)
    global oricanva
    oricanva = FigureCanvasTkAgg(orifig,root)
    oricanva.get_tk_widget().pack(side='left')
    tranfig = plt.figure(1)
    tranplot =tranfig.add_subplot(111)
    global trancanva
    trancanva = FigureCanvasTkAgg(tranfig,root)
    trancanva.get_tk_widget().pack(side='left')
    eqfig = plt.figure(2)
    eqplot =eqfig.add_subplot(111)
    global eqcanva
    eqcanva = FigureCanvasTkAgg(eqfig,root)
    eqcanva.get_tk_widget().pack(side='left')
    r1 = tk.Radiobutton(root,text = " bgr 、 rgb 互轉模式",variable=radioValue, value=1,command = validate).place(x = 0, y = 0)
    r2 = tk.Radiobutton(root,text = " hsv ",variable=radioValue, value=2,command = validate).place(x = 0, y = 20)
    r3 = tk.Radiobutton(root,text = " hls ",variable=radioValue, value=3,command = validate).place(x = 0, y = 40)
    r4 = tk.Radiobutton(root,text = " lab ",variable=radioValue, value=4,command = validate).place(x = 133, y = 0)
    r5 = tk.Radiobutton(root,text = " luv ",variable=radioValue, value=5,command = validate).place(x = 133, y = 20)
    r6 = tk.Radiobutton(root,text = " ycrcb ",variable=radioValue, value=6,command = validate).place(x = 133, y = 40)
    r7 = tk.Radiobutton(root,text = " xyz ",variable=radioValue, value=7,command = validate).place(x = 199, y = 0)
    b1 = tk.Button(root, text="打開",command = oand).place(x = 199, y = 20)
    root.mainloop()
if __name__=='__main__':
    main()