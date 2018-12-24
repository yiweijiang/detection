from skimage import io
import numpy as np
import math
import cv2
import time
import matplotlib.pyplot as plt

def blockNotes(image, indexi, indexj, size):
    for i in range(indexi,indexi+size):
        for j in range(indexj,indexj+size):
            image[i,j] = 128
    return image

def Filter(image,size):
    Block_Mean = []
    Block_Var = []
    Block_Num = {}
    count = 0
    rows, cols = image.shape
    for i in range(0,rows-size):
        for j in range(0,cols-size):
            moment = cv2.moments(image[i:i+size,j:j+size])
            sum = 0
            variance = 0
            for add in cv2.HuMoments(moment):
                sum = sum + add[0]
            mean = sum/7
            for add in cv2.HuMoments(moment):
                variance = variance + (add[0] - mean)**2          
            
            Block_Mean.append([mean,count])
            Block_Var.append([variance,count])
            Block_Num[str(count)] = {
                'x' : i,
                'y' : j,
                'mean' : mean,
                'var' : variance
            }
            count += 1
    return Block_Mean, Block_Var, Block_Num

def Dectection(SortedVar,size):
    New = []
    Match = []
    Match_ary = []
    for block in SortedVar:
        New.append(Block_Num[str(block[1])])
    for index in range(2,len(New)-2):
        cout = 0
        for i in range(index-1,index+2):
            if New[i]['mean'] == New[index]['mean'] and i != index:
                x_1 = New[index]['x']
                y_1 = New[index]['y']
                moment_1 = cv2.moments(img[x_1:x_1+size,y_1:y_1+size])
                phi_1 = cv2.HuMoments(moment_1)            

                x_2 = New[i]['x']
                y_2 = New[i]['y']
                moment_2 = cv2.moments(img[x_2:x_2+size,y_2:y_2+size])
                phi_2 = cv2.HuMoments(moment_2)

                d_inv_m = 0
                for id in range(0,7):
                    d_inv_m = d_inv_m + ((phi_1[id][0] - phi_2[id][0])**2)**0.5
                if d_inv_m <= 1**10:
                    Match.append([New[i]['x'],New[i]['y']])
                    if cout <= 0:
                        Match.append([New[index]['x'],New[index]['y']])
                        cout = cout + 1                   
            else:
                continue
        if Match != []:
            Match_ary.append(Match)
            Match = []
    return Match_ary

def copyMoveDetection(SortedVar,size):
    for match in Dectection(SortedVar,size):
        for l in range(0,len(match)):
            for k in range(0,len(match)):
                if l < k:
                    x1 = match[l][0]
                    y1 = match[l][1]
                    x2 = match[k][0]
                    y2 = match[k][1]   
                    
                    blockNotes(new_img,x1,y1,size)
                    blockNotes(new_img,x2,y2,size)          

start = time.time()
img = io.imread('bird_cp6.tif')
rows,cols = img.shape
new_img = np.zeros((rows,cols))

size = 8

Mean, Var, Block_Num = Filter(img,size)
SortedMean, SortedVar = sorted(Mean), sorted(Var)
copyMoveDetection(SortedVar,size)

plt.figure(num='copy move detection', figsize=(12,12))
plt.subplot(1,2,1)
plt.title('origin image')
plt.imshow(img, plt.cm.gray)

plt.subplot(1,2,2)
plt.title('detected result')
plt.imshow(new_img, plt.cm.gray)

end = time.time()

TIME = end - start
print('執行時間：'.format(),TIME, 'seconds')
