# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 01:32:46 2020

@author: islab
"""

from JEPG import *
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from matplotlib import pyplot as plt

def read():
    options = {}
    options['multiple'] = True
    options['title'] = "tkFileDialog.askopenfilename"
    filename = askopenfilename(**options)[0]
    path.set(filename)

def f():
    block_size = 8
    flag = True if DVar.get() == "GRAY" else False 
    filename = path.get()
    a = imgcompress(filename,block_size,flag)
    b = decompress(block_size,flag) 
    s = filename.split('/')
    window.title(s[len(s)-1])
    size = (b.shape[1] if(b.shape[1]<=256) else int(b.shape[1]/2), b.shape[0] if(b.shape[0]<=256) else int(b.shape[0]/2))
    img = ImageTk.PhotoImage(Image.open(filename).resize(size),Image.ANTIALIAS)    
    img2 = ImageTk.PhotoImage(Image.open('compressed_image.jpg').resize(size),Image.ANTIALIAS)    
    if flag:plt.imshow((a[0:8,0:8]* 255).astype(np.uint8), interpolation='nearest', cmap='gray')  
    else:plt.imshow((a[0:8,0:8]* 255).astype(np.uint8), interpolation='nearest')
    plt.show()
    if flag:plt.imshow((b[0:8,0:8]* 255).astype(np.uint8), interpolation='nearest', cmap='gray')  
    else:plt.imshow((b[0:8,0:8]* 255).astype(np.uint8), interpolation='nearest')
    plt.show()
    orgin.config(image=img)
    orgin.image = img
    compressed.config(image=img2)
    compressed.image = img2
    unsize.config(text = str("the orgin size is {0:.2f} KB".format(get_file_size(filename)/1024)))
    csize.config(text = str("the compressed size is {0:.2f} KB".format(get_file_size('compressed.bin')/1024)))
    com.config(text = "the compress ratio is {0:.2f}%".format(get_ratio(filename,'compressed.bin')*100))
    mse = MSE(a,b,flag)
    
    if flag:distortion.config(text = str("the distortion ratio is {0:.2f}".format(mse)))
    else:
        r=mse[0]
        g=mse[1]
        b=mse[2]
        print(r,g,b)
        distortion.config(text = str("the distortion ratio is {0:.2f}".format(r)+",{0:.2f}".format(g)+",{0:.2f}".format(b)))
    window.update()

window = Tk()
window.title(' ')
window.geometry('800x600')
main = Frame(window, relief = GROOVE)
photo = Frame(window, relief = GROOVE)
ratio = Frame(window, relief = GROOVE,height = 100)

name = Label(main,text = "Input your image name：")
name.grid(row = 0,column = 0)

path=StringVar()
fileinput = Entry(main,text=path)
fileinput.grid(row = 0,column = 1)

iSgray = Label(main,text = "Choose the classify of image：")
iSgray.grid(row = 1,column = 0)

DVar = StringVar()
D = Combobox(main,textvariable=DVar,values=["GRAY","RGB"])
D.grid(row = 1,column = 1)

orgin = Label(photo) 
orgin.grid(row = 0,column = 0) 

compressed = Label(photo) 
compressed.grid(row = 1,column = 0)

com = Label(ratio)
com.grid(row = 2,column = 0)

distortion = Label(ratio)
distortion.grid(row = 3,column = 0)

unsize = Label(ratio)
unsize.grid(row = 0,column = 0)

csize = Label(ratio)
csize.grid(row = 1,column = 0)

read_f = Button(main,text='Select',command=read)
read_f.grid(row = 0,column = 2)

sent = Button(main,text='Confirm',command=f )
sent.grid(row = 1,column = 2)

main.grid(row=0,column=0)
photo.grid(row=1,column=0)
ratio.grid(row=1,column=1)
window.mainloop()
 
