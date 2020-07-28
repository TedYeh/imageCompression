import cv2
import numpy as np
import math
import test

def DCT(N,X1):
    A = []
    for i in range(N):
        A.append([])
        for j in range(N):
            A[i].append(np.power(1/N,0.5)*np.cos(((2*j+1)*i*np.pi)/(2*N)))
    A = np.array(A)    
    Y = np.dot(np.dot(A,X1),np.linalg.inv(A))
    return np.round(Y).astype(int)

def zig_zag(input_matrix,block_size):
    z = np.empty([block_size*block_size])
    index = -1
    bound = 0
    for i in range(0, 2 * block_size -1):
        if i < block_size:
            bound = 0
        else:
            bound = i - block_size + 1
        for j in range(bound, i - bound + 1):
            index += 1
            if i % 2 == 1:
                z[index] = input_matrix[j, i-j]
            else:
                z[index] = input_matrix[i-j, j]
    return z

def find_nearest(array, value): 
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
    
def scalar(arr,m):
    interval = get_interval(m)
    compress = []
    n = 0
    for i in arr:
        compress.append([])
        for j in i:
            tmp = find_nearest(interval,j)
            if j > interval[tmp] and tmp<(m-1):compress[n].append(tmp+1)
            else:compress[n].append(tmp)
        n += 1
    
    return np.array(compress)

def get_interval(m):
    step = 256//m
    interval = []
    for i in range(m):
        interval.append(step * (i+1))
    return interval

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

def iDCT(N,X1):
    A = []
    for i in range(N):
        A.append([])
        for j in range(N):
            A[i].append(np.power(1/N,0.5)*np.cos(((2*j+1)*i*np.pi)/(2*N)))
    A = np.array(A)    
    B = np.linalg.inv(A)
    Y = np.dot(np.dot(B,X1),np.linalg.inv(B))
    return np.round(Y)

def descalar(arr,img,m): 
    
    n = 0
    com_scalar = [(256//m)//2]
    decompress = []
    for i in range(0,len(img)-1):
        com_scalar.append((img[i]+img[i+1])//2)
    for i in arr:
        decompress.append([])
        for j in i:
            decompress[n].append(com_scalar[j])
        n += 1   
    return np.array(decompress)

def zig_zag_reverse(input_matrix,block_size):
    output_matrix = np.empty([block_size,block_size])
    index = -1
    bound = 0
    for i in range(0, 2 * block_size -1):
        if i < block_size:
            bound = 0
        else:
            bound = i - block_size + 1
        for j in range(bound, i - bound + 1):
            index += 1
            if i % 2 == 1:
                output_matrix[j, i - j] = input_matrix[index]
            else:
                output_matrix[i - j, j] = input_matrix[index]
    return output_matrix
