import tkinter as tk
import utils
import objects
from tkinter import ttk

def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

def pullData(fullwindow, currFrame):
        """
        this is a test function to see if i can easily pass info into a function and have it display new field under
        it with the info entered in the text boxes.
        :return: None should modify the mainWindow
        """
        framesWidgets = currFrame.winfo_children()
        for item in framesWidgets:
            print(item)
        comboWidgets = filter(lambda x: type(x) == ttk.Combobox, framesWidgets)
        for item in comboWidgets:
            print("name: "+item.get())

        textWidgets = list(filter(lambda x: type(x) == tk.Text, framesWidgets))
        totalCash = float(textWidgets[0].get("1.0", "end-1c")) + float(textWidgets[1].get("1.0", "end-1c"))
        print("Total Money: "+str(totalCash))

        for item in list(textWidgets)[2:]:
            print("hours: "+float(item.get("1.0", "end-1c")))

def main():
    """
    this will run the gui window
    :return: None always
    """


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


    moneyLabel=tk.Label(frames["inputDays"], text="Money received")
    moneyLabel.grid(row=2, column=0, columnspan=4, pady=5, padx=5, sticky=tk.W)

    cashLabel=tk.Label(frames["inputDays"], text="Cash")
    cashLabel.grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
    cashText= tk.Text(frames["inputDays"], height=1, width=6)
    cashText.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)
    cashText.bind("<Tab>", focus_next_window)
    creditLabel=tk.Label(frames["inputDays"], text="Credit")
    creditLabel.grid(row=3, column=2, pady=5, padx=5, sticky=tk.W)
    creditText= tk.Text(frames["inputDays"], height=1, width=6)
    creditText.grid(row=3, column=3, pady=5, padx=5, sticky=tk.W)
    creditText.bind("<Tab>", focus_next_window)

    ###start per employee doc
    nameLabel = tk.Label(frames["inputDays"], text="Employee Name")
    nameLabel.grid(row=10,column=0,padx=5,pady=5,sticky=tk.W, columnspan=2)
    nameBox = ttk.Combobox(frames["inputDays"], height=1, width=20)
    nameBox.grid(row=11, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)
    hoursLabel = tk.Label(frames["inputDays"], text="Employee Hours")
    hoursLabel.grid(row=10,column=2,padx=5,pady=5,sticky=tk.W)
    hoursText = tk.Text(frames["inputDays"], height=1, width=6)
    hoursText.grid(row=11, column=2, padx=5, pady=5, sticky=tk.W)
    hoursText.bind("<Tab>", focus_next_window)
    ###end per employee doc


    button= tk.Button(frames["inputDays"], text="Quit", command=lambda: pullData(mainWindow, frames["inputDays"]) )     ##used lambda becasue I can read/modify it easier.
    button.grid(row=200, column=1, pady=5, padx=5)


    mainWindow.mainloop()









if __name__=="__main__":
    main()