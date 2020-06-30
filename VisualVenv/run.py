import os.path
from os import path
import subprocess
import tkinter as tk
from tkinter import font
import json
from flask import Flask

app = Flask(__name__)


WIDTH = 1000
HEIGHT = 700
LARGE_FONT = ("Verdana", 12)
BG_COLOR = "#61A0FF"
FONT = "Roboto"

script_dir = os.path.dirname(__file__)
projectpath = ""


@app.route("/")
def index():
    return "Hello, World!"


def main():
    """Main method to run with GUI"""
    global projectpath
    gui = GUI()
    gui.mainloop()
    projectpath = ""


# to be removed
class GUI(tk.Tk):
    """tkinter object that runs entire gui"""

    def __init__(self):
        tk.Tk.__init__(self)  # initilize tkinter
        self._frame = None
        self.canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH)
        self.canvas.pack()
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """swtiches view in gui window to different page"""

        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(relwidth=1, relheight=1)


# to be removed
class StartPage(tk.Frame):
    """first page to be displayed on GUI startup"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)  # initialize main frame of page
        self.parent = parent
        self.buildbody()

    def buildbody(self):
        """sets the body of the page"""

        upperframe = tk.Frame(self, bg=BG_COLOR, bd=5)
        upperframe.place(relwidth=0.75, relheight=0.1, relx=0.5, rely=0.1, anchor="n")

        welcomelabel = tk.Label(
            upperframe, font=(FONT, 50), text="Welcome to VisualVenv"
        )
        welcomelabel.place(relwidth=1, relheight=1)

        lowerframe = tk.Frame(self, bg="green", bd=5)
        lowerframe.place(relwidth=0.75, relheight=0.5, relx=0.5, rely=0.3, anchor="n")

        pathentry = tk.Entry(lowerframe, width=30, font=(FONT, 25))
        pathentry.grid(row=0, column=0)

        openButton = tk.Button(
            lowerframe,
            text="Open",
            command=lambda: self.openVenvPage(pathentry, lowerframe),
        )
        openButton.grid(row=0, column=1)

    def openVenvPage(self, pathentry, lowerframe):
        """Checks if the project exists and switches page depending if there's a venv there or not"""

        global projectpath
        projectpath = pathentry.get()  # gets path from text entry
        if path.exists(projectpath):
            if checkforvenv(projectpath, script_dir):
                self.parent.switch_frame(VenvPage)
            else:
                self.parent.switch_frame(CreateVenvPage)
        else:  # flashes alert to user if path does not exist on system
            alert = tk.Label(
                lowerframe, font=(FONT, 25), text="Path does not exist. Try again."
            )
            alert.grid(row=1, column=2)


# to be removed
class CreateVenvPage(tk.Frame):
    """Page to be displayed if project does not have a venv"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)  # initialize main frame of page
        self.parent = parent
        self.buildbody()

    def buildbody(self):
        """sets body of the page"""

        global projectpath
        upperframe = tk.Frame(self, bg="green", bd=5)
        upperframe.place(relwidth=0.75, relheight=0.2, relx=0.5, rely=0.1, anchor="n")

        novenvlabel = tk.Label(
            upperframe,
            font=(FONT, 50),
            text="There is no venv at this path",
            bg=BG_COLOR,
        )
        novenvlabel.pack()
        createvenvlabel = tk.Label(
            upperframe,
            font=(FONT, 25),
            text="Would you like to create one?",
            bg=BG_COLOR,
        )
        createvenvlabel.pack()

        lowerframe = tk.Frame(self, bg="green", bd=5)
        lowerframe.place(relwidth=0.75, relheight=0.5, relx=0.5, rely=0.4, anchor="n")

        createvenvbutton = tk.Button(
            lowerframe,
            font=(FONT, 20),
            text="Create Venv",
            command=lambda: self.createvenv(),
        )
        createvenvbutton.pack()

    def createvenv(self):
        """creates a new venv at projectpath and switches the view to display the venv information"""

        global projectpath
        createNewVenv(projectpath, script_dir)
        self.parent.switch_frame(VenvPage)


# to be removed
class VenvPage(tk.Frame):
    """Page to be displayed to show venv information and manage packages"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)  # initialize main frame of page
        global projectpath
        getpackages(projectpath, script_dir)
        self.parent = parent
        self.buildbody()

    def buildbody(self):
        """sets the body of the page"""

        global projectpath
        upperframe = tk.Frame(self, bg="green", bd=5)
        upperframe.place(relwidth=0.75, relheight=0.2, relx=0.5, rely=0.1, anchor="n")


def climain():
    """Main method to run through command line interface"""

    # get filepath of project and save to text file
    print("Enter filepath for project")
    projectpath = input()
    # check that venv exists
    if checkforvenv(projectpath, script_dir):
        getpackages(projectpath, script_dir)
    else:  # create new venv
        print("Virtual environment does not exist. Would you like to create a new one?")
        print("y or n?")
        createresponse = input()
        if createresponse == "y":
            createNewVenv(projectpath, script_dir)


def createNewVenv(projectpath, script_dir):
    try:
        subprocess.call(
            [str(os.path.join(script_dir, "../bin/createvenv.sh")), projectpath],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        getpackages(projectpath, script_dir)
    except subprocess.CalledProcessError as exc:
        print("Could not find venv")
        print("Status : FAIL", exc.returncode, exc.output)


def getpackages(projectpath, script_dir):
    """Generates txt file and json file of packages installed in specified path"""

    getInstalledTxt(projectpath, script_dir)
    jsonifypackages()


def checkforvenv(projectpath, script_dir):
    """checks specified folder to see if there is a venv there"""

    return path.exists(os.path.join(projectpath, "venv"))


def getInstalledTxt(projectpath, script_dir):
    """Takes a filepath to a Python project and runs a shell script to generate a text file of that project's
     venv's installed packages
    """

    savepath = os.path.join(script_dir, "../tempfiles/installed.txt")
    # call script to get installed packages
    try:
        subprocess.call(
            [
                str(os.path.join(script_dir, "../bin/getpackages.sh")),
                projectpath,
                savepath,
            ],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        print("Could not find venv")
        print("Status : FAIL", exc.returncode, exc.output)


def jsonifypackages():

    """gets generated text file of packages from the getpackages.sh script and creates a json file of packages"""

    txtpath = os.path.join(script_dir, "../tempfiles/installed.txt")
    jsonpath = os.path.join(script_dir, "../tempfiles/installed.json")
    packagesdict = {}
    try:
        txt = open(txtpath, "r")
        # read textfile of packages
        lines = txt.readlines()
        for line in lines:
            # filter out header lines of package textfile
            if line != "Package    Version\n" and line != "---------- -------\n":
                # remove formatting of text file
                splitline = line.split(" ")
                splitline.remove("\n")
                while "" in splitline:
                    splitline.remove("")
                # add package to packages dict
                packagesdict[splitline[0]] = splitline[1]
        with open(jsonpath, "w") as json_file:
            json.dump(packagesdict, json_file)
    finally:
        txt.close()
        print(packagesdict)


if __name__ == "__main__":
    # main()
    app.run(debug=True)
    # climain()

