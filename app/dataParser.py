from datetime import datetime

# parse '%d Month, %Y' -> datetime(year, month, date)
monDict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, \
        'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12 }
def parseToDate(datestr):
    day, month, year = datestr.split(' ')
    day = int(day)
    month = monDict[month[:-1]]
    year = int(year)
    return datetime(year, month, day)
