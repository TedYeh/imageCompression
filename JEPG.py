import cv2
import numpy as np
import math
import os
from im_compression import *
from huffman_compressor import * 

def get_run_length_encoding(image):
    i = 0
    skip = 0
    stream = []    
    bitstream = ""
    image = image.astype(int)
    while i < image.shape[0]:
        if image[i] != 0:            
            stream.append((image[i],skip))
            bitstream = bitstream + str(image[i])+ " " +str(skip)+ " "
            skip = 0
        else:
            skip = skip + 1
        i = i + 1

    return bitstream

def imgcompress(file,block_size,flag):
    img = cv2.imread(file,cv2.IMREAD_GRAYSCALE) if flag else cv2.imread(file)
    QUANTIZATION_MAT = np.array([[16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],[14,13,16,24,40,57,69,56 ],[14,17,22,29,51,87,80,62],[18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92],[49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]])
    if flag:[h , w ] = img.shape
    else:[h , w , n] = img.shape
    height = h
    width = w
    num = 1 if flag else n
    h = np.float32(h) 
    w = np.float32(w) 
    
    nbh = math.ceil(h/block_size)
    nbh = np.int32(nbh)
    
    nbw = math.ceil(w/block_size)
    nbw = np.int32(nbw)
    
    H =  block_size * nbh
    
    N = num
    
    W =  block_size * nbw
    
    padded_img = np.zeros((H,W)) if flag else np.zeros((H,W,N))
    if flag:padded_img[0:height,0:width] = img[0:height,0:width]
    else:padded_img[0:height,0:width,0:num] = img[0:height,0:width,0:num]
    
    for k in range(num):
        
        for i in range(nbh):
            
                
                row_ind_1 = i*block_size                
                row_ind_2 = row_ind_1+block_size
                
                for j in range(nbw):
                    
                   
                    col_ind_1 = j*block_size                       
                    col_ind_2 = col_ind_1+block_size
                                
                    block = padded_img[ row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2 ] if flag else padded_img[ row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2 ,k]
                       
                    dct = DCT(block_size,block)            
                    
                    DCT_normalized = np.divide(dct,QUANTIZATION_MAT).astype(int)          
                    
                    
                    reordered = zig_zag(DCT_normalized,block_size)
        
                   
                    reshaped= np.reshape(reordered, (block_size, block_size)) 
                    
                    if flag:padded_img[row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2] = reshaped 
                    else:padded_img[row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2,k] = reshaped 
                                     
    
    
    
    arranged = padded_img.flatten()
    
    
    bitstream = get_run_length_encoding(arranged)
    
    
    if flag:bitstream = str(padded_img.shape[0]) + " " + str(padded_img.shape[1]) + " " + bitstream + ";"
    else:bitstream = str(padded_img.shape[0]) + " " + str(padded_img.shape[1]) + " " + str(padded_img.shape[2]) + " " + bitstream + ";"
    
    
    file1 = open("image.txt","w")
    file1.write(bitstream)
    file1.close()
    compress("image.txt", "compressed.bin")
    return img

def decompress(block_size,flag):
    QUANTIZATION_MAT = np.array([[16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],[14,13,16,24,40,57,69,56 ],[14,17,22,29,51,87,80,62],[18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92],[49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]])
    with open('image.txt', 'r') as myfile:
        image=myfile.read()
        
    details = image.split()
    h = int(''.join(filter(str.isdigit, details[0])))
    w = int(''.join(filter(str.isdigit, details[1])))
    n = 1 if flag else int(''.join(filter(str.isdigit, details[2])))
    
    array = np.zeros(h*w).astype(int) if flag else np.zeros(h*w*n).astype(int)
    
    
    k = 0
    i = 2 if flag else 3
    j = 0
    
    while k < array.shape[0]:
    
        if(details[i] == ';'):
            break
    
        if "-" not in details[i]:
            array[k] = int(''.join(filter(str.isdigit, details[i])))        
        else:
            array[k] = -1*int(''.join(filter(str.isdigit, details[i])))        
    
        if(i+3 < len(details)):
            j = int(''.join(filter(str.isdigit, details[i+3])))
    
        if j == 0:
            k = k + 1
        else:                
            k = k + j + 1        
    
        i = i + 2

    array = np.reshape(array,(h,w)) if flag else np.reshape(array,(h,w,n))
    
    
    l = 0
    i = 0
    j = 0
    k = 0

    padded_img = np.zeros((h,w)) if flag else np.zeros((h,w,n))
    while l < n:
        i = 0
        while i < h:
            j = 0
            while j < w:
                if flag:temp_stream = array[i:i+8,j:j+8] 
                else:temp_stream = array[i:i+8,j:j+8,l]                
                block = zig_zag_reverse(temp_stream.flatten(),block_size)  
                de_quantized = np.multiply(block,QUANTIZATION_MAT)                 
                if flag:padded_img[i:i+8,j:j+8] = iDCT(block_size,de_quantized)  
                else:padded_img[i:i+8,j:j+8,l] = iDCT(block_size,de_quantized)        
                j = j + 8        
            i = i + 8
            
        l = l + 1

    padded_img[padded_img > 255] = 255
    padded_img[padded_img < 0] = 0
    cv2.imwrite("compressed_image.jpg",np.uint8(padded_img))
    return padded_img
    
def MSE(data,new_data,flag): 
    if flag: return np.square(np.subtract(data,new_data)).mean()
    else:
        a = []
        b = []
        c = []
        tmp = np.square(np.subtract(data,new_data))
        for i in tmp:
            for j in i:
                a.append(j[0])
                b.append(j[1])
                c.append(j[2])
        
        
        MSEr = np.mean(a)
        MSEg = np.mean(b)
        MSEb = np.mean(c)
        return (MSEr,MSEg,MSEb)

#Get file size  
def get_file_size(filename):
    return os.path.getsize(str(filename))
       
    #Get compress ratio    
def get_ratio(image,txt):    
    after = get_file_size(txt)
    before = get_file_size(image)
    return float(after/before)

'''block_size = 8
a = compress('LenaRGB.bmp',block_size,False)
b = decompress(block_size,False)
print(MSE(a,b,False))'''








    




