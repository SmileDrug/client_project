import datetime
import pytz

def strToDate(string):
    string=string.replace("T"," ")
    string = string[:19]
    _datetime = datetime.datetime.strptime(string,"%Y-%m-%d %H:%M:%S")
    return _datetime

def toEST(date):
	eastern = pytz.timezone('US/Eastern')
	date=date.astimezone(eastern)
	return date
