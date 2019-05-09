import datetime as dt

def calcHours(individualHours=()):
    #tested
    """
    adds up all the hours and gives proportion of each
    :param individualHours: a list or tuple of the hours of individual contributors
    :return: a tuple of the form (float, (float,...)) where the first float is total hours worked and the tuple is the
    proportion of hours worked by each person in the order that individual hours was in
    """
    if isinstance(individualHours, (tuple, list)):
        try:
            check = lambda x: x <= 0.
            total = sum(individualHours)
            if list(filter(check, individualHours)):
                raise TypeError
            return (total, tuple([x/total for x in individualHours]))

        except TypeError:
            TypeError("Hours must be a list or tuple of positive numbers")

    if isinstance(individualHours, (float, int)):
        if individualHours <= 0.:
            raise TypeError("Hours must be a list or tuple of positive numbers")
        return (individualHours, (1.,))

    raise TypeError("Hours must be a list or tuple of positive numbers")


def calcPay(individualHours=(),pot=0):
    #tested
    """
    this bit will calculate how much each person takes home before any blanket adds or subs.
    :param individualHours: a list or tuple of the hours of individual contributors
    :param pot: the amount of money getting split amoung the people
    :return: a tuple of the form (float,...) where the floats are the amount of money each person gets for the day
    """

    if isinstance(pot, (int,float)):
        if pot < 0.:
            raise TypeError("The shared money for a day must be a positive number.")

        _, shares = calcHours(individualHours)
        return tuple([round(pot*x, 2) for x in shares])

    raise TypeError("The shared money for a day must be a positive number.")

def parseDateStrings(datestring):
    #lightly tested
    """
    needed a parser to handle the keeping dates as strings in json files
    :param datestring: a string of the form
    :return: a datetime.date object of the same form
    """
    dates=datestring.split("-")
    return dt.date(int(dates[0]), int(dates[1]), int(dates[2]))


def main():
    """
    Used for testing utils. like why are you looking at this?
    :return: None
    """
    #print(calcHours((2.5, 5., 7.5)))
    #print(calcHours(2.5))
    #print(calcHours((2.5, 5., -7.5)))
    #print(calcHours(-2.5))
    #print(calcPay((2.5, 5., 7.5), 200))
    print (dt.date.today()==parseDateStrings(str(dt.date.today())))
    now = dt.date.today()
    print(now.strftime("%A"))


if __name__== '__main__':
    main()