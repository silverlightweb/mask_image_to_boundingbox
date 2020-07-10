import cv2
import argparse
import os
def extend_box(img,pos):
    h_origin, w_origin, _ = img.shape
    
    crop_img = img[int(pos[1]):int(pos[3]),int(pos[0]):int(pos[2])]
    h, w, _ = crop_img.shape
    if h/w >= 2:
        h_percent = 0.30
        w_percent = 0.30 * 2
    elif h/w >= 1 and h/w < 2:
        h_percent = 0.10
        w_percent = 0.30 * 1.5
    else:
        h_percent = 0.30
        w_percent = 0.30 * 2

    # if pos[0] - w * w_percent > 0:
    #     pos[0] = pos[0] - w * w_percent        
    # else:
    #     pos[0] = 0
        
    if pos[1] - h * h_percent > 0:
        pos[1] = pos[1] - h * h_percent
    else:
        pos[1] = 0

    if pos[2] + w * w_percent < w_origin :
        pos[2] = pos[2] + w * w_percent
    else:
        pos[2] = w_origin

    if pos[3] + h * h_percent < h_origin :
        pos[3] = pos[3] + h * h_percent
    else:
        pos[3] = h_origin
    return  (int(pos[0]),int(pos[1]),int(pos[2]),int(pos[3]))
def writeYolo_annotation(x,y,w,h,imgW,imgH,img_name):
    filename = img_name.split('.')[0]
    if x <= 0.0:
        x = 0.001
    if y <= 0.0:
        y = 0.001
    if w <= 0.0:
        w = 0.001
    if h <= 0.0:
        h = 0.001
    #print(cx, cy, cw, ch)
    cx=x+0.5*w
    cy=y+0.5*h
    vocX=cx/imgW
    vocY=cy/imgH
    vocW=w/imgW
    vocH=h/imgH
    
    if vocX <= 0.0:
        print('x'+str(filename))
    if vocY <= 0.0:
        print('y'+str(filename))
    if vocW <= 0.0:
        print('w'+str(filename))
    if vocH <= 0.0:
        print('h'+str(filename))
    # if int(s[8]) >0 :
    f1=open(str(filename)+'.txt','a')
    f1.write('0'+' ')
    f1.write('{:f} '.format(vocX))
    f1.write('{:f} '.format(vocY))
    f1.write('{:f} '.format(vocW))
    f1.write('{:f}'.format(vocH))			
    f1.write('\n')
def progress_each_file(img_name):
    # img_name = '1312132815-0008-G_gt.tif'
    image = cv2.imread(img_name)
    image2 = cv2.imread(img_name)
    W = 2592
    H = 1944
    copy = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    ROI_number = 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ROI = image[y:y+h, x:x+w]
        x1,y1,x2,y2 = extend_box(image2,[x,y,x+w,y+h])
        # print(x,y,x+w,y+h)
        new_W = x2-x1
        new_H = y2-y1
        writeYolo_annotation(x1,y1,new_W,new_H,W,H,img_name)
        # cv2.rectangle(image2,(x1,y1),(x2,y2),(36,255,12),2)       
        ROI_number += 1
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', default="D:/tools/source",type=str)    
    opt = parser.parse_args()
    list_imgs = os.listdir(opt.image_dir)
    for img in list_imgs:
        progress_each_file(os.path.join(opt.image_dir,img))
    # cv2.imwrite('ROI_{}.png'.format(ROI_number), image2)
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('copy', copy)
    # cv2.waitKey()
