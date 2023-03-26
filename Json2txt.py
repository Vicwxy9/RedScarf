import os
import json
import codecs
import shutil
import cv2

DATAROOT = './'
files = os.listdir(DATAROOT)


images_path = os.path.join(DATAROOT, 'images')
annotations_path = os.path.join(DATAROOT, 'labels')
jsons_path = os.path.join(DATAROOT, 'jsons')

json_files = os.listdir(jsons_path)
for json_file in json_files:
    json_path = os.path.join(jsons_path, json_file)

    names, xmins, ymins, xmaxs, ymaxs = [], [], [], [], []
    height, width = 0, 0
    file_id = json_file.split('.')[0]
    txt_path =  os.path.join(annotations_path, file_id + '.txt')
    with open(json_path, 'r', encoding='utf-8') as f:
        set = json.load(f)
        result = set['labels']
        num = len(result)
        for n in range(num):
            img = cv2.imread(os.path.join(images_path, json_file.split('.')[0]+".jpg"))  
            sp = img.shape[0:2]
            if n == 0:
                height = sp[0]
                width =  sp[1]

            dict = result[n]
            name = dict['name']
            xmin = round((dict['x1']/width+dict['x2']/width)/2,6)
            ymin = round((dict['y1']/height+dict['y2']/height)/2,6)
            xmax = round((dict['x2']-dict['x1'])/width,6)
            ymax = round((dict['y2']-dict['y1'])/height,6)

            with open(txt_path,'a')as txt:
                print('0',xmin,ymin,xmax,ymax,file=txt)