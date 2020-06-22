import tkinter as tk
from tkinter import font
import subprocess
import os.path

WIDTH = 1000
HEIGHT = 700

script_dir = os.path.dirname(__file__)


def main():
    root = tk.Tk()

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    root.mainloop()

def climain():
    #get filepath of project and save to text file
    print('Enter filepath for project')
    projectpath = input()
    savepath = os.path.join(script_dir, '../tempfiles/installed.txt')
    #call script to get installed packages
    subprocess.call([str(os.path.join(script_dir, '../bin/getpackages.sh')), projectpath, savepath])


    


    


if __name__ == '__main__':
    #main()
    climain()