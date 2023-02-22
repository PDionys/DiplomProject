from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from GUI.utils import xml_to_csv as xtc
from GUI.utils import txt_to_csv as ttc
from GUI.utils import generate_tfrecord as gtfr
from pathlib import Path
import os

vlist = []
def createList():
    read_list = open("GUI/utils/classes_list", "r").readlines()

    for line in read_list:
        correct_line = line.replace("\n", "")
        vlist.append(correct_line)

class DatasetWindow:
    def __init__(self, root):
        self.image_path = ""
        self.label_path = ""
        self.root = root
        root.title("Object Detection Program")

        self.custom_dataset_frame = LabelFrame(root, text="Creating Dataset")
        self.custom_dataset_frame.grid(column=0, row=0)
        self.download_dataset_frame = LabelFrame(root, text="Downloading Dataset")
        self.download_dataset_frame.grid(column=0, row=1)

        '''Custom Dataset Frame'''
        Label(self.custom_dataset_frame, text="Create your custom dataset:", font=("Arial", 18)).grid(column=0, row=0, columnspan=3)
        Button(self.custom_dataset_frame, text="Create", font=("Arial", 18), padx=40, command=self.createClick).grid(column=1, row=1)
        Button(self.custom_dataset_frame, text="Xml to Csv", font=("Arial", 18), padx=40 ,command=self.xml_to_csvClick).grid(column=0, row=2)
        Button(self.custom_dataset_frame, text="Generate TFRecord", font=("Arial", 18), command=self.generateTFRecodsClick).grid(column=3, row=2)
        '''Download Dataset Frame'''
        Label(self.download_dataset_frame, text="Download dataset:", font=("Arial", 18)).grid(column=0, row=0, columnspan=3)
        Button(self.download_dataset_frame, text="Download", font=("Arial", 18), command=self.downloadClick).grid(column=1, row=1)
        Button(self.download_dataset_frame, text="Txt to Csv", font=("Arial", 18), command=self.txt_to_csvClick).grid(column=0, row=2)
        Button(self.download_dataset_frame, text="Generate TFRecord", font=("Arial", 18), command=self.generateTFRecodsClick).grid(column=3, row=2)

    def downloadClick(self):
        downlod_win = Tk()

        downlod_win.eval('tk::PlaceWindow . center')
        DownloadWindow(downlod_win)

        downlod_win.mainloop()

    def generateTFRecodsClick(self):
        generate_win = Tk()

        generate_win.eval('tk::PlaceWindow . center')
        GenerateTFRecordsWindow(generate_win)

        generate_win.mainloop()

    def createClick(self):
        os.system("python labelImg/labelImg.py")

    def xml_to_csvClick(self):
        #Баг - если во время выбора папки просто закрить окно то всеровно происходит процесс
        xtc.execute(askdirectory())
        self.trainCheck()

    def trainCheck(self):
        root = Tk()
        root.eval('tk::PlaceWindow . center')
        if (Path('img/train_labels.csv').is_file()):
            Label(root, text="Successfully converted xml to csv!", font=("Arial", 18)).pack()
        else:
            Label(root, text="Xml to csv has not converted! Please try again!", font=("Arial", 18)).pack()
        Button(root, text="OK", font=("Arial", 18), command=root.destroy).pack()
        root.mainloop()


    def txt_to_csvClick(self):
        def setLableClick():
            self.label_path = askdirectory()
            e1.delete(0, END)
            e1.insert(0, self.label_path)

        def setImageClick():
            self.image_path = askdirectory()
            e2.delete(0, END)
            e2.insert(0, self.image_path)

        window = Toplevel()
        def ttc_execute():
            ttc.execute(self.label_path, self.image_path)
            window.destroy()
            self.trainCheck()

        '''Label Dir'''
        Label(window, text="Label dir:", font=("Arial", 12)).grid(column=0, row=0)
        e1 = Entry(window, font=("Arial", 12), width=30)
        e1.grid(column=0, row=1)
        Button(window, text="Set", font=("Arial", 12), command=setLableClick).grid(column=1, row=1)
        '''Image Dir'''
        Label(window, text="Images dir:", font=("Arial", 12)).grid(column=0, row=2)
        e2 = Entry(window, font=("Arial", 12), width=30)
        e2.grid(column=0, row=3)
        Button(window, text="Set", font=("Arial", 12), command=setImageClick).grid(column=1, row=3)
        '''Apply/Cancel'''
        f = Frame(window)
        f.grid(column=0, row=4)
        Button(f, text="Apply", font=("Arial", 18), command=ttc_execute).grid(column=0, row=0)
        Button(f, text="Cancel", font=("Arial", 18), command=window.destroy).grid(column=1, row=0)

