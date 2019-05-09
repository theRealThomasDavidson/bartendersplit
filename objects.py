#this is where you look for how each of the json files work or how objects are made for each employee

import datetime as dt
import json
import utils


jsonDataPath = "data_file.json"

class RepeatError(Exception):
    def __init__(self,string):
        print("Repeat Error: "+string)
        Exception.__init__(self)
        return


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
    """
    
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