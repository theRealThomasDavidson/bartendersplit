"""
this is where you look for how each of the json files work or how objects are made for each employee
"""
import datetime as dt
import json


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


def main():
    """
    Used for testing objects. like why are you looking at this?
    :return: None
    """

    daydict={"date": dt.date.today(),
        "total tips": 300.,
        "employees":{
            "greg": {
               "hours": 40.,
               "income": 300.
        }}
    }
    addDay(daydict,force=True)
    daydict={"date": dt.date(2019,6,15),
        "total tips": 200.,
        "employees":{
            "greg": {
               "hours": 4.,
               "income": 200.
        }}
    }
    addDay(daydict, force=True)
    daydict={"date": dt.date(2019,7,19),
        "total tips": 150.,
        "employees":{
            "greg": {
               "hours": 6.,
               "income": 150.
        }}
    }
    addDay(daydict, force=True)
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