class DownloadWindow:
    def __init__(self, root):
        createList()
        self.class_ = ""
        self.limit_ = ""
        self.root = root
        root.title("Object Detection Program")

        Label(root, text="Download settings:", font=("Arial", 18)).grid(column=0, row=0)

        self.entryframe = ttk.Frame(root)
        self.entryframe.grid(column=0, row=1)
        self.buttonframe = ttk.Frame(root)
        self.buttonframe.grid(column=0, row=2)

        Label(self.entryframe, text="Classes", font=("Arial", 12)).grid(column=0, row=0)
        self.Combo = ttk.Combobox(self.entryframe, font=("Arial", 12), values=vlist)
        self.Combo.set("Pick a class")
        self.Combo.grid(column=0, row=1)
        Button(self.entryframe, text="Set", font=("Arial", 12), padx=20, command=self.setClassesClick).grid(column=1, row=1)

        Label(self.entryframe, text="Limit", font=("Arial", 12)).grid(column=0, row=2)
        self.Entry = ttk.Entry(self.entryframe, font=("Arial", 12))
        self.Entry.grid(column=0, row=3)
        Button(self.entryframe, text="Set", font=("Arial", 12), padx=20, command=self.setLimitClick).grid(column=1, row=3)

        Button(self.buttonframe, text="Apply", font=("Arial", 18), command=self.applyClick).grid(column=0, row=0)
        Button(self.buttonframe, text="Cancel", font=("Arial", 18), command=root.destroy).grid(column=1, row=0)

    def setClassesClick(self):
        self.class_ = self.Combo.get()
    def setLimitClick(self):
        self.limit_ = self.Entry.get()

    def applyClick(self):
        command = "python oid.py downloader --classes " + self.class_ + " --type_csv train --limit " + self.limit_
        os.system(command)
        self.root.destroy()

class GenerateTFRecordsWindow:
    def __init__(self, root):
        self.csv_input = "D:/DiplomProject/img/train_labels.csv"
        self.output_path = "D:/DiplomProject/img/train.record"
        self.image_dir = ""
        self.root = root
        root.title("Object Detection Program")

        '''Path to the CSV input'''
        Label(root, text='Path to the CSV', font=("Arial", 12)).grid(column=0, row=0)
        self.csv_e = Entry(root, font=("Arial", 12), width=30)
        self.csv_e.insert(0, self.csv_input)
        self.csv_e.grid(column=0, row=1)
        Button(root, text='Set', font=("Arial", 12), padx=20, command=self.setCsvClick).grid(column=1, row=1)
        '''Path to images'''
        Label(root, text='Path to images', font=("Arial", 12)).grid(column=0, row=2)
        self.image_dir_e = Entry(root, font=("Arial", 12), width=30)
        self.image_dir_e.grid(column=0, row=3)
        Button(root, text='Set', font=("Arial", 12), padx=20, command=self.setImgClick).grid(column=1, row=3)
        '''Buttons Apply/Cancel'''
        self.f = Frame(root)
        self.f.grid(column=0,row=4)
        Button(self.f, text="Apply", font=("Arial", 18), command=self.applyClick).grid(column=0, row=0)
        Button(self.f, text="Cancel", font=("Arial", 18), command=root.destroy).grid(column=1, row=0)

    def setCsvClick(self):
        self.csv_input = askopenfilename()
        self.clearAndWriteEntry(self.csv_input, self.csv_e)

    def setImgClick(self):
        self.image_dir = askdirectory()
        self.clearAndWriteEntry(self.image_dir, self.image_dir_e)

    def applyClick(self):
        command = "python GUI/utils/generate_tfrecord.py --csv_input=" + self.csv_input + " --output_path=" + self.output_path + " --image_dir=" + self.image_dir
        os.system(command)
        self.root.destroy()

    def clearAndWriteEntry(self, string, entry):
        entry.delete(0, END)
        entry.insert(0, string)