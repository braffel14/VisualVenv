import os.path
from os import path
import subprocess
import tkinter as tk
from tkinter import font
import json

WIDTH = 1000
HEIGHT = 700

script_dir = os.path.dirname(__file__)


def main():
    """Main method to run with GUI"""
    root = tk.Tk()

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    root.mainloop()


def climain():
    """Main method to run through command line interface"""

    #get filepath of project and save to text file
    print('Enter filepath for project')
    projectpath = input()
    #check that venv exists
    if checkforvenv(projectpath, script_dir):
        getpackages(projectpath, script_dir)
    else: #create new venv
        print('Virtual environment does not exist. Would you like to create a new one?')
        print('y or n?')
        createresponse = input()
        if createresponse == 'y':
            try:
                cmd = subprocess.call([str(os.path.join(script_dir, '../bin/createvenv.sh')), projectpath], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                getpackages(projectpath, script_dir)
            except subprocess.CalledProcessError as exc:
                print("Could not find venv")
                print("Status : FAIL", exc.returncode, exc.output)


def getpackages(projectpath, script_dir):
    getInstalledTxt(projectpath, script_dir)
    jsonifypackages()


def checkforvenv(projectpath, script_dir):
    return path.exists(os.path.join(projectpath, 'venv'))


def getInstalledTxt(projectpath, script_dir):
    """Takes a filepath to a Python project and runs a shell script to generate a text file of that project's venv's installed packages"""
    
    savepath = os.path.join(script_dir, '../tempfiles/installed.txt')
    #call script to get installed packages
    try:
        cmd = subprocess.call([str(os.path.join(script_dir, '../bin/getpackages.sh')), projectpath, savepath], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        print("Could not find venv")
        print("Status : FAIL", exc.returncode, exc.output)

def jsonifypackages():
    """gets generated text file of packages from the getpackages.sh script and creates a json file of packages"""
    txtpath = os.path.join(script_dir, '../tempfiles/installed.txt')
    jsonpath = os.path.join(script_dir, '../tempfiles/installed.json')
    packagesdict = {}
    try:
        txt = open(txtpath, 'r')
        #read textfile of packages
        lines = txt.readlines()
        for line in lines:
            #filter out header lines of package textfile
            if line != 'Package    Version\n' and line != '---------- -------\n':
                #remove formatting of text file
                splitline = line.split(' ')
                splitline.remove('\n')
                while("" in splitline) : 
                     splitline.remove("")
                #add package to packages dict
                packagesdict[splitline[0]] = splitline[1]
        with open(jsonpath, 'w') as json_file:
            json.dump(packagesdict, json_file)
    finally:
        txt.close()
        print(packagesdict)



if __name__ == '__main__':
    #main()
    climain()
