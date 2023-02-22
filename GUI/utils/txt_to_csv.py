import os
import os.path
import argparse
import pandas as pd
from PIL import Image

def write_to_csv(label_path, image_path):
    annos = []
    for files in os.listdir(label_path):

        '''Read image and take W/H'''
        image_name = files.replace(".txt", ".jpg")
        fileimgpath = image_path + "/" + image_name
        im = Image.open(fileimgpath)
        w = int(im.size[0])
        h = int(im.size[1])
        # print("{},{}".format(w, h))

        '''Read txt file'''
        filelabel = open(os.path.join(label_path, files), "r")
        lines = filelabel.read().split('\n')
        obj = lines[:len(lines) - 1]
        for i in range(0, int(len(obj))):
            objbud = obj[i].split(' ')
            name = objbud[0].lower()

            x1 = float(objbud[1])
            y1 = float(objbud[2])
            x2 = float(objbud[3])
            y2 = float(objbud[4])

            xmin = int(x1)
            ymin = int(y1)
            xmax = int(x2)
            ymax = int(y2)

            annos.append([image_name, w, h, name, xmin, ymin, xmax, ymax])

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    df = pd.DataFrame(annos, columns=column_name)
    return df

def execute(label_path, image_path):
    data = write_to_csv(label_path, image_path)
    data.to_csv("D:/DiplomProject/img/train_labels.csv", index=None)


# execute("D:/DiplomProject/img/Dataset/train/Flower/Label", "D:/DiplomProject/img/Dataset/train/Flower")