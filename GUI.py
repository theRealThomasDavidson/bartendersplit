import tkinter as tk
import utils
import objects
import re
from tkinter import ttk


def addEmployee(holder):
    """
    this should add a new employee frame to the gui
    :return: this will return the frames reference
    """
    global newEmployeeRow
    newEmployeeRow += 1
    newFrame=ttk.Frame(holder)
    newFrame.grid(row=11 + newEmployeeRow, column=0, padx=0, pady=0, sticky=tk.W, columnspan=6)
    nameBox = objects.AutocompleteCombobox(newFrame, height=1, width=20)
    nameBox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)
    populateEmployees(nameBox)
    hoursText = tk.Text(newFrame, height=1, width=6)
    hoursText.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W, columnspan=2)
    hoursText.bind("<Tab>", focus_next_window)
    addEmployee=tk.Button(newFrame, text="Delete",command=lambda: delFrame(newFrame))
    addEmployee.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W, columnspan=1)


def delFrame(frame):
    """
    this is here to delete frames
    :param frame: the frame that we want to delete
    :return: None
    """
    frame.grid_forget()
    frame.destroy()


def populateEmployees(comboEmp):
    """
    this basically should populate the combo box for with names of employees that are already in the system
    it is only used for the population as handling the .json is left to the objects.py file
    :param comboEmp: this is a reference to the combo box that you want to populate.
    :return: None
    """
    comboEmp.config(objects.findAllEmployees())


def pull_number(numstring):
    """
    this is basically what we are going to be using so that we don't have toi parse every number on it's own.
    I want this to throw errors in a rather intuitive way that allows us to easily tell what is needed for proper input
    instead.
    it should be able to handle tabs and spaces easily,
    :param numstring: a str tyhat is the input of the user
    :return: a float that is the a number that is associated with the
    """
    unexpectedDigits = re.findall("(?!\d|\.|\s)", numstring)
    if len(unexpectedDigits) > 1 or unexpectedDigits[0]:
        raise ValueError("Expected a string that converts to a floating point (decimal) number in user input.")

    else:
        numbers = re.findall("(\d+\.\d+|\d+)*", numstring)
        numbers=list(filter(lambda x: bool(x),numbers))
        howMany = len(numbers)
        if howMany == 0:
            return 0.
        elif howMany > 1:
            raise ValueError("One number was expected, more than one was received.")
        else:
            return float(numbers[0])


def focus_next_window(event):
    """
    this basically keeps a button press form registering during a press and instead changes focus to the next item.
    :param event: is a button press during highlighting (tab for the text/comboboxes)
    :return: "break" here basically tells the current text/combobox to ignore the button press.
    """
    event.widget.tk_focusNext().focus()
    return "break"


def pullData(fullwindow, currFrame):
    """
    this is a test function to see if i can easily pass info into a function and have it display new field under
    it with the info entered in the text boxes.
    :return: None should modify the mainWindow
    """
    framesWidgets = currFrame.winfo_children()

    textWidgets = list(filter(lambda x: type(x) == tk.Text, framesWidgets))
    totalCash = pull_number(textWidgets[0].get("1.0", "end-1c")) + pull_number(textWidgets[1].get("1.0", "end-1c"))
    print("Total Money: "+str(totalCash))

    employeeFrames = filter(lambda x: type(x) == ttk.Frame, framesWidgets)
    for employee in employeeFrames:
        temp = employee.winfo_children()
        currName=temp[0].get()
        currHours=pull_number(temp[1].get("1.0", "end-1c"))
        print("name: "+currName+" \nHours: "+str(currHours))

    print("\n\n")

def main():
    """
    this will run the gui window
    :return: None always
    """
    global newEmployeeRow
    newEmployeeRow = 1

    #whole windows
    mainWindow = tk.Tk()
    mainWindow.wm_title("this is a window")
    mainWindow.resizable(True, True)


    #this is where the select frames go to show different thingsa in the gui.
    frames = {}

    notebook = ttk.Notebook(mainWindow)

    frames["inputDays"] = ttk.Frame(notebook)
    frames["reportPrint"] = ttk.Frame(notebook)

    adjustWindow = ttk.Frame(notebook)
    notebook.add(frames["inputDays"], text="Enter Day info")
    notebook.add(frames["reportPrint"], text="Get Reports")
    notebook.grid(row=0, column=0, columnspan=3, pady=5, padx=5,)

    inputTitle=tk.Label(frames["inputDays"], text="You can input money data for days here.")
    inputTitle.grid(row=1, column=0, pady=5, padx=5, columnspan=4)
    objects.CalenderFrame(frames["inputDays"], 2)
    moneyLabel=tk.Label(frames["inputDays"], text="Money received")
    moneyLabel.grid(row=4, column=0, columnspan=4, pady=5, padx=5)

    cashLabel=tk.Label(frames["inputDays"], text="Cash")
    cashLabel.grid(row=6, column=0, pady=5, padx=5, sticky=tk.W)
    cashText= tk.Text(frames["inputDays"], height=1, width=6)
    cashText.grid(row=6, column=1, pady=5, padx=5, sticky=tk.W)
    cashText.bind("<Tab>", focus_next_window)
    creditLabel=tk.Label(frames["inputDays"], text="Credit")
    creditLabel.grid(row=6, column=2, pady=5, padx=5, sticky=tk.W)
    creditText= tk.Text(frames["inputDays"], height=1, width=6)
    creditText.grid(row=6, column=3, pady=5, padx=5, sticky=tk.W)
    creditText.bind("<Tab>", focus_next_window)
    nameLabel = tk.Label(frames["inputDays"], text="Employee Name")
    nameLabel.grid(row=10,column=0,padx=5,pady=5,sticky=tk.W, columnspan=2)
    hoursLabel = tk.Label(frames["inputDays"], text="Hours")
    hoursLabel.grid(row=10, column=2, padx=5, pady=5, columnspan=2)


    ###start per employee doc
    firstEmpFrame=ttk.Frame(frames["inputDays"])
    firstEmpFrame.grid(row=11, column=0, padx=0, pady=0, sticky=tk.W, columnspan=6)
    nameBox = objects.AutocompleteCombobox(firstEmpFrame, height=1, width=20)
    nameBox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)
    populateEmployees(nameBox)
    hoursText = tk.Text(firstEmpFrame, height=1, width=6)
    hoursText.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W, columnspan=2)
    hoursText.bind("<Tab>", focus_next_window)
    addEmployeeBtn=tk.Button(firstEmpFrame, text="Add", command=lambda: addEmployee(frames["inputDays"]))
    addEmployeeBtn.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W, columnspan=1)
    ###end per employee doc


    button= tk.Button(frames["inputDays"], text="Log Report", command=lambda: pullData(mainWindow, frames["inputDays"]) )     ##used lambda becasue I can read/modify it easier.
    button.grid(row=2000, column=1, pady=5, padx=5)


    mainWindow.mainloop()


if __name__=="__main__":
    main()