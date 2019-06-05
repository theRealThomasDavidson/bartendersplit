#this is where you look for how each of the json files work or how objects are made for each employee

import datetime as dt
import json
import utils
import tkinter as tk
from tkinter import ttk


jsonDataPath = "data_file.json"

class RepeatError(Exception):
    def __init__(self,string):
        print("Repeat Error: "+string)
        Exception.__init__(self)
        return

class CalenderFrame:
    """
    this is going to be my shitty version of a calender selector widget that I will use for the date selection it should
     consist of three Labels that say day, month, year, and three combo
    """
    def __init__(self, container, row):
        self.frame = ttk.Frame(container)
        self.frame.grid(row=row, columnspan=6, padx=5, pady=5)
        dayLabel=tk.Label(self.frame, text="Day")
        dayLabel.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        monthLabel=tk.Label(self.frame, text="Month")
        monthLabel.grid(row=0, column=1, columnspan=1, padx=5, pady=5)

        yearLabel=tk.Label(self.frame, text="Year")
        yearLabel.grid(row=0, column=2, columnspan=1, padx=5, pady=5)

        self.weekday = tk.StringVar()
        self.wdayLabel = tk.Label(self.frame, textvariable=self.weekday)      ##sanity check label to say what weekday it is supposed to be

        self.weekday.set("thisday")
        self.wdayLabel.grid(row=1, column=3, columnspan=1, padx=5, pady=5)
        years = list(range(2016, 2040))
        self.months = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
        self.days = list(range(1, 32))
        #None is used here because we have to change ordinal datetime months to offsets for the tuple and this was easy enough
        self.currMonth= tk.StringVar(self.frame)
        self.currYear = tk.StringVar(self.frame)
        self.currDay = tk.StringVar()
        yesterday = dt.date.today()-dt.timedelta(days=1)
        self.currMonthNum = yesterday.month
        self.currMonth.set(self.months[self.currMonthNum])
        self.currYear.set(yesterday.year)
        self.currDay.set(yesterday.day)
        monthOption = tk.OptionMenu(self.frame, self.currMonth, *self.months, command=lambda x: self.monthUpdate())
        yearOption = tk.OptionMenu(self.frame, self.currYear, *years, command=lambda x: self.setDays())
        self.dayOption = tk.OptionMenu(self.frame, self.currDay, *self.days, command=lambda x:self.weekDayCheck())
        monthOption.grid(row=1, column=1, padx=5, pady=5)
        yearOption.grid(row=1, column=2, padx=5, pady=5)
        self.dayOption.grid(row=1, column=0, padx=5, pady=5)

        self.setDays()


    def monthUpdate(self):
        """
        this should update the month num when you select a month then run set days etc.
        :return: this isn't meant to return anything
        """
        if self.currMonth.get()== "None":
        #this will always retun a string instead of a None Type so I Use "None" instead of None
            self.currMonth.set("Jan")
        self.currMonthNum = self.months.index(self.currMonth.get())
        self.setDays()

    def setDays(self):
        """
        this will set the current day number and will handle changing the number of days in the month for the month and
        year provided.
        :return: this isn't meant to return shit
        """
        temp = dt.date(year=int(self.currYear.get()), month=int(self.currMonthNum), day=2)
        monthDays = (temp.replace(month=temp.month % 12 + 1, day=1) - dt.timedelta(days=1)).day
        #daylist = self.dayOption["menu"]
        #daylist.delete(0, 'end')
        #for dayNum in range(1,monthDays+1):
        #    daylist.add_command(label=dayNum, command=lambda name=dayNum: self.days.set(name))
        self.weekDayCheck()

    def weekDayCheck(self):
        """
        this is our sanity check that will display a weekday associated with the last selected date.
        :return: this only displays to the screen and returns None
        """
        days=("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

        self.weekday.set(days[self.getDate().weekday()])


        #self.wdayLabel = tk.Label(self.frame, text=self.weekday)
        #self.wdayLabel.grid(row=1, column=3, columnspan=1, padx=5, pady=5)

    def getDate(self):
        """
        This will return a date time date that corresponds to the current selection on the frames widgets.
        :return: a datetime.date object that correponds to the currently selected date in the options on the frame
        """
        return dt.date(day=int(self.currDay.get()), month=int(self.currMonthNum), year=int(self.currYear.get()))


class AutocompleteCombobox(ttk.Combobox):
    """
    credit to https://stackoverflow.com/questions/47839813/python-tkinter-autocomplete-combobox-with-like-search
    stolen with minimal changes and minimal review on june 3 2019
    """

    def config(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if len(event.keysym) == 1:
            self.autocomplete()
        # No need for up/down, we'll jump to the popup
        # list at the position of the autocompletion


def findAllEmployees():
    """
    used to get a list of employees that worked before the current date.
    it uses the periodSummary default case to do it so it can definately be more optimized, but no decision has been
    made on if the .json should have an employees JavaScript Object that stores a list.
    :return: a list of all the employees that are in the .json before the current date.
    """
    return list(periodSummary(dt.date.today()).keys())
def addDay(dayinfo, force=False):
    """
    just updates the json file to add a new day to the file
    :param dayinfo:a dictionary of the form {
                                            "date" : object of datetime.date type
                                            "total tips" : float,
                                            "employees" :
                                                "name" :{
                                                "hours" : float ,
                                                "income" : float
                                                }
                                                ,...
                                            }
    :param force: this is a boolean that will tell this tyo override the last date that existed if it is there.
    :return: None
    """
    """
    this should add a day to the data and update any employee info push directly into the json file
    :return: None
    """
    if not isinstance(dayinfo["date"], dt.date):
        raise TypeError("Date must be in datetime.date format")
    day = dayinfo["date"]
    dateString = str(day) + "-" + day.strftime("%A")
    dayinfo["date"] = dateString

    with open(jsonDataPath, "r") as data:
        days=json.load(data)
    if dateString in days and not force:
        raise RepeatError("Day already in list")
        return
    days[dateString] = dayinfo
    with open(jsonDataPath, "w") as testjason:
        json.dump(days, testjason, sort_keys=True, indent=2)
    return


def periodSummary(endDate, startDate=None, lookback=None, employees=None):
    #lightly tested
    """
    this should give the summary of one or all employees in the system between the given dates.
    :param endDate: this is a datetime.date that corresponds to the last date in the lookup inclusive (required)
    :param lookback: this can be an int that says how long before the datetime one should
    :param startDate: this can be a datetime.date that corresponds to the start date that you want to include in the summary
    :param employee: when None will handle all employees that worked during the period, can be a string for 1 employee
    or a tuple of string that refer to many employees
    :return: a dictionary of the form
    {"name": {
        "Total Pay" : float,
        "Total Hours" : float,
        "Days Worked":{
            "datestring":{
                "Pay" : float
                "Hours" : float
                }
            ...}
        }
    ...
    }
    where datestring is the formatted datestring in addDay, and name is the employee name other things in quotes are literals.
    """
    summary={}
    if not isinstance(endDate, dt.date):
        raise TypeError("Date must be in the from of a datetime.date.")
    if not startDate:
        if not lookback:
            startDate = dt.date(1,1,1)
        else:
            if not isinstance(lookback, int):
                raise TypeError("Lookback must be an int")
            startDate = endDate - dt.timedelta(days=lookback)
    if not isinstance(startDate, dt.date):
        raise TypeError("Date must be in the from of a datetime.date.")

    with open(jsonDataPath, "r") as data:
        days = json.load(data)
    for day in days:
        date = utils.parseDateStrings(day)
        if not (date - startDate).days * (date - endDate).days >= 0:
            dayemployees = days[day]["employees"]
            for employee in dayemployees:

                if employees:
                    if employee not in employees:
                        continue
                if employee not in summary:
                    temp = {}
                    temp["Total Pay"] = 0.
                    temp["Total Hours"] =0.
                    temp["Days Worked"]={}
                    summary[employee] = temp
                temp = summary[employee]
                temp["Total Pay"] += dayemployees[employee]["income"]
                temp["Total Hours"] += dayemployees[employee]["hours"]
                temp["Days Worked"][day] = dayemployees[employee]
                summary[employee] = temp

    return summary


def main():
    """
    Used for testing objects. like why are you looking at this?
    :return: None
    """
    findAllEmployees()

    """

    a = {"date": dt.date.today(),
        "total tips": 140.,
        "employees": {
            "Alice": {
                "hours": 8.,
                "income": 140.
        }}
    }
    addDay(a,force=True)
    a = {"date": dt.date(2019,5,7),
        "total tips": 90.,
        "employees": {
            "Alice": {
                "hours": 3.,
                "income": 40.},
            "Bob": {
                "hours": 5.,
                "income": 50.}
        }}
    addDay(a,force=True)
    a = {"date":  dt.date(2019,5,6),
        "total tips": 275.,
        "employees": {
            "Alice": {
                "hours": 2.,
                "income": 45.},
            "Carol": {
                "hours": 7.,
                "income": 230.},
        }}
    addDay(a,force=True)
    a = {"date": dt.date.today(),
        "total tips": 140.,
        "employees": {
            "Alice": {
                "hours": 8.,
                "income": 140.
        }}
    }
    addDay(a,force=True)
    a = {"date": dt.date(2019, 4, 11),
        "total tips": 140.,
        "employees": {
            "Alice": {
                "hours": 8.,
                "income": 200000.
        }}
    }
    addDay(a,force=True)
    summary=periodSummary(dt.date(2019, 5,10),lookback=12)
    with open("newJason.json", "w") as testjason:
        json.dump(summary, testjason, sort_keys=True, indent=2)
    for key in summary:
        print(key, summary[key])
    return
    ##########################
    print(dt.date(2019, 5, 8).weekday())
    delta = dt.timedelta(days=7)
    a=dt.date.today()-delta
    
    
    with open(jsonDataPath, "r") as testjason:
        data=json.load(testjason)
    print(data)
    print(data["employees"]["greg"])
    for day in data["employees"]["greg"]["days_worked"]:
        print (day, data["employees"]["greg"]["days_worked"][day])
    """
if __name__== '__main__':
    main()