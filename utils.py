def calcHours(individualHours=()):
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
        print(individualHours, individualHours <= 0.)
        if individualHours <= 0.:
            raise TypeError("Hours must be a list or tuple of positive numbers")
        return (individualHours, (1.,))

    raise TypeError("Hours must be a list or tuple of positive numbers")


def main():
    """
    Used for testing utils. like why are you looking at this?
    :return: None
    """
    print(calcHours((2.5, 5., 7.5)))
    print(calcHours(2.5))
    #print(calcHours((2.5, 5., -7.5)))
    #print(calcHours(-2.5))


if __name__== '__main__':
    main()