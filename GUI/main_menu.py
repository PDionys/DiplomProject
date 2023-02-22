from tkinter import *
from tkinter import ttk
from GUI import dataset_win as dw

class MainMenu:
    def __init__(self, root):
        root.title("Object Detection Program")

        Label(root, text="Object Detection Program", font=("Arial", 25)).grid(column=0, row=0, columnspan=3)

        Button(root, text="Detect Object", font=("Arial", 18)).grid(column=0, row=2)
        Button(root, text="Dataset", font=("Arial", 18), padx=30, command=self.datasetClick).grid(column=1, row=2)
        Button(root, text="Exit", font=("Arial", 18), padx=40, command=root.destroy).grid(column=2, row=2)

    def datasetClick(self):
        dataset_win = Tk()

        dataset_win.eval('tk::PlaceWindow . center')
        dw.DatasetWindow(dataset_win)

        dataset_win.mainloop()