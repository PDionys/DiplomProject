from GUI import main_menu as mm
from tkinter import *

def main():
    mainmenu = Tk()

    # mainmenu.geometry("800x400")
    mainmenu.eval('tk::PlaceWindow . center')
    mm.MainMenu(mainmenu)

    mainmenu.mainloop()

main()
